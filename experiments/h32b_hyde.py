"""
H32 --- Fix the VOCABULARY MISMATCH: retrieve with generated CODE, not with the report.

THE DIAGNOSIS
  H31 proved by intervention that finding gold's definition is worth +28pp:
      gold-absent queries: RAG8 0.0452 @3399 tok  ->  gold definition alone 0.5486 @349 tok
  Retrieval recall is 0.6046 and the bug report names the gold symbol only 20.4% of
  the time. BM25/dense are matching a SYMPTOM DESCRIPTION against IMPLEMENTATION CODE.
  "sessions aren't persisted across requests" shares almost no tokens with
  `def save_session(self, app, session, response)`. Different vocabularies.

WHY NOT GENERATE NAMES (H29/H30)
  Names are brittle: one wrong character resolves to nothing, 7.0% of gold symbols are
  absent from the index, 36.2% are ambiguous, and H30b shows the model emits only
  ~4.6 DISTINCT names in 16 samples. H29 died exactly here -- it invented
  `FlaskynamoDbInstanceFolderCreator`, which resolves to nothing.

THE MECHANISM
  Have the model WRITE the function it believes is buggy -- a plausible implementation,
  not a label -- then retrieve with that as the query. Code-vs-code matching, one
  vocabulary. It degrades gracefully: a 60%-correct hypothetical function still embeds
  near the real one, whereas a 90%-correct NAME resolves to nothing.

ARMS (all measured as gold-DEFINITION recall at top-8, the deployable quantity)
  REPORT    retrieve with the bug report          (baseline, 0.6046)
  HYDE      retrieve with the generated function
  RRF       reciprocal-rank fusion of both        (complementarity test)
  UNION     set union of the two top-8 sets       (upper bound on fusion, 16 chunks)

PRE-REGISTERED
  WIN    : HYDE or RRF recall >= 0.70 at top-8 (same candidate budget as baseline).
  USEFUL : RRF/UNION materially above 0.6046 while HYDE alone is below -> the signals
           are complementary and should be fused.
  FAIL   : neither exceeds 0.6046 meaningfully -> generated code is not a better query
           and the vocabulary-mismatch diagnosis is wrong.
  I expect USEFUL. HyDE is known to help when query and corpus vocabularies differ,
  which is exactly the measured condition here -- but the model must already half-know
  the implementation to write a useful hypothetical, and H24 put its cold prior at
  18.3%. Stating this before the run.

COST: A10G generation + A10G embedding => ~$0.40.
"""
import json, os, re, modal
SEP = "\n\n---\n\n"
EMB_MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_TOK, APPROX, TOP_K = 512, 0.27, 8
REPOS = {"flask": "pallets/flask", "httpx": "encode/httpx", "click": "pallets/click",
         "requests": "psf/requests", "jinja": "pallets/jinja",
         "werkzeug": "pallets/werkzeug", "attrs": "python-attrs/attrs",
         "urllib3": "urllib3/urllib3"}
EXCL = ("test", "tests", "vendor", "docs")

llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
emb_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
app = modal.App("qcarve-h32b-hyde")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

