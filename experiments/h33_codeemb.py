"""
H33 --- The obvious lever I never pulled: a CODE embedder instead of a text embedder.

THE OVERSIGHT
  Every retrieval in this session used BAAI/bge-small-en-v1.5 -- a general-purpose
  ENGLISH TEXT embedder -- over Python source. I built 14 mechanisms against the recall
  bottleneck without once questioning the retriever itself.

WHY IT MATTERS NOW
  H31 proved recall is the binding constraint: gold definition alone = 0.5486 @349 tok
  vs RAG8 0.2628 @3399. H32b showed no clever second query helps at matched budget
  (RRF +1.0pp at k=8; the apparent +9.2pp was just a doubled candidate set), while
  simply going k=8 -> 16 buys +9.4pp recall. So recall responds to BRUTE budget but
  not to cleverness -- which makes the quality of the RETRIEVER itself the untested
  variable.

WHAT IS COMPARED (identical corpus, chunks, queries, gold, and BM25 component)
  bge-small-en-v1.5   general English text      the incumbent, recall@8 = 0.6312
  jina-embeddings-v2-base-code   trained on code-text pairs
  bge-m3              multilingual, stronger on code than bge-small
  Each is measured dense-only AND fused with BM25 via RRF, at k = 4, 8, 12, 16.

PRE-REGISTERED
  WIN    : a code embedder reaches >= 0.72 recall at k=8 (what the incumbent needs
           k=16 to reach) -> same recall at HALF the candidate tokens.
  USEFUL : +4pp or more at matched k.
  FAIL   : < +4pp -> the retriever was not the problem, and recall on this task is
           limited by something other than embedding quality.
  I expect USEFUL. Code embedders help most when queries are code-like, but here the
  query is a PROSE bug report -- the asymmetric case they are least suited to. The
  corpus side improves; the query side may not. Stating this before the run.

COST: A10G, 3 embedders x ~2000 chunks x 8 repos => ~$0.45.
"""
import json, os, re, subprocess, modal
CHUNK_TOK, APPROX = 512, 0.27
EXCL = ("test", "tests", "vendor", "docs")
REPOS = {"flask": "pallets/flask", "httpx": "encode/httpx", "click": "pallets/click",
         "requests": "psf/requests", "jinja": "pallets/jinja",
         "werkzeug": "pallets/werkzeug", "attrs": "python-attrs/attrs",
         "urllib3": "urllib3/urllib3"}
MODELS = [("bge-small", "BAAI/bge-small-en-v1.5", False),
          ("jina-code", "jinaai/jina-embeddings-v2-base-code", True),
          ("bge-m3", "BAAI/bge-m3", False)]

image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4", "einops==0.8.0")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
app = modal.App("qcarve-h33-codeemb")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


