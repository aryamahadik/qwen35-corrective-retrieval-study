"""
H1 --- Does a SHARED KV prefix amortize the residency tax across a batch?

THE CLAIM UNDER TEST
--------------------
Every measurement that produced the "decode tax kills end-to-end latency" verdict was taken at
batch size 1. Decode time per token is

    t  =  (W_bytes + m * k_KV) / B_eff

At B=1 the weight term dominates: for a 4-bit 4B model, weights ~2.1 GB vs ~288 MB of KV at
m=2048, so residency is ~12% of decode. The published obstruction says the residency tax
n*delta*m grows linearly in output length n while the prefill saving a*m is constant, crossing at
n* = a/delta = 782 output tokens.

BUT: under batched decoding the weight read amortizes across the batch. If the KV cache is SHARED
(many concurrent sessions over the SAME repository), the cache tiles are loaded into SRAM once per
attention op and reused across every query in the batch, so the KV read amortizes too:

    delta_eff = delta / B      =>      n*_shared = B * n*

At B=32 that moves the crossover from 782 to ~25,000 output tokens -- past any realistic agent
output. The obstruction would not be engineered around; it would dissolve.

If instead each session carries its OWN prefix, nothing amortizes and the tax is real.

PREDICTIONS (pre-registered, stated before the run)
---------------------------------------------------
  P1  SHARED:   tokens/sec/sequence stays roughly FLAT as B grows (sub-linear degradation).
  P2  DISTINCT: tokens/sec/sequence degrades materially faster than SHARED as B grows.
  P3  MEMORY:   peak GPU memory for SHARED is ~O(m); for DISTINCT it is ~O(B*m).
  P4  delta:    the batch-1 residency slope on cloud silicon is measurable and can be compared
                against the value derived from public specs.

FALSIFICATION
-------------
If SHARED and DISTINCT degrade at the SAME rate, the sharing hypothesis is dead, the residency tax
is per-sequence regardless of cache provenance, and the T2 obstruction stands exactly as published.

COST CONTROL
------------
A10G at ~$1.10/hr. The full sweep is budgeted under 20 minutes => under $0.40.
Smoke test first (`--smoke`) so a crash costs cents, not dollars.

NO MODEL IS RUN ON THE PRINCIPAL'S MACHINE. All execution is remote on Modal.

Usage:
    modal run experiments/h1_shared_prefix.py::smoke
    modal run experiments/h1_shared_prefix.py
"""

import json
import time

import modal

MODEL = "Qwen/Qwen2.5-0.5B"   # small on purpose: we are measuring BANDWIDTH, not quality
GPU = "A10G"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.5.1",
        "transformers==4.46.3",
        "accelerate==1.1.1",
        "numpy==1.26.4",
    )
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"})
)

app = modal.App("qcarve-h1-shared-prefix")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)