HYDE = ("You are a maintainer of the Python project `{r}`. A bug has been reported.\n\n"
        "BUG REPORT:\n{q}\n\n"
        "Write the Python function or method you believe contains this bug, as it would "
        "most plausibly appear in the `{r}` source code. Include the def line, the "
        "signature, a docstring, and a realistic body. Output ONLY code.")


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def generate_unused(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer()
    sp = SamplingParams(temperature=0.3, top_p=0.95, max_tokens=320)
    chat = [tok.apply_chat_template(
        [{"role": "user", "content": HYDE.format(r=it["repo"], q=it["query"])}],
        tokenize=False, add_generation_prompt=True) for it in items]
    print(f"[hyde] {len(chat)} hypothetical functions")
    docs = [o.outputs[0].text.strip() for o in llm.generate(chat, sp)]
    json.dump(docs, open("/data/h32_hyde_docs.json", "w")); data_vol.commit()
    import statistics as st
    print(f"  mean length {st.mean(len(d) for d in docs):.0f} chars; "
          f"{sum(1 for d in docs if 'def ' in d or 'class ' in d)}/{len(docs)} contain a def/class")
    return {"n": len(docs), "sample": docs[0][:400]}


@app.function(image=emb_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def evaluate():
    os.environ["HF_HOME"] = "/hf"
    import numpy as np, subprocess
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    items = json.load(open("/data/h21_items.json"))
    docs = json.load(open("/data/h32_hyde_docs.json"))
    emb = SentenceTransformer(EMB_MODEL, device="cuda")
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    dfn = lambda c, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c))
    byrepo = {}
    for nm, slug in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                            "https://github.com/" + slug, d], capture_output=True)
        files = [p for p in subprocess.run(["git", "ls-files"], cwd=d, capture_output=True,
                 text=True).stdout.split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        ch = []
        nch = int(CHUNK_TOK/APPROX)
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for i in range(0, len(s), nch): ch.append(s[i:i+nch])
        if len(ch) < 8: continue
        E = emb.encode(ch, batch_size=256, normalize_embeddings=True,
                       convert_to_numpy=True, show_progress_bar=False)
        byrepo[nm] = (ch, E, BM25Okapi([tk(c) for c in ch]))
        print(f"  {nm}: {len(ch)} chunks")

    def topk(nm, q, k=TOP_K, kk=60):
        ch, E, bm = byrepo[nm]
        qv = emb.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = np.argsort(-(E @ qv)); br = np.argsort(-bm.get_scores(tk(q)))
        sc = {}
        for r_, i in enumerate(dr[:200]): sc[i] = sc.get(i, 0) + 1/(kk+r_+1)
        for r_, i in enumerate(br[:200]): sc[i] = sc.get(i, 0) + 1/(kk+r_+1)
        return sorted(sc, key=lambda i: -sc[i])[:k], sc

    KS = (4, 8, 12, 16)
    res = {f"{a}@{k}": 0 for a in ("REPORT", "HYDE", "RRF") for k in KS}
    res.update({"UNION@16(8+8)": 0, "n": 0})
    for i, it in enumerate(items):
        nm = it["repo"]
        if nm not in byrepo: continue
        ch = byrepo[nm][0]; gold = it["gold"]; res["n"] += 1
        hit = lambda idx: any(dfn(ch[j], g) for j in idx for g in gold)
        _, sr = topk(nm, it["query"], k=1)
        _, sh = topk(nm, docs[i] if docs[i].strip() else it["query"], k=1)
        rr = sorted(sr, key=lambda j: -sr[j]); hh = sorted(sh, key=lambda j: -sh[j])
        fu = sorted(set(sr) | set(sh), key=lambda j: -(sr.get(j, 0) + sh.get(j, 0)))
        for k in KS:
            res[f"REPORT@{k}"] += hit(rr[:k]); res[f"HYDE@{k}"] += hit(hh[:k])
            res[f"RRF@{k}"] += hit(fu[:k])
        res["UNION@16(8+8)"] += hit(list(set(rr[:8]) | set(hh[:8])))
    hf_cache.commit()
    return res


@app.local_entrypoint()
def main(out: str = "h32b_results.json"):
    g = {"cached": True}
    r = evaluate.remote(); json.dump({"eval": r}, open(out, "w"), indent=2)
    n = r["n"]
    H = json.load(open("h21_results.json")); N = json.load(open("h24_results.json"))
    print(f"\n{'='*74}\nH32 -- GOLD-DEFINITION RECALL at top-8, n={n} (all 8 real repos)\n{'='*74}")
    print(f"  {'k':>4}{'REPORT':>10}{'HYDE':>10}{'RRF':>10}{'RRF-REPORT':>13}")
    print("-"*74)
    for k in (4, 8, 12, 16):
        a, b, c = r[f"REPORT@{k}"]/n, r[f"HYDE@{k}"]/n, r[f"RRF@{k}"]/n
        print(f"  {k:>4}{a:>10.4f}{b:>10.4f}{c:>10.4f}{(c-a)*100:>12.1f}p")
    print(f"\n  union of the two top-8 sets (16 chunks) = {r['UNION@16(8+8)']/n:.4f}")
    print(f"  FAIR COMPARISON -- report alone at k=16 = {r['REPORT@16']/n:.4f}"
          f"   -> union advantage {(r['UNION@16(8+8)']-r['REPORT@16'])/n*100:+.1f}pp")
    base = r["REPORT@8"]/n
    best = max(r["RRF@8"]/n, r["RRF@16"]/n)
    print(f"\n  H31 reference: gold definition alone = 0.5486 @349 tok "
          f"vs RAG8 0.2628 @3399")
    print(f"\n{'='*74}\nVERDICT\n{'='*74}")
    d16 = (r["UNION@16(8+8)"] - r["REPORT@16"])/n
    d8 = (r["RRF@8"] - r["REPORT@8"])/n
    if d8 > 0.04 or d16 > 0.04:
        print(f"  USEFUL -- matched-budget gain {d8*100:+.1f}pp at k=8, "
              f"{d16*100:+.1f}pp at k=16.")
        print("  Generated code adds recall the bug report cannot reach.")
    else:
        print(f"  FAIL -- at MATCHED budget the gain is {d8*100:+.1f}pp (k=8) and "
              f"{d16*100:+.1f}pp (k=16).")
        print("  The apparent +9.2pp was the larger candidate set, not the second query.")
