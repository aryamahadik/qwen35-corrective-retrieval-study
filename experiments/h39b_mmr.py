"""
H39 --- Is CONVERSION lost to CONFUSABILITY? Diversify the candidate set and see.

THE MEASURED PUZZLE
    arm     recall   accuracy  conversion
    RAG8    0.6046   0.2628    43.5%      8 chunks, ~24 functions
    DEF8    0.6505   0.1607    24.7%      8 definitions, 8 functions
    DEF12   0.6964   0.1480    21.2%
  Definitions RETRIEVE BETTER and ANSWER WORSE. Fewer candidate functions, worse
  conversion -- so it is not the NUMBER of alternatives. H31 also rules out
  "uniqueness": gold alone 0.5486 vs gold + 7 chunk distractors 0.5278, only -2.1pp.

THE HYPOTHESIS THIS TESTS
  Similarity retrieval returns items similar TO EACH OTHER, not merely to the query.
  A set of k near-duplicates is maximally confusable; a heterogeneous set is not.
  Whole definitions are self-consistent and mutually interchangeable-looking; ragged
  chunks are not. If CONFUSABILITY drives the conversion loss, then diversifying the
  set at IDENTICAL k and IDENTICAL token budget should RAISE conversion.

  Nothing in this session has manipulated diversity. Every arm ranked by score alone.

METHOD -- Maximal Marginal Relevance over the same candidates
    MMR(d) = lambda * rel(d, q) - (1 - lambda) * max_{s in S} sim(d, s)
  lambda = 1.0 is pure relevance (the incumbent); lower lambda trades relevance for
  dissimilarity from already-selected items. Same corpus, same k, same tokens --
  only the ORDER of selection changes.

ARMS (chunks, k=8, so directly comparable to RAG8 = 0.2628 @3399)
  MMR100  lambda=1.0  pure relevance (reproduces the incumbent; sanity check)
  MMR70   lambda=0.7
  MMR50   lambda=0.5
  MMR30   lambda=0.3  aggressive diversity
  Recall is reported alongside accuracy so conversion can be computed directly:
  diversity should COST recall and, if the hypothesis holds, BUY more conversion.

PRE-REGISTERED
  WIN  : some lambda < 1.0 beats RAG8 accuracy at k=8 AND shows higher conversion.
  MECH : conversion rises with diversity even if accuracy does not (recall loss
         cancels it) -> confusability confirmed as the mechanism, pointing at
         diversity-aware retrieval as the lever.
  FAIL : conversion flat or falling as diversity rises -> confusability is not the
         mechanism, and the conversion ceiling has a different cause entirely.
  I expect MECH rather than WIN: diversity should help conversion but cost recall,
  and which dominates at k=8 is unknown. Stating this before the run.

COST: A10G embed + 7B answer, ~$0.40.
"""
import json, os, re, subprocess, modal
SEP = "\n\n---\n\n"
CHUNK_TOK, APPROX, EXCL = 512, 0.27, ("test", "tests", "vendor", "docs")
EMB = "BAAI/bge-small-en-v1.5"
REPOS = {"flask": "pallets/flask", "httpx": "encode/httpx", "click": "pallets/click",
         "requests": "psf/requests", "jinja": "pallets/jinja",
         "werkzeug": "pallets/werkzeug", "attrs": "python-attrs/attrs",
         "urllib3": "urllib3/urllib3"}
emb_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h39b-mmr")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")
LAMBDAS = [("MMR100", 1.0), ("MMR70", 0.7), ("MMR50", 0.5), ("MMR30", 0.3)]


