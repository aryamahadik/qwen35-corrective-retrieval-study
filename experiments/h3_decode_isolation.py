"""
H3 --- Is the measured sharing advantage PREFILL amortization or DECODE amortization?

WHY THIS IS THE DECISIVE EXPERIMENT
-----------------------------------
H2 measured a 2.79x throughput advantage for a shared prefix at C=32 under vLLM prefix caching,
with a clean control (caching OFF => 1.06x, i.e. no effect). The effect is real and it is
attributable to caching.

But H2 used a 4,096-token prefix and only 64 output tokens, so WALL CLOCK IS PREFILL-DOMINATED:
the distinct arm re-prefills ~131k tokens while the shared arm prefills 4,096 once. Prefill
amortization was never in dispute -- it is the already-conceded TTFT win (3.4x-36x).

The published T2 obstruction is about the DECODE residency tax: the claim that holding m resident
KV tokens costs delta*m on EVERY output token, per sequence, forever. That is what makes a constant
prefill saving lose to a linear tax at n* ~ 782 output tokens.

Standard PagedAttention reads a sequence's KV blocks per sequence during decode, even when the
block table points at SHARED physical blocks. Only CASCADE ATTENTION -- one flash-attention call
over the shared prefix, merged with per-sequence suffixes via log-sum-exp -- amortizes the decode
read. Cascade attention landed in vLLM V1; 0.6.6 predates it.

THE TEST
--------
Hold concurrency and prefix length fixed. Sweep OUTPUT LENGTH. Prefill cost is constant in n_out;
decode cost is linear in n_out. So the two hypotheses separate cleanly:

  PREFILL-ONLY   advantage -> 1.0 as n_out grows (the constant saving is amortized away)
  DECODE-TOO     advantage stays roughly FLAT in n_out

PRE-REGISTERED PREDICTION
-------------------------
  I expect PREFILL-ONLY. If so, H2's 2.79x does NOT rescue T2, the decode obstruction stands, and
  the honest verdict is unchanged. Stating this before the run.

FALSIFICATION OF THE OBSTRUCTION
--------------------------------
If the advantage is still > 1.5x at n_out = 1024, decode genuinely amortizes under sharing, delta
is not per-sequence, and the T2 end-to-end obstruction is broken for multi-tenant serving.

COST: A10G ~$1.10/hr, budgeted under 12 minutes => ~$0.22. Image already cached from H2.
NO MODEL RUNS ON THE PRINCIPAL'S MACHINE.

Usage:
    modal run experiments/h3_decode_isolation.py
"""

import json
import time

import modal

MODEL = "Qwen/Qwen2.5-0.5B"
GPU = "A10G"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "VLLM_LOGGING_LEVEL": "WARNING",
    })
)

app = modal.App("qcarve-h3-decode-isolation")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)


@app.function(image=image, gpu=GPU, timeout=2400, volumes={"/hf": hf_cache})
def isolate(prefix_tokens=4096, C=32, out_lens=(16, 64, 256, 1024)):
    import os
    os.environ["HF_HOME"] = "/hf"

    import random
    from vllm import LLM, SamplingParams

    llm = LLM(
        model=MODEL,
        enable_prefix_caching=True,
        gpu_memory_utilization=0.85,
        max_model_len=8192,
        disable_log_stats=True,
    )
    tok = llm.get_tokenizer()

    def make_prefix(seed):
        rng = random.Random(seed)
        return tok.decode([rng.randint(1000, 30000) for _ in range(prefix_tokens)])

    shared_prefix = make_prefix(0)
    distinct_prefixes = [make_prefix(100 + i) for i in range(C)]

    rows = []
    for n_out in out_lens:
        sp = SamplingParams(temperature=0.0, max_tokens=n_out, ignore_eos=True)
        for mode in ("shared", "distinct"):
            if mode == "shared":
                prompts = [shared_prefix + f"\n\nQ{i}: explain." for i in range(C)]
            else:
                prompts = [distinct_prefixes[i] + f"\n\nQ{i}: explain." for i in range(C)]

            llm.generate(prompts[:1], SamplingParams(temperature=0.0, max_tokens=4,
                                                     ignore_eos=True))  # warm
            t0 = time.perf_counter()
            outs = llm.generate(prompts, sp)
            dt = time.perf_counter() - t0

            gen = sum(len(o.outputs[0].token_ids) for o in outs)
            rows.append({
                "n_out": n_out, "mode": mode, "C": C,
                "wall_s": round(dt, 3),
                "gen_tokens": gen,
                "gen_tok_s": round(gen / dt, 1),
            })

    hf_cache.commit()
    import torch
    return {"gpu": torch.cuda.get_device_name(0), "model": MODEL,
            "prefix_tokens": prefix_tokens, "C": C, "rows": rows}


@app.local_entrypoint()
def main(out: str = "h3_results.json"):
    r = isolate.remote()
    with open(out, "w") as fh:
        json.dump(r, fh, indent=2)

    print(f"\nGPU: {r['gpu']}   prefix={r['prefix_tokens']} tok   C={r['C']}\n")
    print(f"{'n_out':>7} {'shared tok/s':>13} {'distinct tok/s':>15} {'advantage':>11} "
          f"{'shared s':>9} {'distinct s':>11}")
    print("-" * 72)

    def get(n_out, mode, field):
        for row in r["rows"]:
            if row["n_out"] == n_out and row["mode"] == mode:
                return row[field]
        return None

    pts = []
    for n_out in sorted({row["n_out"] for row in r["rows"]}):
        s, d = get(n_out, "shared", "gen_tok_s"), get(n_out, "distinct", "gen_tok_s")
        sw, dw = get(n_out, "shared", "wall_s"), get(n_out, "distinct", "wall_s")
        if s and d:
            adv = s / d
            pts.append((n_out, adv))
            print(f"{n_out:>7} {s:>13.1f} {d:>15.1f} {adv:>10.2f}x "
                  f"{sw:>9.2f} {dw:>11.2f}")

    print(f"\n{'='*72}\nVERDICT\n{'='*72}")
    if len(pts) >= 2:
        (n_lo, a_lo), (n_hi, a_hi) = pts[0], pts[-1]
        decay = a_hi / a_lo
        print(f"  Advantage at n_out={n_lo}: {a_lo:.2f}x")
        print(f"  Advantage at n_out={n_hi}: {a_hi:.2f}x")
        print(f"  Retention as output grows {n_hi//n_lo}x: {decay:.2f}\n")

        if a_hi > 1.5:
            print(f"  DECODE AMORTIZES. Advantage holds at {a_hi:.2f}x with {n_hi} output tokens,")
            print("  where decode dominates wall clock. The residency tax is NOT per-sequence")
            print("  under sharing. The T2 end-to-end obstruction is BROKEN for multi-tenant")
            print("  same-corpus serving, and n* scales with concurrency.")
        elif a_hi > 1.15:
            print(f"  PARTIAL ({a_hi:.2f}x at n_out={n_hi}). Some decode benefit, but far below")
            print("  the prefill-regime figure. Recompute n* with the measured decode factor only.")
        else:
            print(f"  PREFILL-ONLY, AS PREDICTED. Advantage collapses to {a_hi:.2f}x once decode")
            print("  dominates. H2's headline was prefill amortization -- real, valuable, and")
            print("  ALREADY CONCEDED as the TTFT win. It does not touch the decode residency")
            print("  tax. THE T2 END-TO-END OBSTRUCTION STANDS.")

    print(f"\n  Full results -> {out}\n")
