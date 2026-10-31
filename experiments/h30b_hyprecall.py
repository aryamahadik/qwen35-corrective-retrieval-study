"""
H30 --- Can SAMPLED HYPOTHESES beat retrieval on RECALL of the gold definition?

THE REFRAME THAT LED HERE
  Eleven mechanisms attacked SELECTION. The arithmetic says selection is the smaller
  half of the problem:
      P(gold definition in top-8 chunks)  = 0.6046   <- 39.5% MISSING
      oracle | gold present               = 0.5696
      RAG8                                = 0.2628
      headroom from perfect SELECTION     = +12.8pp
      headroom from perfect RECALL        = +30.7pp   <- 2.4x larger
  No selector can recover a gold definition that was never retrieved.

WHY HYPOTHESES MIGHT RETRIEVE BETTER THAN SIMILARITY
  The bug report names the gold symbol only 20.4% of the time, so BM25/dense are
  searching with a query that usually does not contain the target. A model hypothesis
  is different in kind: it IS a symbol name, drawn from the index's own vocabulary, and
  correct 18.3% of the time with ZERO evidence.
  Crucially, resolving a name against the symbol index returns its definition WITH
  CERTAINTY. So candidate-set recall is exactly P(gold in the sampled name set) --
  it composes over samples, with no ranking anywhere in the path.

MEASURED (no answer generation needed -- recall only, which makes this cheap)
  for k in 1,2,4,8,16 :  P(gold in k sampled hypotheses)
    HYP_COLD   sampled with NO evidence          (pure prior)
    HYP_WARM   sampled with the rank-1 chunk     (prior + weak evidence)
  vs RETRIEVAL_TOPK : P(gold definition in top-k chunks), the thing to beat.
  Also reported: UNION of hypotheses and retrieval, since they may be complementary.

PRE-REGISTERED
  WIN   : some k where hypothesis recall > 0.6046 at a comparable token budget
          (each resolved definition is ~250 tok, so k=4 is ~1000 tok vs RAG8's 3399).
  USEFUL: hypotheses below retrieval alone, but the UNION exceeds 0.6046 materially
          -> the two are complementary and should be combined.
  FAIL  : hypothesis recall saturates well below retrieval -> the prior is too weak to
          drive retrieval and the recall ceiling needs a different attack.
  I expect USEFUL, not WIN. A cold prior of 0.183 needs a lot of diversity to reach
  0.60, and sampling the same model repeatedly tends to produce correlated guesses --
  the samples are unlikely to be independent draws. Stating this before the run.

COST: A10G 7B, ~18k short generations (24 tok each) => ~$0.40.
"""
import json, os, re, modal
SEP = "\n\n---\n\n"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h30b-hyprecall")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
K = 16
COLD = ("You are a code maintainer. A bug has been reported.\n\nBUG REPORT:\n{q}\n\n"
        "Which single function or class must be modified to fix this bug?\n"
        "Answer with ONLY the name, nothing else.")   # H24's exact NOCTX wording
