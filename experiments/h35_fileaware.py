"""
H35 --- Is the signature win real? File-aware gold + the small-k regime that matters.

WHAT H34 SHOWED
    signature@25 = 0.6438 @ 559 tok   vs   chunk@8 = 0.6312 @ 3959 tok
  i.e. the same recall at ~7x fewer localisation tokens. Two reasons that may be wrong:

  (1) ASYMMETRIC SCORING. Chunk recall requires gold's DEFINITION to be in the chunk.
      Signature recall only requires a NAME match -- and 36.2% of gold names have
      multiple definitions (`__init__` has 62 and is gold 9.4% of the time). A hit on
      the wrong `convert` scores as success. Signatures are flattered by an unknown
      amount.
  (2) THE HIDDEN LOCALISER. recall@50 only pays off if something picks among 50. That
      step has failed 14 times, and widening 8 -> 50 makes it harder, not easier
      (H14: picking among 8 signatures closed only 9.7% of the rank-0 -> oracle gap).
      The deployable design fetches definitions for the TOP-m signatures and lets the
      answer model see all of them, so signature recall at SMALL m is the real metric.
      H34 never measured below k=10.

THE FIX
  Re-derive gold as (file, symbol) PAIRS from each commit's diff, and score both units
  the same way: a hit requires the right symbol IN THE RIGHT FILE. Then sweep
  k = 1,2,3,5,10,25,50 so the small-m regime is visible.

PRE-REGISTERED
  HOLDS   : file-aware signature recall still beats chunk recall at matched tokens,
            AND signature recall@3 (~1050 tok once definitions are fetched) >= 0.45.
  DEFLATED: signatures still win on the curve but recall@3 < 0.45 -> the advantage
            depends on a localiser that does not exist.
  ILLUSORY: file-aware scoring erases the advantage -> H34 was the name/definition
            asymmetry, not a real result.
  I expect DEFLATED. The per-token curve should survive file-aware scoring, but small-k
  recall is where thin 22-token signatures are weakest against a prose bug report.
  Stating this before the run.

COST: CPU clone + A10G embed, ~$0.40.
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
app = modal.App("qcarve-h35-fileaware")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


def innermost(src, lines):
    try: tree = A.parse(src)
    except Exception: return set()
    sp = [(n.lineno, getattr(n, "end_lineno", n.lineno), n.name) for n in A.walk(tree)
          if isinstance(n, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef))]
    out = set()
    for l in lines:
        best = None
        for a, b, nm in sp:
            if a <= l <= b and (best is None or (b-a) < best[0]): best = (b-a, nm)
        if best: out.add(best[1])
    return out


def sigs(path, src):
    try: tree = A.parse(src)
    except Exception: return []
    cls = {}
    for nd in A.walk(tree):
        if isinstance(nd, A.ClassDef):
            for sub in nd.body: cls[id(sub)] = nd.name
    out = []
    for nd in A.walk(tree):
        if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
            kind = "class" if isinstance(nd, A.ClassDef) else "def"
            args = "" if isinstance(nd, A.ClassDef) else "(" + ", ".join(
                a.arg for a in nd.args.args) + ")"
            doc = (A.get_docstring(nd) or "").strip().split("\n")[0][:90]
            owner = cls.get(id(nd), "")
            rec = f"{os.path.basename(path)} | {owner+'.' if owner else ''}{kind} {nd.name}{args}"
            if doc: rec += f" | {doc}"
            out.append((path, nd.name, rec))
    return out


@app.function(image=image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run():
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
            subprocess.run(["git", "clone", "--quiet", "https://github.com/"+slug, d],
                           capture_output=True)
        subprocess.run(["git", "checkout", "--quiet", "--force", "HEAD"], cwd=d,
                       capture_output=True)
        files = [p for p in subprocess.run(["git", "ls-files"], cwd=d, capture_output=True,
                 text=True).stdout.split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        ch, cown, sg, sown = [], [], [], []
        nch = int(CHUNK_TOK/APPROX)
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for i in range(0, len(s), nch):
                ch.append(s[i:i+nch]); cown.append(p)
            for fp, name, rec in sigs(p, s): sg.append(rec); sown.append((fp, name))
        if len(ch) < 8 or len(sg) < 20: continue
        idx[nm] = (ch, cown, m.encode(ch, batch_size=128, normalize_embeddings=True,
                   convert_to_numpy=True, show_progress_bar=False),
                   BM25Okapi([tk(c) for c in ch]), sg, sown,
                   m.encode(sg, batch_size=256, normalize_embeddings=True,
                   convert_to_numpy=True, show_progress_bar=False),
                   BM25Okapi([tk(c) for c in sg]), d)
        print(f"  {nm}: {len(ch)} chunks / {len(sg)} signatures")

    # ---- file-aware gold: (file, symbol) pairs from the commit diff ----
    gold_fa, nog = {}, 0
    for i, it in enumerate(items):
        nm = it["repo"]
        if nm not in idx: continue
        d = idx[nm][8]
        subprocess.run(["git", "checkout", "--quiet", "--force", it["sha"]], cwd=d,
                       capture_output=True)
        diff = subprocess.run(["git", "show", "--unified=0", "--format=", it["sha"]],
                              cwd=d, capture_output=True, text=True).stdout
        cur, ch_lines = None, {}
        for line in diff.split("\n"):
            mm = re.match(r"\+\+\+ b/(.+)", line)
            if mm: cur = mm.group(1)
            h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if h and cur and cur.endswith(".py") and "test" not in cur.lower():
                st = int(h.group(1)); ln = int(h.group(2) or 1)
                ch_lines.setdefault(cur, []).extend(range(st, st+max(1, ln)))
        g = set()
        for f, lns in ch_lines.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                try: src = open(p, encoding="utf-8", errors="ignore").read()
                except OSError: continue
                for s in innermost(src, lns): g.add((f, s))
        subprocess.run(["git", "checkout", "--quiet", "--force", "HEAD"], cwd=d,
                       capture_output=True)
        if g: gold_fa[i] = g
        else: nog += 1
    print(f"  file-aware gold built for {len(gold_fa)}/{len(items)} items ({nog} empty)")

    def rank(E, bm, q, pool=400):
        qv = m.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = list(np.argsort(-(E @ qv))); br = list(np.argsort(-bm.get_scores(tk(q))))
        sc = {}
        for r_, i2 in enumerate(dr[:pool]): sc[i2] = sc.get(i2, 0) + 1/(60+r_+1)
        for r_, i2 in enumerate(br[:pool]): sc[i2] = sc.get(i2, 0) + 1/(60+r_+1)
        return sorted(sc, key=lambda j: -sc[j])

    CK = (1, 2, 4, 8, 16); SK = (1, 2, 3, 5, 10, 25, 50)
    res = {f"chunk@{k}": 0 for k in CK}; res.update({f"sig@{k}": 0 for k in SK})
    res.update({f"signame@{k}": 0 for k in SK})
    res["n"] = 0; res["st"] = 0.0; res["ct"] = 0.0
    for i, it in enumerate(items):
        nm = it["repo"]
        if nm not in idx or i not in gold_fa: continue
        ch, cown, Ec, bmc, sg, sown, Es, bms, _ = idx[nm]
        G = gold_fa[i]; Gn = {s for _, s in G}; res["n"] += 1
        rc = rank(Ec, bmc, it["query"]); rs = rank(Es, bms, it["query"])
        for k in CK:
            if any((cown[j] == f and re.search(rf"(?:def|class)\s+{re.escape(s)}\b", ch[j]))
                   for j in rc[:k] for f, s in G): res[f"chunk@{k}"] += 1
        for k in SK:
            if G & {sown[j] for j in rs[:k]}: res[f"sig@{k}"] += 1
            if Gn & {sown[j][1] for j in rs[:k]}: res[f"signame@{k}"] += 1
        res["st"] += sum(len(sg[j]) for j in rs[:50])/50*APPROX
        res["ct"] += sum(len(ch[j]) for j in rc[:16])/16*APPROX
    hf_cache.commit()
    return res


@app.local_entrypoint()
def main(out: str = "h35_results.json"):
    r = run.remote(); json.dump(r, open(out, "w"), indent=2)
    n = r["n"]; st = r["st"]/n; ct = r["ct"]/n
    print(f"\n{'='*78}\nH35 -- FILE-AWARE RECALL, n={n}\n{'='*78}")
    print(f"  signature {st:.0f} tok, chunk {ct:.0f} tok\n")
    print(f"  {'unit':<22}{'k':>4}{'loc tok':>9}{'recall':>9}")
    print("-"*78)
    for k in (1, 2, 4, 8, 16):
        print(f"  {'chunk (file-aware)':<22}{k:>4}{k*ct:>9.0f}{r[f'chunk@{k}']/n:>9.4f}")
    print()
    for k in (1, 2, 3, 5, 10, 25, 50):
        print(f"  {'signature (file-aware)':<22}{k:>4}{k*st:>9.0f}{r[f'sig@{k}']/n:>9.4f}"
              f"   name-only {r[f'signame@{k}']/n:>6.4f}")
    c8 = r["chunk@8"]/n; s3 = r["sig@3"]/n; s25 = r["sig@25"]/n
    infl = (r["signame@25"] - r["sig@25"])/n
    print(f"\n  name-vs-file inflation at k=25: {infl*100:+.1f}pp "
          f"(name-only {r['signame@25']/n:.4f} vs file-aware {s25:.4f})")
    print(f"  chunk@8 = {c8:.4f} @ {8*ct:.0f} tok")
    print(f"  sig@3   = {s3:.4f} @ {3*st:.0f} tok  (+~{3*349} tok to fetch 3 definitions)")
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if s25 > c8 and s3 >= 0.45:
        print(f"  HOLDS -- file-aware signatures still beat chunks per token, and")
        print(f"  recall@3 = {s3:.4f} >= 0.45, so the top-m design works WITHOUT a localiser.")
    elif s25 > c8:
        print(f"  DEFLATED -- the per-token curve survives ({s25:.4f} vs {c8:.4f}),")
        print(f"  but recall@3 = {s3:.4f} < 0.45: the advantage needs a localiser that")
        print("  14 experiments say does not exist.")
    else:
        print(f"  ILLUSORY -- file-aware scoring erases it ({s25:.4f} vs {c8:.4f}).")
        print("  H34 measured the name/definition asymmetry, not a real advantage.")
