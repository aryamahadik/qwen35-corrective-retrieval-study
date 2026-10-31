"""
H2 --- Does the PRODUCTION serving kernel amortize a shared KV prefix across a batch?

WHY THIS EXPERIMENT EXISTS
--------------------------
H1 (experiments/h1_shared_prefix.py) REFUTED the sharing hypothesis on HuggingFace transformers:
a stride-0 expanded cache and a real B-fold copy produced BYTE-IDENTICAL peak memory
(5050.5 MiB at m=8192, B=32) and identical throughput (6.79 vs 6.71 tok/s/seq, 0.98x).
The attention path materializes the view, so the "free" sharing is not free.

But that is a property of HF's attention path, not of the idea. vLLM's PagedAttention stores shared
prefixes as shared PHYSICAL blocks behind distinct LOGICAL sequences, and vLLM ships CASCADE
ATTENTION -- a kernel that reads a shared prefix once and broadcasts it across the batch instead of
re-reading it per sequence.

THE QUESTION: does the production stack amortize, and is it on by default?

This matters because the entire T2 end-to-end obstruction rests on the residency tax being
PER-SEQUENCE. If a shared corpus cache amortizes across B concurrent sessions, then
delta_eff = delta / B and the crossover n* = a/delta scales with B, moving it from ~782 output
tokens to beyond any realistic agent output at B=32.

PRE-REGISTERED PREDICTIONS
--------------------------
  P1  With prefix caching ON and a long shared prefix, total throughput scales markedly better
      with concurrency than with distinct prefixes of the same length.
  P2  Time-to-first-token for requests 2..N on the shared prefix is far below request 1
      (the prefix is computed once).
  P3  If P1 fails -- shared and distinct scale alike -- then amortization does not occur in
      production either, the residency tax is per-sequence at every level of the stack, and the
      T2 obstruction is CONFIRMED rather than merely unrefuted.

WHAT WOULD FALSIFY THE WHOLE PROGRAMME
--------------------------------------
P3 holding. That is a clean, decisive negative and it should be reported as the result.

COST: A10G ~$1.10/hr. Image build is one-time and cached. Run budgeted under 10 minutes => <$0.20.
NO MODEL RUNS ON THE PRINCIPAL'S MACHINE. All execution is remote.

Usage:
    modal run experiments/h2_cascade.py
"""

import json
import time

import modal

MODEL = "Qwen/Qwen2.5-0.5B"
GPU = "A10G"

image = (
    modal.Image.debian_slim(python_version="3.11")
    # transformers must be pinned <5: vLLM 0.6.6 calls
    # tokenizer.all_special_tokens_extended, which transformers 5.x removed.
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "VLLM_LOGGING_LEVEL": "WARNING",
    })
)

app = modal.App("qcarve-h2-cascade")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)


@app.function(image=image, gpu=GPU, timeout=2400, volumes={"/hf": hf_cache})
def measure(prefix_tokens=4096, n_out=64, concurrencies=(1, 4, 8, 16, 32)):
    """
    Two arms at each concurrency level:
      SHARED   -- every request carries the SAME long prefix (cacheable, shareable)
      DISTINCT -- every request carries a DIFFERENT long prefix of identical length

    Same total token volume in both arms. The only difference is shareability.
    """
    import os
    os.environ["HF_HOME"] = "/hf"

    from vllm import LLM, SamplingParams

    results = {}

    for pc_enabled in (True, False):
        llm = LLM(
            model=MODEL,
            enable_prefix_caching=pc_enabled,
            gpu_memory_utilization=0.85,
            max_model_len=8192,
            disable_log_stats=True,
            enforce_eager=False,
        )
        tok = llm.get_tokenizer()
        sp = SamplingParams(temperature=0.0, max_tokens=n_out, ignore_eos=True)

        # Build prefixes of EXACTLY prefix_tokens length so both arms move equal volume.
        def make_prefix(seed):
            rng = __import__("random").Random(seed)
            ids = [rng.randint(1000, 30000) for _ in range(prefix_tokens)]
            return tok.decode(ids)

        shared_prefix = make_prefix(0)
        rows = []

        for C in concurrencies:
            for mode in ("shared", "distinct"):
                if mode == "shared":
                    prompts = [shared_prefix + f"\n\nQ{i}: explain." for i in range(C)]
                else:
                    prompts = [make_prefix(100 + i) + f"\n\nQ{i}: explain." for i in range(C)]

                llm.generate(prompts[:1], sp)          # warm the engine
                t0 = time.perf_counter()
                outs = llm.generate(prompts, sp)
                dt = time.perf_counter() - t0

                gen = sum(len(o.outputs[0].token_ids) for o in outs)
                prompt_toks = sum(len(o.prompt_token_ids) for o in outs)
                rows.append({
                    "C": C, "mode": mode,
                    "wall_s": round(dt, 3),
                    "gen_tokens": gen,
                    "prompt_tokens": prompt_toks,
                    "gen_tok_s": round(gen / dt, 1),
                    "gen_tok_s_per_seq": round(gen / dt / C, 2),
                })

        results["prefix_caching_on" if pc_enabled else "prefix_caching_off"] = rows
        del llm
        import gc, torch
        gc.collect(); torch.cuda.empty_cache()

    hf_cache.commit()
    import torch
    return {"gpu": torch.cuda.get_device_name(0), "model": MODEL,
            "prefix_tokens": prefix_tokens, "n_out": n_out, "results": results}