@app.function(image=image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def compare():
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    items = json.load(open("/data/h21_items.json"))
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    dfn = lambda c, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c))

    corpus = {}
    for nm, slug in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                            "https://github.com/" + slug, d], capture_output=True)
        files = [p for p in subprocess.run(["git", "ls-files"], cwd=d, capture_output=True,
                 text=True).stdout.split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        ch = []; nch = int(CHUNK_TOK/APPROX)
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for i in range(0, len(s), nch): ch.append(s[i:i+nch])
        if len(ch) >= 8:
            corpus[nm] = (ch, BM25Okapi([tk(c) for c in ch]))
    print(f"  corpus: {sum(len(v[0]) for v in corpus.values())} chunks over {len(corpus)} repos")

    KS = (4, 8, 12, 16)
    out = {}
    for tag, mid, remote in MODELS:
        try:
            m = SentenceTransformer(mid, device="cuda", trust_remote_code=remote)
            m.max_seq_length = min(getattr(m, "max_seq_length", 512) or 512, 512)
        except Exception as e:
            print(f"  [{tag}] LOAD FAILED: {type(e).__name__}: {str(e)[:120]}")
            out[tag] = {"error": f"{type(e).__name__}"}
            continue
        E = {}
        for nm, (ch, _) in corpus.items():
            E[nm] = m.encode(ch, batch_size=64, normalize_embeddings=True,
                             convert_to_numpy=True, show_progress_bar=False)
        res = {f"dense@{k}": 0 for k in KS}
        res.update({f"rrf@{k}": 0 for k in KS}); res["n"] = 0
        for it in items:
            nm = it["repo"]
            if nm not in corpus: continue
            ch, bm = corpus[nm]; res["n"] += 1
            qv = m.encode([it["query"]], normalize_embeddings=True,
                          convert_to_numpy=True)[0]
            dr = list(np.argsort(-(E[nm] @ qv)))
            br = list(np.argsort(-bm.get_scores(tk(it["query"]))))
            sc = {}
            for r_, i in enumerate(dr[:200]): sc[i] = sc.get(i, 0) + 1/(60+r_+1)
            for r_, i in enumerate(br[:200]): sc[i] = sc.get(i, 0) + 1/(60+r_+1)
            fu = sorted(sc, key=lambda j: -sc[j])
            hit = lambda idx: any(dfn(ch[j], g) for j in idx for g in it["gold"])
            for k in KS:
                res[f"dense@{k}"] += hit(dr[:k]); res[f"rrf@{k}"] += hit(fu[:k])
        out[tag] = res
        n = res["n"]
        print(f"  [{tag}] dense@8={res['dense@8']/n:.4f}  rrf@8={res['rrf@8']/n:.4f}")
        del m, E
        import gc, torch; gc.collect(); torch.cuda.empty_cache()
    hf_cache.commit()
    return out


@app.local_entrypoint()
def main(out: str = "h33_results.json"):
    r = compare.remote(); json.dump(r, open(out, "w"), indent=2)
    print(f"\n{'='*80}\nH33 -- GOLD-DEFINITION RECALL by EMBEDDER (identical corpus & BM25)\n{'='*80}")
    print(f"  {'embedder':<12}{'mode':<8}" + "".join(f"{'k='+str(k):>9}" for k in (4,8,12,16)))
    print("-"*80)
    base8 = None
    for tag, _, _ in MODELS:
        d = r.get(tag, {})
        if "error" in d:
            print(f"  {tag:<12}{'--':<8}  LOAD FAILED ({d['error']})"); continue
        n = d["n"]
        for mode in ("dense", "rrf"):
            row = "".join(f"{d[f'{mode}@{k}']/n:>9.4f}" for k in (4,8,12,16))
            print(f"  {tag:<12}{mode:<8}{row}")
        if tag == "bge-small": base8 = d["rrf@8"]/n
    print(f"\n  incumbent (bge-small rrf@8) = {base8:.4f};  it needs k=16 to reach 0.7250")
    best, bt = 0, None
    for tag, _, _ in MODELS:
        d = r.get(tag, {})
        if "error" in d or tag == "bge-small": continue
        v = d["rrf@8"]/d["n"]
        if v > best: best, bt = v, tag
    print(f"\n{'='*80}\nVERDICT\n{'='*80}")
    if bt is None:
        print("  INCONCLUSIVE -- no alternative embedder loaded; nothing to compare.")
    elif best >= 0.72:
        print(f"  WIN -- {bt} reaches {best:.4f} at k=8, what bge-small needs k=16 for.")
        print("  Same recall at HALF the candidate tokens, from swapping the retriever.")
    elif best >= base8 + 0.04:
        print(f"  USEFUL -- {bt} {best:.4f} vs {base8:.4f} at matched k=8 "
              f"({(best-base8)*100:+.1f}pp).")
    else:
        print(f"  FAIL -- best alternative {bt} {best:.4f} vs incumbent {base8:.4f} "
              f"({(best-base8)*100:+.1f}pp).")
        print("  The retriever was not the problem; recall is limited by something else.")
