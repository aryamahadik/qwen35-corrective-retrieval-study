"""
H12 --- Does an <=850-token context that preserves RAG8 quality EXIST AT ALL?

Every experiment so far tested SELECTORS. None established there is anything to
select. This is the prior question, and it yields a binary research fork:

  S_oracle,850 >= S_RAG8 - 0.01  -> 4x exists; SELECTION is the breakthrough problem
  S_oracle,850 <<  S_RAG8        -> 4x selection-only compression is structurally dead,
                                    and a new INFORMATION SOURCE is required

METHOD
  Start from the exact 8 chunks RAG8 already returned (identical items, verified
  byte-identical to H7/H9/H11). Enumerate every subset whose full prompt is <=850
  tokens. Run the same model, same template, same scorer. Take the BEST result per
  query after seeing it. This is intentionally an ORACLE UPPER BOUND: no real
  selector can beat it, so failure here forecloses reranking, AST routing,
  confidence models and threshold tuning in one shot.

THE CONFOUND I AM CONTROLLING (not in the original spec)
  Best-of-N over ~30 subsets is ~30 chances to guess. At a ~33% base rate that
  manufactures hits from useless context. So a matched CHANCE FLOOR runs the same
  number of subsets, same budget, but with chunks taken from a DIFFERENT query's
  RAG8 set. ORACLE minus CHANCE is the real signal; ORACLE alone is not
  interpretable.

PRE-REGISTERED
  PASS  : S_oracle,850 >= S_RAG8 - 0.01 AND S_oracle,850 > S_chance,850 (McNemar p<0.05)
  FAIL  : S_oracle,850 < S_RAG8 - 0.01
  VOID  : S_oracle,850 ~ S_chance,850  -> the oracle is guessing inflation, test is
          uninformative and must be redesigned with a stricter scorer.
  I expect PASS. Dropping 6 distractor chunks should HELP a model that is already
  monotone-improving in evidence, and RAG8's own misses cap both arms equally.
  Stating this before the run.

COST: A10G, 7B (highest absolute accuracy of the three scales, cheapest to run),
prefix caching ON since all subsets of a query share the prompt prefix. ~$1.30.
"""
import json, re, modal
from itertools import combinations

BUDGET = 850
MODEL = "Qwen/Qwen2.5-7B-Instruct"
SEP = "\n\n---\n\n"

llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h12-oracle")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def oracle(budget=BUDGET, model=MODEL):
    import os; os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h7_items.json"))
    n = len(items)
    bad = sum(1 for it in items if len(it["RAG8"].split(SEP)) != 8)
    print(f"[integrity] RAG8 not splitting into exactly 8 chunks: {bad}/{n}")

    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer()
    sp = SamplingParams(temperature=0.0, max_tokens=24)
    nt = lambda q, e: len(tok(TPL.format(q=q, e=e))["input_ids"])

    # ---- enumerate qualifying subsets per query -------------------------------
    plan = []          # (query_idx, arm, subset_tuple, evidence_text, n_tok)
    counts = []
    for i, it in enumerate(items):
        ch = it["RAG8"].split(SEP)
        alt = items[(i + 120) % n]["RAG8"].split(SEP)     # chance floor: other query
        keep = []
        for r in (1, 2, 3):
            for c in combinations(range(8), r):
                ev = SEP.join(ch[j] for j in c)
                t = nt(it["query"], ev)
                if t <= budget:
                    keep.append((c, ev, t))
            if r == 1 and not keep:
                break                                      # even 1 chunk overflows
        counts.append(len(keep))
        for c, ev, t in keep:
            plan.append((i, "ORACLE", c, ev, t))
        # matched chance floor: SAME subset shapes, irrelevant chunks
        for c, _, _ in keep:
            ev2 = SEP.join(alt[j] for j in c)
            plan.append((i, "CHANCE", c, ev2, nt(it["query"], ev2)))
        # reference arm, unconstrained
        plan.append((i, "RAG8", tuple(range(8)), it["RAG8"], nt(it["query"], it["RAG8"])))

    import numpy as np
    print(f"[plan] {len(plan)} generations | qualifying subsets/query: "
          f"min={min(counts)} median={int(np.median(counts))} max={max(counts)} "
          f"zero={sum(1 for c in counts if c==0)}")

    prompts = [tok.apply_chat_template(
        [{"role": "user", "content": TPL.format(q=items[i]["query"], e=ev)}],
        tokenize=False, add_generation_prompt=True) for i, _, _, ev, _ in plan]
    res = llm.generate(prompts, sp)

    recs = []
    for (i, arm, c, _, t), r in zip(plan, res):
        txt = r.outputs[0].text
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", txt) for g in items[i]["gold"]))
        recs.append({"i": i, "arm": arm, "subset": list(c), "n_tok": t, "hit": hit,
                     "repo": items[i]["repo"]})
    hf_cache.commit()
    return {"model": model, "budget": budget, "n_items": n,
            "subset_counts": counts, "records": recs}


