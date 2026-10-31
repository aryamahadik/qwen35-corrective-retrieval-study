"""
H23 --- GOLD-FREE SELECTION via output-evidence GROUNDING.

THE INVERSION
  Six failed mechanisms all predicted utility from (query, chunk): dense relevance,
  cross-encoder rerank, learned utility features, LLM-over-signatures, rank order,
  and self-consistency. The first five are views of the same text similarity that H12
  showed is nearly orthogonal to utility (rank-0 lift only +4.9pp).

  This treats the model's ANSWER as a measurement OF the chunk. Given chunk C the
  model names symbol A. Then ask a purely syntactic, gold-free question:
      is A actually DEFINED in C?
  A in C  -> the model READ the evidence (grounded).
  A not in C -> the model guessed from priors, ignoring C (ungrounded).

  Why it should work: H12 measured P(correct | chunk defines gold) = 0.819 vs 0.196.
  If the right chunk is present the model names the right symbol -- and that symbol is
  BY CONSTRUCTION defined in that chunk. So grounded => likely correct, no gold needed.

SECOND INVERSION
  H16 tested majority vote (consensus = correct) and got nothing above RAG2. The
  OPPOSITE may hold: a DISTINCTIVE answer, produced by only one chunk, is
  evidence-driven; a repeated answer is the model's prior leaking through. Consensus
  was measured; its inverse never was.

GOLD-FREE SELECTORS (decided only from the 8 answer strings + the 8 chunk texts)
  GROUNDED      first chunk whose answer is DEFINED in it
  GROUNDED_RARE grounded, tie-broken toward answers rare in the repo
  DISTINCT      chunk whose answer no other chunk produced
  GROUNDED_DIST grounded AND distinct
  MAJORITY      (H16 baseline, for direct comparison)

HONEST BASELINE -- addressing a real criticism
  My RAG8 baseline is NOT optimized. H9 showed RAG6 (0.4000) beat RAG8 (0.3958) at 7B.
  So this run also measures RAG at k=2,4,6,8 on the H21 corpus and compares every
  selector against the BEST-k baseline, not the convenient one.

PRE-REGISTERED
  WIN  : some gold-free selector beats BEST-k RAG at ~496 tok (vs ~3400), and the
         advantage TRANSFERS to 14B.
  WEAK : beats rank-0 (~0.32) but not best-k RAG.
  FAIL : <= rank-0 -> grounding carries no selection signal either; seventh mechanism
         down, and the gold-free selection problem stands open.
  I expect WEAK-to-WIN for GROUNDED. The 0.819-vs-0.196 statistic is the strongest
  signal measured all session and grounding is a direct, exact proxy for it.
  Stating this before the run.

COST: A10G 7B, ~6700 generations => ~$0.40.
"""
import json, os, re, modal
SEP = "\n\n---\n\n"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h28-gnd32")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A100-80GB", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(model="Qwen/Qwen2.5-32B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.95, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["chunks"]):
            pr.append(TPL.format(q=it["query"], e=c)); key.append((i, "S", k))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in pr]
    print(f"[plan] {len(chat)} generations")
    res = llm.generate(chat, sp)
    ans = [[""]*8 for _ in range(n)]
    rag = {k: [0]*n for k in (2, 4, 6, 8)}
    S = [[0]*8 for _ in range(n)]
    for (i, arm, k), r in zip(key, res):
        t = r.outputs[0].text.strip()
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", t) for g in items[i]["gold"]))
        if arm == "S":
            ans[i][k] = t; S[i][k] = hit
        else:
            rag[int(arm[1:])][i] = hit
    hf_cache.commit()
    return {"model": model, "n": n, "answers": ans, "S": S,
            "rag": {str(k): v for k, v in rag.items()}}


def norm(t):
    m = re.search(r"[A-Za-z_][\w.]*", (t or "").replace("`", ""))
    return m.group(0).split(".")[-1] if m else ""


@app.local_entrypoint()
def main(out: str = "h28_results.json"):
    r = run.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json")); H22 = json.load(open("h22_results.json"))
    H23 = json.load(open("h23_results.json")); N = json.load(open("h24_results.json"))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = r["n"]; null = N["NOCTX"]
    S7 = H["r7"]["S"]; S32 = H22["S"]
    need = [i for i in range(n) if null[i] == 0 and repos[i] not in SMALL]
    import subprocess
    subprocess.run(["./.venv-frontier-modal/bin/modal", "volume", "get", "qcarve-h7-data",
                    "h21_items.json", "/tmp/h21_items.json", "--force"], capture_output=True)
    items = json.load(open("/tmp/h21_items.json"))
    def gnd(ans, i):
        ch = items[i]["chunks"]; v = [norm(a) for a in ans[i]]
        return [1 if v[k] and re.search(rf"(?:def|class)\s+{re.escape(v[k])}\b", ch[k]) else 0
                for k in range(8)]
    def sel(fn, L):
        return sum(L[i][max(range(8), key=lambda k: fn(i, k))] for i in need)/len(need)
    rows = []
    for lab, ans, L in (("7B grounding -> 7B", H23["answers"], S7),
                        ("32B grounding -> 32B", r["answers"], S32),
                        ("7B grounding -> 32B", H23["answers"], S32),
                        ("32B grounding -> 7B", r["answers"], S7)):
        base = sel(lambda i, k: -k, L)
        orc = sum(max(L[i]) for i in need)/len(need)
        g = sel(lambda i, k: gnd(ans, i)[k]*10 - k*0.1, L)
        rows.append((lab, base, g, orc, (g-base)/(orc-base)))
    print(f"\n{'='*78}\nH28 -- DOES THE GROUNDING SIGNAL IMPROVE WITH LABELLER STRENGTH?")
    print(f"        n={len(need)} evidence-needed queries\n{'='*78}")
    print(f"  {'pipeline':<24}{'rank-1':>9}{'grounded':>10}{'oracle':>9}{'gap closed':>13}")
    print("-"*78)
    for lab, b, g, o, f in rows:
        print(f"  {lab:<24}{b:>9.4f}{g:>10.4f}{o:>9.4f}{f:>12.1%}")
    g7 = rows[0][4]; g32 = rows[1][4]
    print(f"\n  RAG8 reference: 7B 0.2628 @3399 tok | 32B {sum(H22['R'][i] for i in need)/len(need):.4f}")
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if g32 > g7 + 0.05:
        print(f"  SCALES -- grounding closes {g32:.1%} with a 32B labeller vs {g7:.1%} with 7B.")
        print("  The signal improves with labeller strength; the cascade has a scaling path.")
    elif g32 > g7:
        print(f"  MARGINAL -- {g32:.1%} vs {g7:.1%}. Slight improvement, not a clear path.")
    else:
        print(f"  CAPPED -- {g32:.1%} vs {g7:.1%}. A stronger labeller does NOT produce a")
        print("  better grounding signal. ~24% is what this mechanism buys, full stop.")
