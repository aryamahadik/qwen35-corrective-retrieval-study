"""
H27 --- Explicit VERIFICATION as the selector: just ask the model.

WHY THIS IS DIFFERENT FROM THE NINE THAT FAILED
  Every prior mechanism inferred usefulness IMPLICITLY:
    relevance / rerank / learned features  -> from (query, chunk) similarity
    signatures / self-consistency          -> from answer text patterns
    grounding                              -> from answer-in-chunk syntax
  None ASKED. This poses a direct yes/no about causality, conditioned on a specific
  candidate: "given this bug report and this code, would this function cause it?"
  Verification of a specific claim is usually easier for a model than generation of
  the right one, and it is a strictly narrower question than "which of 8 chunks".

  Grounding is currently the only validated gold-free signal: 0.2143 vs 0.1582 for the
  matched control (McNemar 30/8, p=0.0005), closing 24.2% of the rank-1 -> oracle gap
  (0.1582 -> 0.3903). Beating RAG8 (0.2628) needs 45.1%.

ARMS
  VERIFY        rank chunks by P(yes) from an explicit verification prompt
  VERIFY_GND    verification score, grounded chunks first (combines the two)
  grounding-only and rank-only as references

  Selection is evaluated at k=1 using the EXISTING singleton labels, so no answer
  generation is needed -- only the verification pass itself.

HONEST COST NOTE
  Verification costs 8 extra generations per query on top of the 8 needed for
  grounding. As a same-model pipeline that is far more expensive than RAG8. It is only
  meaningful as a cheap-labeller cascade feeding a larger answerer, and it is reported
  that way.

PRE-REGISTERED
  WIN  : VERIFY or VERIFY_GND >= 0.2628 (RAG8) at ~500 answer tokens.
  GAIN : beats grounding-only (0.2143) -> report the new gap fraction.
  FAIL : <= grounding-only -> asking directly adds nothing; grounding remains the
         only gold-free signal and the 45% target is not reachable with these methods.
  I expect GAIN but not WIN. Verification is a genuinely different question, but H14
  showed this model is weak at chunk-level judgement, and nine mechanisms have failed.
  Stating this before the run.

COST: A10G 7B, ~4500 short generations => ~$0.30.
"""
import json, os, re, modal
SEP = "\n\n---\n\n"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h27-verify")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

VTPL = ("A bug has been reported in a Python project.\n\nBUG REPORT:\n{q}\n\n"
        "CANDIDATE CODE:\n{e}\n\n"
        "Could a defect in THIS code cause the reported bug? "
        "Answer with exactly one word: YES or NO.")


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def verify(answers, model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer()
    # logprobs so we get a CONTINUOUS score, not just a yes/no bit
    sp = SamplingParams(temperature=0.0, max_tokens=3, logprobs=20)
    pr, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["chunks"]):
            pr.append(VTPL.format(q=it["query"], e=c)); key.append((i, k))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in pr]
    print(f"[plan] {len(chat)} verification generations")
    res = llm.generate(chat, sp)
    import math
    score = [[0.0]*8 for _ in range(n)]
    said = [[""]*8 for _ in range(n)]
    for (i, k), r in zip(key, res):
        txt = r.outputs[0].text.strip()
        said[i][k] = txt[:6]
        p_yes = 0.0
        try:
            lp = r.outputs[0].logprobs[0]
            for tid, obj in lp.items():
                t = (obj.decoded_token if hasattr(obj, "decoded_token") else str(obj)).strip().upper()
                if t.startswith("YES"):
                    p_yes = max(p_yes, math.exp(obj.logprob))
        except Exception:
            pass
        if p_yes == 0.0:
            p_yes = 1.0 if txt.upper().startswith("YES") else 0.0
        score[i][k] = float(p_yes)
    hf_cache.commit()
    return {"model": model, "n": n, "p_yes": score, "said": said}


@app.local_entrypoint()
def main(out: str = "h27_results.json"):
    H = json.load(open("h21_results.json")); H23 = json.load(open("h23_results.json"))
    N = json.load(open("h24_results.json"))
    r = verify.remote(H23["answers"]); json.dump(r, open(out, "w"), indent=2)
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = r["n"]; S7 = H["r7"]["S"]; null = N["NOCTX"]; A = H23["answers"]
    need = [i for i in range(n) if null[i] == 0 and repos[i] not in SMALL]
    import subprocess
    subprocess.run(["./.venv-frontier-modal/bin/modal", "volume", "get", "qcarve-h7-data",
                    "h21_items.json", "/tmp/h21_items.json", "--force"], capture_output=True)
    items = json.load(open("/tmp/h21_items.json"))
    norm = lambda t: (re.search(r"[A-Za-z_][\w.]*", (t or "").replace("`", "")).group(0)
                      .split(".")[-1] if re.search(r"[A-Za-z_][\w.]*",
                      (t or "").replace("`", "")) else "")
    P = r["p_yes"]
    def gnd(i):
        ch = items[i]["chunks"]; v = [norm(a) for a in A[i]]
        return [1 if v[k] and re.search(rf"(?:def|class)\s+{re.escape(v[k])}\b", ch[k]) else 0
                for k in range(8)]
    def sel(fn):
        return sum(S7[i][max(range(8), key=lambda k: fn(i, k))] for i in need)/len(need)
    base = sel(lambda i, k: -k)
    orc = sum(max(S7[i]) for i in need)/len(need)
    res = {
        "rank_only": base,
        "grounding_only": sel(lambda i, k: gnd(i)[k]*10 - k*0.1),
        "VERIFY": sel(lambda i, k: P[i][k] - k*1e-3),
        "VERIFY_GND": sel(lambda i, k: gnd(i)[k]*10 + P[i][k] - k*1e-3),
    }
    yes = sum(1 for i in need for k in range(8) if P[i][k] > 0.5)
    print(f"\n{'='*70}\nH27 -- EXPLICIT VERIFICATION, n={len(need)} evidence-needed\n{'='*70}")
    print(f"  verifier said YES on {yes}/{len(need)*8} = {yes/(len(need)*8):.1%} of chunks")
    print(f"\n  {'selector':<20}{'score':>9}{'gap closed':>13}")
    print("-"*70)
    for k in ("rank_only", "grounding_only", "VERIFY", "VERIFY_GND"):
        print(f"  {k:<20}{res[k]:>9.4f}{(res[k]-base)/(orc-base):>12.1%}")
    print(f"  {'RAG8 @3399':<20}{0.2628:>9.4f}{(0.2628-base)/(orc-base):>12.1%}")
    print(f"  {'ORACLE':<20}{orc:>9.4f}{100.0:>12.1f}%")
    best = max(res["VERIFY"], res["VERIFY_GND"])
    print(f"\n{'='*70}\nVERDICT\n{'='*70}")
    if best >= 0.2628:
        print(f"  WIN -- verification reaches {best:.4f} >= RAG8, at 6.6x fewer answer tokens.")
    elif best > res["grounding_only"] + 0.01:
        print(f"  GAIN -- {best:.4f} beats grounding-only ({res['grounding_only']:.4f}).")
    else:
        print(f"  FAIL -- {best:.4f} does not beat grounding-only "
              f"({res['grounding_only']:.4f}). Asking directly adds nothing.")
