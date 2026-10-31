"""
H34 --- RECALL PER TOKEN: signature-level retrieval vs chunk-level.

THE UNTESTED ASSUMPTION
  Every retrieval this session was chunk-level (512-token slices). But LOCALISING a
  function does not require its code -- only enough to identify it. A signature plus
  docstring line is ~30 tokens; a chunk is ~425. At a fixed token budget that is a ~7x
  wider net:
      1500 tokens = 3.5 chunks (~7 functions)  vs  ~50 signatures (50 functions)

WHY IT MATTERS
  H31: the correct definition alone = 0.5486 accuracy @349 tok vs RAG8 0.2628 @3399.
  H32b: broad retrieval buys recall with TOKENS (k=8 -> 16 is +9.4pp) but no clever
  second query helps at matched budget. So the open problem is precise LOW-TOKEN
  localisation. If signatures give far better recall per token, then localisation and
  evidence should be SEPARATE stages at different granularity:
      cheap wide signature search  ->  fetch ONE full definition  ->  answer

MEASURED (retrieval only, no generation -- so this is cheap and decisive)
  chunk-level   recall@k for k=2,4,8,16    tokens ~ 425*k
  signature     recall@k for k=10..200     tokens ~ 30*k
  plotted on a common TOKEN axis, which is the comparison that matters.
  Signatures are built with AST (name, args, first docstring line, class context).

PRE-REGISTERED
  WIN    : signature recall at <=1500 tokens exceeds chunk recall at 3399 tokens
           (0.6312) -> better localisation at less than half the cost.
  USEFUL : signatures beat chunks at MATCHED tokens anywhere on the curve.
  FAIL   : chunks dominate at every budget -> a short signature carries too little
           signal to match against a prose bug report, and granularity is not the lever.
  I expect USEFUL but not WIN. More candidates must help coverage, but a 30-token
  signature is a much weaker embedding target than 425 tokens of code, so per-candidate
  precision falls. Which effect dominates is exactly what is unmeasured.

COST: A10G, embed signatures + chunks for 8 repos => ~$0.35.
"""
import ast as A, json, os, re, subprocess, modal
CHUNK_TOK, APPROX, EXCL = 512, 0.27, ("test", "tests", "vendor", "docs")
EMB = "BAAI/bge-small-en-v1.5"
REPOS = {"flask": "pallets/flask", "httpx": "encode/httpx", "click": "pallets/click",
         "requests": "psf/requests", "jinja": "pallets/jinja",
         "werkzeug": "pallets/werkzeug", "attrs": "python-attrs/attrs",
         "urllib3": "urllib3/urllib3"}
image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
app = modal.App("qcarve-h34-sigretrieval")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


def signatures(path, src):
    """one short retrievable record per symbol: class ctx, name, args, docstring line"""
    try: tree = A.parse(src)
    except Exception: return []
    out, cls = [], {}
    for nd in A.walk(tree):
        if isinstance(nd, A.ClassDef):
            for sub in nd.body: cls[id(sub)] = nd.name
    for nd in A.walk(tree):
        if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
            kind = "class" if isinstance(nd, A.ClassDef) else "def"
            args = ""
            if not isinstance(nd, A.ClassDef):
                try: args = "(" + ", ".join(a.arg for a in nd.args.args) + ")"
                except Exception: args = "()"
            doc = (A.get_docstring(nd) or "").strip().split("\n")[0][:90]
            owner = cls.get(id(nd), "")
            rec = f"{os.path.basename(path)} | {owner+'.' if owner else ''}{kind} {nd.name}{args}"
            if doc: rec += f" | {doc}"
            out.append((nd.name, rec))
    return out