@app.function(image=emb_image, gpu="A100-40GB", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def build():
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    items = json.load(open("/data/h21_items.json"))
    m = SentenceTransformer(EMB, device="cuda")
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    idx = {}
    for nm, slug in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                            "https://github.com/"+slug, d], capture_output=True)
        files = [p for p in subprocess.run(["git", "ls-files"], cwd=d, capture_output=True,
                 text=True).stdout.split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        ch = []; nch = int(CHUNK_TOK/APPROX)
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for i in range(0, len(s), nch): ch.append(s[i:i+nch])
        if len(ch) < 8: continue
        E = m.encode(ch, batch_size=128, normalize_embeddings=True,
                     convert_to_numpy=True, show_progress_bar=False)
        idx[nm] = (ch, E, BM25Okapi([tk(c) for c in ch]))
        print(f"  {nm}: {len(ch)} chunks")
    out = []
    for it in items:
        nm = it["repo"]
        if nm not in idx: out.append(None); continue
        ch, E, bm = idx[nm]
        qv = m.encode([it["query"]], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = [int(x) for x in np.argsort(-(E @ qv))]
        br = [int(x) for x in np.argsort(-bm.get_scores(tk(it["query"])))]
        sc = {}
        for r_, j in enumerate(dr[:200]): sc[j] = sc.get(j, 0) + 1/(60+r_+1)
        for r_, j in enumerate(br[:200]): sc[j] = sc.get(j, 0) + 1/(60+r_+1)
        pool = [int(j) for j in sorted(sc, key=lambda j: -sc[j])[:40]]
        rel = {j: float(sc[j]) for j in pool}
        mx = max(rel.values()) or 1.0
        arms = {}
        for tag, lam in LAMBDAS:
            sel = []
            cand = list(pool)
            while cand and len(sel) < 8:
                best, bv = None, -9e9
                for j in cand:
                    div = max((float(E[j] @ E[s]) for s in sel), default=0.0)
                    v = lam*(rel[j]/mx) - (1-lam)*div
                    if v > bv: best, bv = j, v
                sel.append(best); cand.remove(best)
            arms[tag] = [int(j) for j in sel]
        out.append({t: {"text": SEP.join(ch[j] for j in v), "idx": v} for t, v in arms.items()})
    json.dump(out, open("/data/h39b_ctx.json", "w")); data_vol.commit(); hf_cache.commit()
    return {"n": sum(1 for x in out if x)}


@app.function(image=llm_image, gpu="A100-40GB", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def answer(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json"))
    ctx = json.load(open("/data/h39b_ctx.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.90, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key, nt = [], [], []
    for i, it in enumerate(items):
        c = ctx[i]
        if not c: continue
        for tag, _ in LAMBDAS:
            body = TPL.format(q=it["query"], e=c[tag]["text"])
            pr.append(body); key.append((i, tag)); nt.append(len(tok(body)["input_ids"]))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
            add_generation_prompt=True) for p in pr]
    print(f"[plan] {len(chat)} generations")
    res = llm.generate(chat, sp)
    out = {}
    for (i, tag), r, t in zip(key, res, nt):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in items[i]["gold"]))
        out.setdefault(tag, []).append((i, hit, t))
    hf_cache.commit()
    return out


@app.local_entrypoint()
def main(out: str = "h39b_results.json"):
    b = build.remote(); print(f"  contexts for {b['n']} items")
    r = answer.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json")); N = json.load(open("h24_results.json"))
    items = json.load(open("/tmp/h21_items.json"))
    ctxf = "/tmp/h39_ctx.json"
    subprocess.run(["./.venv-frontier-modal/bin/modal", "volume", "get", "qcarve-h7-data",
                    "h39b_ctx.json", ctxf, "--force"], capture_output=True)
    ctx = json.load(open(ctxf))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = H["r7"]["n"]; null = N["NOCTX"]; P7 = H["r7"]["R"]
    real = set(i for i in range(n) if repos[i] not in SMALL)
    need = [i for i in real if null[i] == 0]
    dfn = lambda c, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c))
    print(f"\n{'='*76}\nH39 -- DIVERSITY vs CONFUSABILITY (chunks, k=8, n={len(need)})\n{'='*76}")
    print(f"  {'arm':<9}{'lambda':>8}{'recall':>9}{'accuracy':>10}{'conversion':>12}{'tokens':>8}")
    print("-"*76)
    res = {}
    for tag, lam in LAMBDAS:
        v = [x for x in r[tag] if x[0] in set(need)]
        acc = sum(h for _, h, _ in v)/len(v)
        rec = sum(1 for i, _, _ in v
                  if any(dfn(items[i]["chunks"][0] if False else t, g)
                         for t in ctx[i][tag]["text"].split(SEP) for g in items[i]["gold"]))/len(v)
        t = sum(t for _, _, t in v)/len(v)
        res[tag] = (rec, acc, acc/max(rec, 1e-9))
        print(f"  {tag:<9}{lam:>8.1f}{rec:>9.4f}{acc:>10.4f}{acc/max(rec,1e-9):>11.1%}{t:>8.0f}")
    r8 = sum(P7[i] for i in need)/len(need)
    print(f"  {'RAG8':<9}{'--':>8}{0.6046:>9.4f}{r8:>10.4f}{r8/0.6046:>11.1%}{3399:>8}")
    c100, c30 = res["MMR100"][2], res["MMR30"][2]
    a100, a30 = res["MMR100"][1], res["MMR30"][1]
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    print(f"  conversion at lambda=1.0 -> 0.3 : {c100:.1%} -> {c30:.1%} ({(c30-c100)*100:+.1f}pp)")
    if max(a for _, a, _ in res.values()) > r8:
        print(f"  WIN -- diversified retrieval beats RAG8 at the same k and tokens.")
    elif c30 > c100 + 0.03:
        print(f"  MECH -- conversion RISES with diversity: confusability is the mechanism.")
        print("  Diversity-aware retrieval is the lever; recall loss currently cancels it.")
    else:
        print(f"  FAIL -- conversion does not rise with diversity. Confusability is not")
        print("  the cause, and the conversion ceiling has a different explanation.")