@app.local_entrypoint()
def main(out: str = "h2_results.json"):
    r = measure.remote()
    with open(out, "w") as fh:
        json.dump(r, fh, indent=2)

    print(f"\nGPU: {r['gpu']}   prefix={r['prefix_tokens']} tok   out={r['n_out']} tok\n")

    for key, rows in r["results"].items():
        print(f"--- {key} ---")
        print(f"{'C':>4} {'mode':>9} {'wall s':>8} {'gen tok/s':>10} {'per-seq':>9}")
        for row in rows:
            print(f"{row['C']:>4} {row['mode']:>9} {row['wall_s']:>8.2f} "
                  f"{row['gen_tok_s']:>10.1f} {row['gen_tok_s_per_seq']:>9.2f}")
        print()

    on = r["results"].get("prefix_caching_on", [])

    def get(C, mode):
        for row in on:
            if row["C"] == C and row["mode"] == mode:
                return row["gen_tok_s"]
        return None

    Cs = sorted({row["C"] for row in on})
    if len(Cs) >= 2:
        lo, hi = Cs[0], Cs[-1]
        print("=" * 68)
        print(f"SCALING FROM C={lo} TO C={hi}, prefix caching ON")
        print("=" * 68)
        s_lo, s_hi = get(lo, "shared"), get(hi, "shared")
        d_lo, d_hi = get(lo, "distinct"), get(hi, "distinct")
        if all(v for v in (s_lo, s_hi, d_lo, d_hi)):
            s_scale, d_scale = s_hi / s_lo, d_hi / d_lo
            print(f"  shared   throughput scales {s_scale:.2f}x  ({s_lo:.0f} -> {s_hi:.0f} tok/s)")
            print(f"  distinct throughput scales {d_scale:.2f}x  ({d_lo:.0f} -> {d_hi:.0f} tok/s)")
            adv = s_scale / d_scale
            print(f"\n  SHARING ADVANTAGE: {adv:.2f}x\n")
            print("=" * 68)
            if adv > 1.5:
                print(f"  P1 CONFIRMED ({adv:.2f}x). The production kernel DOES amortize a shared")
                print("  prefix. delta_eff = delta/B, so n* scales with concurrency and the T2")
                print("  end-to-end obstruction dissolves for multi-tenant same-corpus serving.")
                print(f"  At C={hi} the crossover moves from ~782 to ~{782*adv:.0f}+ output tokens.")
            elif adv > 1.15:
                print(f"  PARTIAL ({adv:.2f}x). Sharing helps but does not fully amortize.")
                print("  Recompute n* with the measured factor before claiming anything.")
            else:
                print(f"  P3 --- NO AMORTIZATION ({adv:.2f}x). HYPOTHESIS REFUTED IN PRODUCTION TOO.")
                print("  The residency tax is per-sequence at every level of the stack.")
                print("  The T2 end-to-end obstruction is CONFIRMED, not merely unrefuted.")
                print("  This closes the last open route. Stop.")

    print(f"\n  Full results -> {out}\n")