def _load():
    """Load model + tokenizer once inside the container."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(MODEL, cache_dir="/hf")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, torch_dtype=torch.float16, cache_dir="/hf"
    ).cuda().eval()
    return tok, model


def _kv_bytes_per_token(model):
    """k_KV = 2 * L * H_kv * d_head * bytes. Exact, from the config."""
    c = model.config
    n_kv = getattr(c, "num_key_value_heads", c.num_attention_heads)
    d_head = c.hidden_size // c.num_attention_heads
    return 2 * c.num_hidden_layers * n_kv * d_head * 2  # fp16


def _prefill(model, m):
    """Build a length-m KV cache with batch 1. Returns legacy tuple form."""
    import torch
    from transformers import DynamicCache

    ids = torch.randint(100, 30000, (1, m), device="cuda")
    with torch.no_grad():
        out = model(input_ids=ids, use_cache=True)
    cache = out.past_key_values
    return cache.to_legacy_cache() if isinstance(cache, DynamicCache) else cache


def _make_batch(legacy, B, mode):
    """
    SHARED   -> expand(): a stride-0 VIEW. One physical copy, B logical sequences.
    DISTINCT -> repeat(): a real copy. B physical copies.
    """
    import torch
    from transformers import DynamicCache

    out = []
    for k, v in legacy:
        if mode == "shared":
            out.append((k.expand(B, -1, -1, -1), v.expand(B, -1, -1, -1)))
        else:
            out.append((k.repeat(B, 1, 1, 1), v.repeat(B, 1, 1, 1)))
    return DynamicCache.from_legacy_cache(tuple(out))


def _decode(model, cache, B, m, n_steps):
    """Decode n_steps tokens with batch B over an existing cache. Returns tok/s/seq."""
    import torch

    ids = torch.randint(100, 30000, (B, 1), device="cuda")
    pos = torch.full((B, 1), m, device="cuda", dtype=torch.long)

    with torch.no_grad():  # warmup
        for _ in range(3):
            o = model(input_ids=ids, past_key_values=cache,
                      position_ids=pos, use_cache=True)
            cache = o.past_key_values
    torch.cuda.synchronize()

    t0 = time.perf_counter()
    with torch.no_grad():
        for i in range(n_steps):
            o = model(input_ids=ids, past_key_values=cache,
                      position_ids=pos + i + 3, use_cache=True)
            cache = o.past_key_values
    torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    return (n_steps * B) / dt, (n_steps / dt)   # total tok/s, per-seq tok/s


@app.function(image=image, gpu=GPU, timeout=900, volumes={"/hf": hf_cache})
def smoke():
    """Cheap sanity check: does the image build, model load, cache manipulate?"""
    import torch

    tok, model = _load()
    k_kv = _kv_bytes_per_token(model)
    legacy = _prefill(model, 512)

    shared = _make_batch(legacy, 8, "shared")
    distinct = _make_batch(legacy, 8, "distinct")
    sk = shared.to_legacy_cache()[0][0]
    dk = distinct.to_legacy_cache()[0][0]

    tot, per = _decode(model, shared, 8, 512, 16)
    hf_cache.commit()

    return {
        "gpu": torch.cuda.get_device_name(0),
        "model": MODEL,
        "kv_bytes_per_token": k_kv,
        "shared_shape": list(sk.shape),
        "shared_stride0": sk.stride()[0],       # 0 => true view, no copy
        "distinct_stride0": dk.stride()[0],     # != 0 => real copy
        "shared_is_view": sk.stride()[0] == 0,
        "decode_tok_s_total": round(tot, 1),
        "decode_tok_s_per_seq": round(per, 1),
        "ok": True,
    }


@app.function(image=image, gpu=GPU, timeout=2400, volumes={"/hf": hf_cache})
def sweep(m_list=(512, 2048, 8192), b_list=(1, 2, 4, 8, 16, 32), n_steps=32):
    """The measurement. Returns one row per (m, B, mode)."""
    import torch

    tok, model = _load()
    k_kv = _kv_bytes_per_token(model)
    rows = []

    for m in m_list:
        legacy = _prefill(model, m)
        for mode in ("shared", "distinct"):
            for B in b_list:
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats()
                try:
                    cache = _make_batch(legacy, B, mode)
                    tot, per = _decode(model, cache, B, m, n_steps)
                    peak = torch.cuda.max_memory_allocated() / 2**20
                    rows.append({
                        "m": m, "B": B, "mode": mode,
                        "tok_s_total": round(tot, 2),
                        "tok_s_per_seq": round(per, 2),
                        "peak_mib": round(peak, 1),
                        "kv_mib_nominal": round(B * m * k_kv / 2**20, 1),
                        "ok": True,
                    })
                    del cache
                except Exception as e:  # OOM on the distinct arm is itself a result
                    rows.append({"m": m, "B": B, "mode": mode, "ok": False,
                                 "error": f"{type(e).__name__}: {e}"[:160]})
                    torch.cuda.empty_cache()

    # Batch-1 residency slope: regress per-token latency on m. This is delta.
    b1 = [r for r in rows if r.get("ok") and r["B"] == 1 and r["mode"] == "shared"]
    delta = None
    if len(b1) >= 2:
        xs = [r["m"] for r in b1]
        ys = [1000.0 / r["tok_s_per_seq"] for r in b1]     # ms per token
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        den = sum((x - mx) ** 2 for x in xs)
        slope = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / den if den else None
        if slope is not None:
            delta = {
                "ms_per_output_token_per_resident_kv_token": slope,
                "t0_ms": my - slope * mx,
                "implied_B_eff_GB_s": (k_kv / (slope * 1e-3)) / 1e9 if slope > 0 else None,
                "points": list(zip(xs, [round(y, 3) for y in ys])),
            }

    hf_cache.commit()
    return {"gpu": torch.cuda.get_device_name(0), "model": MODEL,
            "kv_bytes_per_token": k_kv, "n_steps": n_steps,
            "rows": rows, "delta_batch1": delta}


@app.local_entrypoint()
def main(smoke_only: bool = False, out: str = "h1_results.json"):
    if smoke_only:
        print(json.dumps(smoke.remote(), indent=2))
        return

    print("H1 smoke test first (cost control)...")
    s = smoke.remote()
    print(json.dumps(s, indent=2))
    if not s.get("ok") or not s.get("shared_is_view"):
        print("\nSMOKE FAILED or sharing is not a true view. Stopping before the sweep.")
        return

    print("\nRunning sweep...")
    r = sweep.remote()

    with open(out, "w") as fh:
        json.dump(r, fh, indent=2)

    print(f"\nGPU: {r['gpu']}   k_KV = {r['kv_bytes_per_token']:,} B/token\n")
    print(f"{'m':>6} {'B':>4} {'mode':>9} {'tok/s/seq':>10} {'tok/s tot':>10} {'peak MiB':>9}")
    print("-" * 56)
    for row in r["rows"]:
        if row.get("ok"):
            print(f"{row['m']:>6} {row['B']:>4} {row['mode']:>9} "
                  f"{row['tok_s_per_seq']:>10.2f} {row['tok_s_total']:>10.1f} {row['peak_mib']:>9.1f}")
        else:
            print(f"{row['m']:>6} {row['B']:>4} {row['mode']:>9} {'FAILED':>10}  {row.get('error','')[:40]}")

    # ---- the decisive comparison -------------------------------------------------
    print(f"\n{'='*70}\nP1/P2 --- per-sequence throughput retention at B=32 vs B=1\n{'='*70}")
    verdict_rows = []
    for m in {row["m"] for row in r["rows"]}:
        def get(mode, B):
            for row in r["rows"]:
                if row.get("ok") and row["m"] == m and row["B"] == B and row["mode"] == mode:
                    return row["tok_s_per_seq"]
            return None
        out_ = {}
        for mode in ("shared", "distinct"):
            a, b = get(mode, 1), get(mode, 32)
            out_[mode] = (b / a) if (a and b) else None
        verdict_rows.append((m, out_["shared"], out_["distinct"]))
        s_ = f"{out_['shared']:.3f}" if out_["shared"] else "n/a"
        d_ = f"{out_['distinct']:.3f}" if out_["distinct"] else "n/a"
        print(f"  m={m:>5}:  shared retains {s_}   distinct retains {d_}")

    ratios = [(s / d) for _, s, d in verdict_rows if s and d]
    if ratios:
        avg = sum(ratios) / len(ratios)
        print(f"\n  Mean sharing advantage at B=32: {avg:.2f}x")
        print(f"\n{'='*70}\nVERDICT\n{'='*70}")
        if avg > 1.5:
            print(f"  SHARING AMORTIZES ({avg:.2f}x). The residency tax is NOT per-sequence when")
            print("  the cache is shared. n*_shared scales with batch size and the T2 end-to-end")
            print("  obstruction dissolves for multi-tenant same-corpus serving.")
        elif avg > 1.1:
            print(f"  PARTIAL ({avg:.2f}x). Sharing helps but does not fully amortize.")
            print("  n* scales sub-linearly in B. Recompute the crossover with the measured factor.")
        else:
            print(f"  NO AMORTIZATION ({avg:.2f}x). HYPOTHESIS REFUTED.")
            print("  The residency tax is per-sequence regardless of cache provenance.")
            print("  The T2 obstruction stands exactly as published. Stop here.")

    if r.get("delta_batch1"):
        d = r["delta_batch1"]
        print(f"\n{'='*70}\nP4 --- measured residency coefficient at batch 1\n{'='*70}")
        print(f"  delta = {d['ms_per_output_token_per_resident_kv_token']:.3e} ms/out-tok/resident-tok")
        print(f"  t0    = {d['t0_ms']:.2f} ms")
        if d.get("implied_B_eff_GB_s"):
            print(f"  implied effective bandwidth = {d['implied_B_eff_GB_s']:.1f} GB/s")
        print(f"  points (m, ms/token): {d['points']}")

    print(f"\n  Full results -> {out}\n")
