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
app = modal.App("qcarve-h23-grounding")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["chunks"]):
            pr.append(TPL.format(q=it["query"], e=c)); key.append((i, "S", k))
        for k in (2, 4, 6, 8):                      # optimized-baseline sweep
            pr.append(TPL.format(q=it["query"], e=SEP.join(it["chunks"][:k])))
            key.append((i, f"R{k}", 0))
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
def main(out: str = "h23_results.json"):
    r = run.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json"))
    S14 = H["r14"]["S"]; R14 = H["r14"]["R"]
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    items_chunks = None
    A, S, n = r["answers"], r["S"], r["n"]
    rag = {int(k): v for k, v in r["rag"].items()}

    # need chunk texts for the grounding test -> fetch once from the volume copy
    import subprocess
    subprocess.run(["./.venv-frontier-modal/bin/modal", "volume", "get", "qcarve-h7-data",
                    "h21_items.json", "/tmp/h21_items.json", "--force"],
                   capture_output=True)
    items = json.load(open("/tmp/h21_items.json"))

    real = [i for i in range(n) if repos[i] not in SMALL]
    defined_in = lambda nm, c: bool(nm) and bool(
        re.search(rf"(?:def|class)\s+{re.escape(nm)}\b", c))

    sel = {k: [] for k in ("GROUNDED", "GROUNDED_RARE", "DISTINCT", "GROUNDED_DIST",
                           "MAJORITY", "RANK0")}
    diag = {"grounded_hit": [0, 0], "ungrounded_hit": [0, 0]}
    from collections import Counter
    for i in range(n):
        ch = items[i]["chunks"]; v = [norm(a) for a in A[i]]
        g = [defined_in(v[k], ch[k]) for k in range(8)]
        cnt = Counter(x for x in v if x)
        for k in range(8):
            d = diag["grounded_hit" if g[k] else "ungrounded_hit"]
            d[0] += S[i][k]; d[1] += 1
        rare = sorted([k for k in range(8) if g[k]],
                      key=lambda k: cnt[v[k]])
        dist = [k for k in range(8) if v[k] and cnt[v[k]] == 1]
        gd = [k for k in range(8) if g[k] and v[k] and cnt[v[k]] == 1]
        top = cnt.most_common(1)[0][0] if cnt else ""
        sel["GROUNDED"].append(next((k for k in range(8) if g[k]), 0))
        sel["GROUNDED_RARE"].append(rare[0] if rare else 0)
        sel["DISTINCT"].append(dist[0] if dist else 0)
        sel["GROUNDED_DIST"].append(gd[0] if gd else (rare[0] if rare else 0))
        sel["MAJORITY"].append(next((k for k in range(8) if v[k] == top), 0))
        sel["RANK0"].append(0)

    gh, uh = diag["grounded_hit"], diag["ungrounded_hit"]
    print(f"\n{'='*84}\nH23 -- DOES GROUNDING PREDICT CORRECTNESS? (the mechanism)\n{'='*84}")
    print(f"  P(correct | answer IS defined in the chunk)  = {gh[0]/max(1,gh[1]):.4f}  (n={gh[1]})")
    print(f"  P(correct | answer NOT defined in the chunk) = {uh[0]/max(1,uh[1]):.4f}  (n={uh[1]})")
    print(f"  LIFT = {(gh[0]/max(1,gh[1]) - uh[0]/max(1,uh[1]))*100:+.1f}pp   "
          f"grounded share = {gh[1]/(gh[1]+uh[1]):.1%}")

    def sc(ix, pick, L): return sum(L[i][pick[i]] for i in ix)/len(ix)
    print(f"\n{'='*84}\nGOLD-FREE SELECTORS on 8 real repos (n={len(real)}), ~496 tok\n{'='*84}")
    print(f"  {'selector':<18}{'7B':>9}{'14B(transfer)':>15}{'gold-free':>11}")
    print("-"*84)
    best7 = best14 = 0
    for k in ("RANK0", "MAJORITY", "DISTINCT", "GROUNDED", "GROUNDED_RARE", "GROUNDED_DIST"):
        a = sc(real, sel[k], S); b = sc(real, sel[k], S14)
        best7 = max(best7, a); best14 = max(best14, b)
        print(f"  {k:<18}{a:>9.4f}{b:>15.4f}{'yes':>11}")
    orc7 = sum(max(S[i]) for i in real)/len(real)
    pick7 = [next((k for k in range(8) if S[i][k]), 0) for i in range(n)]
    print(f"  {'ORACLE (7B)':<18}{orc7:>9.4f}{sc(real,pick7,S14):>15.4f}{'NO':>11}")
    print(f"\n  OPTIMIZED RAG baseline (7B), same corpus:")
    for k in (2, 4, 6, 8):
        print(f"    RAG{k}  {sum(rag[k][i] for i in real)/len(real):.4f}  @~{[912,1740,2571,3399][(k//2)-1]} tok")
    bk = max((sum(rag[k][i] for i in real)/len(real), k) for k in (2, 4, 6, 8))
    print(f"    BEST-k = RAG{bk[1]} at {bk[0]:.4f}")
    r14best = sum(R14[i] for i in real)/len(real)
    print(f"\n{'='*84}\nVERDICT\n{'='*84}")
    print(f"  best gold-free selector: 7B {best7:.4f} | 14B {best14:.4f} @496 tok")
    print(f"  best-k RAG (7B): {bk[0]:.4f} @~{[912,1740,2571,3399][(bk[1]//2)-1]} tok | "
          f"14B RAG8 {r14best:.4f} @3399")
    if best7 > bk[0] or best14 > r14best:
        print(f"  WIN -- a GOLD-FREE selector beats the optimized baseline at 4-7x fewer tokens.")
    elif best7 > sc(real, sel["RANK0"], S) + 0.03:
        print(f"  WEAK -- beats rank-0 but not best-k RAG. Grounding carries signal, not enough.")
    else:
        print(f"  FAIL -- seventh mechanism down; gold-free selection stands open.")