@app.local_entrypoint()
def main(out: str = "h12_results.json"):
    r = oracle.remote()
    json.dump(r, open(out, "w"), indent=2)
    n = r["n_items"]; R = r["records"]
    from math import comb

    def best_of(arm):
        per = {}
        for x in R:
            if x["arm"] == arm:
                per[x["i"]] = max(per.get(x["i"], 0), x["hit"])
        return per
    orc, chc = best_of("ORACLE"), best_of("CHANCE")
    rag = {x["i"]: x["hit"] for x in R if x["arm"] == "RAG8"}
    cover = [i for i in range(n) if i in orc]          # queries with >=1 valid subset

    S_rag = sum(rag.values()) / n
    S_orc = sum(orc.get(i, 0) for i in range(n)) / n
    S_chc = sum(chc.get(i, 0) for i in range(n)) / n
    toks = [x["n_tok"] for x in R if x["arm"] == "ORACLE"]
    rag_tok = sum(x["n_tok"] for x in R if x["arm"] == "RAG8") / n

    print(f"\n{'='*82}\nH12 ORACLE MINIMAL SUFFICIENT CONTEXT  (budget <= {r['budget']} tok)\n{'='*82}")
    print(f"  queries                              : {n}")
    print(f"  queries with >=1 qualifying subset   : {len(cover)} ({len(cover)/n:.1%})")
    print(f"  mean subset prompt tokens            : {sum(toks)/len(toks):.0f}")
    print(f"  RAG8 prompt tokens                   : {rag_tok:.0f}  "
          f"({rag_tok/(sum(toks)/len(toks)):.2f}x compression)\n")
    print(f"  S_RAG8        = {S_rag:.4f}")
    print(f"  S_oracle,{r['budget']}  = {S_orc:.4f}   ({(S_orc-S_rag)*100:+.1f}pp vs RAG8)")
    print(f"  S_chance,{r['budget']}  = {S_chc:.4f}   <- best-of-N guessing floor")
    print(f"  ORACLE - CHANCE = {(S_orc-S_chc)*100:+.1f}pp   <- the only interpretable signal")

    f = [orc.get(i, 0) for i in range(n)]; g = [chc.get(i, 0) for i in range(n)]
    b = sum(1 for x, y in zip(f, g) if x and not y); c = sum(1 for x, y in zip(f, g) if y and not x)
    m = b + c; k = min(b, c)
    p = min(1.0, 2*sum(comb(m, j) for j in range(k+1))/2**m) if m else 1.0
    print(f"  McNemar oracle vs chance: {b} / {c} discordant, p={p:.2e}")

    print(f"\n{'='*82}\nVERDICT\n{'='*82}")
    if S_orc - S_chc < 0.02 or p >= 0.05:
        print("  VOID -- the oracle is indistinguishable from best-of-N guessing.")
        print("  The test cannot answer the question as scored. Redesign before spending more.")
    elif S_orc >= S_rag - 0.01:
        print(f"  PASS -- an <={r['budget']}-token subset preserving RAG8 quality EXISTS.")
        print(f"  4x compression is possible in principle. The breakthrough problem is")
        print(f"  SET-LEVEL SELECTION (H13: learn U(Q,S), exploit complementarity).")
        print(f"  Headroom a perfect selector would unlock: {(S_orc-0.3292)*100:+.1f}pp over RAG2.")
    else:
        print(f"  FAIL -- even the ORACLE loses {(S_rag-S_orc)*100:.1f}pp at <={r['budget']} tokens.")
        print("  No reranker, AST router, confidence model or threshold can reach 4x by")
        print("  SELECTING from RAG8's chunks. Selection-only compression is structurally")
        print("  dead. A new INFORMATION SOURCE is required (execution traces, H14).")

    print(f"\n  per-repo S_oracle / S_RAG8 / S_chance:")
    for rp in sorted({x["repo"] for x in R}):
        ix = sorted({x["i"] for x in R if x["repo"] == rp})
        print(f"    {rp:<7} n={len(ix):<4} "
              f"{sum(orc.get(i,0) for i in ix)/len(ix):.3f} / "
              f"{sum(rag.get(i,0) for i in ix)/len(ix):.3f} / "
              f"{sum(chc.get(i,0) for i in ix)/len(ix):.3f}")