WARM = ("You are a maintainer of the Python project `{r}`. A bug has been reported.\n\n"
        "BUG REPORT:\n{q}\n\nRELATED CODE:\n{c}\n\nName the single function or class "
        "most likely to contain this bug.\nAnswer with ONLY the name.")


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def sample(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer()
    sp = SamplingParams(temperature=1.0, top_p=0.95, n=K, max_tokens=16)  # NO seed:
    # a fixed seed returns n IDENTICAL draws (measured 1.00 unique names / 16)
    out = {}
    for tag, mk in (("COLD", lambda it: COLD.format(q=it["query"])),
                    ("WARM", lambda it: WARM.format(r=it["repo"], q=it["query"],
                                                    c=it["chunks"][0][:1800]))):
        chat = [tok.apply_chat_template([{"role": "user", "content": mk(it)}],
                tokenize=False, add_generation_prompt=True) for it in items]
        print(f"[{tag}] {len(chat)} prompts x {K} samples")
        res = llm.generate(chat, sp)
        got = []
        for r in res:
            names = []
            for o in r.outputs:
                m = re.search(r"[A-Za-z_][\w.]*", (o.text or "").replace("`", ""))
                names.append(m.group(0).split(".")[-1] if m else "")
            got.append(names)
        import statistics as _st
        uq = _st.mean(len(set(x)) for x in got)
        print(f"  [{tag}] mean unique names/query = {uq:.2f}/{K}"
              + ("   <-- WARNING: samples are degenerate" if uq < 1.5 else ""))
        out[tag] = got
    hf_cache.commit()
    return {"model": model, "n": n, "samples": out, "K": K}


@app.local_entrypoint()
def main(out: str = "h30b_results.json"):
    r = sample.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json")); N = json.load(open("h24_results.json"))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = r["n"]; null = N["NOCTX"]
    need = [i for i in range(n) if null[i] == 0 and repos[i] not in SMALL]
    import subprocess
    subprocess.run(["./.venv-frontier-modal/bin/modal", "volume", "get", "qcarve-h7-data",
                    "h21_items.json", "/tmp/h21_items.json", "--force"], capture_output=True)
    items = json.load(open("/tmp/h21_items.json"))
    dfn = lambda c, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c))
    S = r["samples"]

    def hyp_recall(tag, k):
        hit = 0
        for i in need:
            names = set(S[tag][i][:k]) - {""}
            if names & set(items[i]["gold"]): hit += 1
        return hit/len(need)

    def ret_recall(k):
        hit = 0
        for i in need:
            if any(dfn(c, g) for c in items[i]["chunks"][:k] for g in items[i]["gold"]):
                hit += 1
        return hit/len(need)

    def union_recall(tag, k, rk):
        hit = 0
        for i in need:
            names = set(S[tag][i][:k]) - {""}
            ok = bool(names & set(items[i]["gold"])) or any(
                dfn(c, g) for c in items[i]["chunks"][:rk] for g in items[i]["gold"])
            if ok: hit += 1
        return hit/len(need)

    print(f"\n{'='*80}\nH30 -- RECALL OF THE GOLD DEFINITION, n={len(need)} evidence-needed\n{'='*80}")
    print(f"  {'k':>3}{'HYP cold':>11}{'HYP warm':>11}{'retrieval':>12}"
          f"{'union(warm,8)':>16}")
    print("-"*80)
    for k in (1, 2, 4, 8, 16):
        print(f"  {k:>3}{hyp_recall('COLD',k):>11.4f}{hyp_recall('WARM',k):>11.4f}"
              f"{ret_recall(min(k,8)):>12.4f}{union_recall('WARM',k,8):>16.4f}")
    r8 = ret_recall(8); bw = max(hyp_recall("WARM", k) for k in (1,2,4,8,16))
    bu = max(union_recall("WARM", k, 8) for k in (1,2,4,8,16))
    print(f"\n  retrieval top-8 recall (the bar) = {r8:.4f}")
    print(f"  best hypothesis-only recall      = {bw:.4f}")
    print(f"  best union recall                = {bu:.4f}   ({(bu-r8)*100:+.1f}pp vs bar)")
    print(f"\n  ceiling if recall were perfect: oracle|gold-present = 0.5696 vs RAG8 0.2628")
    print(f"\n{'='*80}\nVERDICT\n{'='*80}")
    if bw > r8:
        print(f"  WIN -- hypotheses alone out-recall retrieval ({bw:.4f} vs {r8:.4f}).")
    elif bu > r8 + 0.05:
        print(f"  USEFUL -- union {bu:.4f} exceeds retrieval {r8:.4f} by "
              f"{(bu-r8)*100:+.1f}pp; the two signals are COMPLEMENTARY.")
    else:
        print(f"  FAIL -- hypotheses add {(bu-r8)*100:+.1f}pp over retrieval. The prior is")
        print("  too weak, and sampled guesses are too correlated, to drive recall.")