@app.function(image=image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def compare():
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    items = json.load(open("/data/h21_items.json"))
    m = SentenceTransformer(EMB, device="cuda")
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    dfn = lambda c, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c))
    C = {}
    for nm, slug in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                            "https://github.com/" + slug, d], capture_output=True)
        files = [p for p in subprocess.run(["git", "ls-files"], cwd=d, capture_output=True,
                 text=True).stdout.split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        ch, sig, own = [], [], []
        nch = int(CHUNK_TOK/APPROX)
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for i in range(0, len(s), nch): ch.append(s[i:i+nch])
            for name, rec in signatures(p, s): sig.append(rec); own.append(name)
        if len(ch) < 8 or len(sig) < 20: continue
        Ec = m.encode(ch, batch_size=128, normalize_embeddings=True,
                      convert_to_numpy=True, show_progress_bar=False)
        Es = m.encode(sig, batch_size=256, normalize_embeddings=True,
                      convert_to_numpy=True, show_progress_bar=False)
        C[nm] = (ch, Ec, BM25Okapi([tk(c) for c in ch]),
                 sig, Es, BM25Okapi([tk(c) for c in sig]), own)
        print(f"  {nm}: {len(ch)} chunks, {len(sig)} signatures "
              f"(mean {sum(len(x) for x in sig)/len(sig):.0f} chars)")

    def rank(E, bm, q, pool=400):
        qv = m.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = list(np.argsort(-(E @ qv))); br = list(np.argsort(-bm.get_scores(tk(q))))
        sc = {}
        for r_, i in enumerate(dr[:pool]): sc[i] = sc.get(i, 0) + 1/(60+r_+1)
        for r_, i in enumerate(br[:pool]): sc[i] = sc.get(i, 0) + 1/(60+r_+1)
        return sorted(sc, key=lambda j: -sc[j])

    CK = (2, 4, 8, 16); SK = (10, 25, 50, 100, 200)
    res = {f"chunk@{k}": 0 for k in CK}; res.update({f"sig@{k}": 0 for k in SK})
    res["n"] = 0; res["sig_tok"] = 0.0; res["chunk_tok"] = 0.0
    for it in items:
        nm = it["repo"]
        if nm not in C: continue
        ch, Ec, bmc, sig, Es, bms, own = C[nm]; res["n"] += 1
        rc = rank(Ec, bmc, it["query"]); rs = rank(Es, bms, it["query"])
        for k in CK:
            if any(dfn(ch[j], g) for j in rc[:k] for g in it["gold"]): res[f"chunk@{k}"] += 1
        gset = set(it["gold"])
        for k in SK:
            if gset & {own[j] for j in rs[:k]}: res[f"sig@{k}"] += 1
        res["sig_tok"] += sum(len(sig[j]) for j in rs[:200])/200*APPROX
        res["chunk_tok"] += sum(len(ch[j]) for j in rc[:16])/16*APPROX
    hf_cache.commit()
    return res


@app.local_entrypoint()
def main(out: str = "h34_results.json"):
    r = compare.remote(); json.dump(r, open(out, "w"), indent=2)
    n = r["n"]; st = r["sig_tok"]/n; ct = r["chunk_tok"]/n
    print(f"\n{'='*76}\nH34 -- RECALL PER TOKEN, n={n}\n{'='*76}")
    print(f"  mean signature = {st:.0f} tok   mean chunk = {ct:.0f} tok\n")
    print(f"  {'unit':<12}{'k':>5}{'tokens':>9}{'recall':>9}")
    print("-"*76)
    pts = []
    for k in (2, 4, 8, 16):
        v = r[f"chunk@{k}"]/n; print(f"  {'chunk':<12}{k:>5}{k*ct:>9.0f}{v:>9.4f}")
        pts.append(("chunk", k*ct, v))
    print()
    for k in (10, 25, 50, 100, 200):
        v = r[f"sig@{k}"]/n; print(f"  {'signature':<12}{k:>5}{k*st:>9.0f}{v:>9.4f}")
        pts.append(("sig", k*st, v))
    c8 = r["chunk@8"]/n
    cheap = [(t, v) for u, t, v in pts if u == "sig" and t <= 1500]
    best_cheap = max(cheap, key=lambda x: x[1]) if cheap else (0, 0)
    print(f"\n  chunk baseline: {c8:.4f} recall @ {8*ct:.0f} tok")
    print(f"  best signature under 1500 tok: {best_cheap[1]:.4f} @ {best_cheap[0]:.0f} tok")
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if best_cheap[1] > c8:
        print(f"  WIN -- signatures reach {best_cheap[1]:.4f} at {best_cheap[0]:.0f} tokens,")
        print(f"  beating chunk recall {c8:.4f} at {8*ct:.0f} tokens. Localisation and")
        print("  evidence should be separate stages at different granularity.")
    else:
        same = [(t, v) for u, t, v in pts if u == "sig" and t <= 8*ct]
        b = max(same, key=lambda x: x[1]) if same else (0, 0)
        if b[1] > c8:
            print(f"  USEFUL -- at matched tokens signatures reach {b[1]:.4f} vs {c8:.4f}.")
        else:
            print(f"  FAIL -- chunks dominate at every budget ({c8:.4f} vs best "
                  f"signature {max(v for u,_,v in pts if u=='sig'):.4f}).")
            print("  A short signature is too weak a target for a prose bug report.")
