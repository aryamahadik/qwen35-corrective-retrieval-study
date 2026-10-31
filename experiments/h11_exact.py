"""
H11 --- The stop condition requires the STRONGEST router + an EXACT verifier.
Neither was tested. This tests both, and measures gamma and latency, which were
never measured at all.

WHY THIS CAN OVERTURN THE NO-GO
-------------------------------
My diagnosis of the failure (H5/H6) was: p_slow is invariant in retrieval budget k
because THE VERIFIER READS THE SAME SIGNAL AS THE RETRIEVER -- both are text
similarity, so escalating k moves items between buckets without reducing
unrepairable misses.

An AST SYMBOL TABLE is a genuinely independent signal: exact name RESOLUTION, not
similarity. If a bug report names `save_session`, resolution returns its definition
site with certainty -- no embedding, no BM25, no ranking. That is the "compiled
address / evidence-plan routing" of architecture-search item 2 and the "cheap exact
structural verification" of item 3, neither of which I actually implemented.

ARMS (identical model, prompt, queries; only evidence differs)
  RAG8      8 chunks   ~3399 tok   strong baseline
  RAG2      2 chunks    ~912 tok   MATCHED-BUDGET control
  FAST3     3 spans     ~860 tok   previous architecture arm (RRF only)
  RERANK3   3 spans     ~860 tok   STRONGEST ROUTER: RRF -> cross-encoder rerank
  SYM3      3 spans     ~860 tok   EXACT: AST symbol resolution first, RRF fills
  SYMRR3    3 spans     ~860 tok   both

PRE-REGISTERED
  The architecture is revived iff some fast arm beats RAG2 at matched budget
  (McNemar p<0.05, positive direction). Otherwise the NO-GO extends to the
  strongest router and the exact verifier, and is no longer scoped.
  I expect SYM3 > FAST3 (resolution adds real information) but still <= RAG2,
  because ~half of queries name no resolvable symbol. Stating this before the run.

ALSO MEASURED FOR THE FIRST TIME
  gamma = retrieval rounds to reach gold, fast vs RAG (escalation ladder)
  L(50), L(95) of the retrieval stage, reported SEPARATELY from generation.

COST: A10G build + A10G 7B generate => ~$0.60. Escalate to 32B only if an arm wins.
"""
import ast as pyast, json, os, re, subprocess, time, modal

GPU = "A10G"
EMB_MODEL = "BAAI/bge-small-en-v1.5"
RERANKER = "BAAI/bge-reranker-base"
LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"

build_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))

app = modal.App("qcarve-h11-exact")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

REPOS = ["https://github.com/pallets/flask", "https://github.com/encode/httpx",
         "https://github.com/pallets/click"]
FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")
EXCL = ("test", "tests", "vendor", "docs")
CHUNK_TOK, TOP_K_RAG, APPROX, SEP = 512, 8, 0.27, "\n\n---\n\n"

def _sh(c, cwd=None): return subprocess.run(c, cwd=cwd, capture_output=True, text=True).stdout
def _is_code(p):
    lo = p.lower()
    return not any(f"/{x}/" in f"/{lo}" for x in EXCL) and os.path.splitext(lo)[1] == ".py"
def _split_chunks(t):
    n = int(CHUNK_TOK / APPROX); return [t[i:i+n] for i in range(0, len(t), n)] or [t]
def _idents(s): return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", s))


def ast_symbols(path, src):
    """EXACT structural index: real AST, not a regex. name -> (file, source segment)."""
    out = []
    try: tree = pyast.parse(src)
    except SyntaxError: return out
    lines = src.split("\n")
    for node in pyast.walk(tree):
        if isinstance(node, (pyast.FunctionDef, pyast.AsyncFunctionDef, pyast.ClassDef)):
            a = node.lineno - 1
            b = getattr(node, "end_lineno", None) or min(a + 60, len(lines))
            seg = "\n".join(lines[a:b]).strip()
            if seg: out.append((node.name, path, seg))
    return out


@app.function(image=build_image, gpu=GPU, timeout=3600,
              volumes={"/hf": hf_cache, "/data": data_vol})
def build(per_repo=80):
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer, CrossEncoder
    from rank_bm25 import BM25Okapi
    emb = SentenceTransformer(EMB_MODEL, device="cuda")
    rr = CrossEncoder(RERANKER, device="cuda", max_length=512)
    tokz = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    items, diag = [], []

    for url in REPOS:
        name = url.rstrip("/").split("/")[-1]; d = f"/tmp/{name}"
        if not os.path.exists(d): _sh(["git", "clone", "--quiet", url, d])
        files = [p for p in _sh(["git", "ls-files"], d).split("\n") if p and _is_code(p)]
        contents = {}
        for p in files:
            try:
                s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
                if 200 < len(s) < 200_000: contents[p] = s
            except OSError: pass
        if len(contents) < 8: continue

        chunks, chunk_owner, spans, span_owner, symtab = [], [], [], [], {}
        for p, s in contents.items():
            for c in _split_chunks(s): chunks.append(c); chunk_owner.append(p)
            for nm, fp, seg in ast_symbols(p, s):
                i = len(spans); spans.append(seg); span_owner.append(fp)
                symtab.setdefault(nm, []).append(i)

        E_c = emb.encode(chunks, batch_size=256, normalize_embeddings=True,
                         convert_to_numpy=True, show_progress_bar=False)
        E_s = emb.encode(spans, batch_size=256, normalize_embeddings=True,
                         convert_to_numpy=True, show_progress_bar=False)
        bm_c, bm_s = BM25Okapi([tokz(c) for c in chunks]), BM25Okapi([tokz(c) for c in spans])

        def rrf(bm, E, q, k, kk=60, pool=200):
            qv = emb.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
            dr = np.argsort(-(E @ qv)); br = np.argsort(-bm.get_scores(tokz(q)))
            sc = {}
            for r_, i in enumerate(dr[:pool]): sc[i] = sc.get(i, 0) + 1/(kk+r_+1)
            for r_, i in enumerate(br[:pool]): sc[i] = sc.get(i, 0) + 1/(kk+r_+1)
            return sorted(sc, key=lambda i: -sc[i])[:k]

        log = _sh(["git","log","--no-merges","-n","1200",
                   "--pretty=format:@@@%H|%B<<<E>>>"], d)
        n = 0
        for blk in log.split("@@@")[1:]:
            if n >= per_repo: break
            try: sha, rest = blk.split("|", 1)
            except ValueError: continue
            msg = rest.split("<<<E>>>")[0].strip().replace("\n", " ")[:900]
            if not any(w in msg.lower() for w in FIX) or len(msg) < 25: continue
            diff = _sh(["git","show","--unified=0","--format=","-M", sha], d)
            gold = set()
            for line in diff.split("\n"):
                m = re.match(r"@@ .*? @@\s*(?:async\s+)?(?:def|class)\s+(\w+)", line)
                if m: gold.add(m.group(1))
            if not (1 <= len(gold) <= 4): continue

            t0 = time.perf_counter(); idx_r = rrf(bm_c, E_c, msg, TOP_K_RAG)
            t_rag = time.perf_counter() - t0
            t0 = time.perf_counter(); base = rrf(bm_s, E_s, msg, 3); t_fast = time.perf_counter() - t0

            # ---- EXACT AST symbol resolution: no embedding, no ranking ----
            t0 = time.perf_counter()
            qi = _idents(msg)
            resolved = []
            for nm in sorted(qi & set(symtab)):
                for i in symtab[nm][:2]:
                    if i not in resolved: resolved.append(i)
            t_sym = time.perf_counter() - t0
            sym3 = (resolved[:3] + [i for i in base if i not in resolved])[:3]

            # ---- STRONGEST ROUTER: cross-encoder rerank of a 50-candidate pool ----
            t0 = time.perf_counter()
            pool = rrf(bm_s, E_s, msg, 50)
            sc = rr.predict([[msg, spans[i][:1800]] for i in pool])
            rer = [pool[j] for j in np.argsort(-sc)]
            t_rr = time.perf_counter() - t0
            rr3 = rer[:3]
            symrr3 = (resolved[:2] + [i for i in rer if i not in resolved])[:3]

            ev = lambda ix: SEP.join(spans[i] for i in ix)
            items.append({
                "repo": name, "sha": sha[:8], "query": msg, "gold": sorted(gold),
                "RAG8": SEP.join(chunks[i] for i in idx_r),
                "RAG2": SEP.join(chunks[i] for i in idx_r[:2]),
                "FAST3": ev(base), "RERANK3": ev(rr3), "SYM3": ev(sym3), "SYMRR3": ev(symrr3),
            })
            diag.append({
                "repo": name,
                "n_resolved": len(resolved),
                "addressable": int(bool(resolved)),
                # does exact resolution land a GOLD symbol name directly?
                "gold_resolved": int(bool(gold & qi & set(symtab))),
                "lat_rag_ms": round(t_rag*1000, 2), "lat_fast_ms": round(t_fast*1000, 2),
                "lat_sym_ms": round(t_sym*1000, 2), "lat_rerank_ms": round(t_rr*1000, 2),
            })
            n += 1
        print(f"{name}: {n} queries  files={len(contents)} spans={len(spans)} symbols={len(symtab)}")

    json.dump(items, open("/data/h11_items.json", "w"))
    json.dump(diag, open("/data/h11_diag.json", "w"))
    data_vol.commit(); hf_cache.commit()
    addr = sum(d["addressable"] for d in diag)
    return {"n": len(items), "addressable": addr, "addressable_frac": round(addr/max(1,len(diag)), 4),
            "diag": diag}


@app.function(image=llm_image, gpu=GPU, timeout=3600,
              volumes={"/hf": hf_cache, "/data": data_vol})
def answer(model=LLM_MODEL):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h11_items.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=False, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
           "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
           "Which single function or class must be modified to fix this bug?\n"
           "Answer with ONLY the name, nothing else.")
    out = {}
    for arm in ("RAG8", "RAG2", "FAST3", "RERANK3", "SYM3", "SYMRR3"):
        prompts, ntoks = [], []
        for it in items:
            ev = it[arm]
            if len(tok(TPL.format(q=it["query"], e=ev))["input_ids"]) > 7800:
                ev = tok.decode(tok(ev)["input_ids"][:7400])
            p = TPL.format(q=it["query"], e=ev)
            prompts.append(tok.apply_chat_template([{"role": "user", "content": p}],
                                                   tokenize=False, add_generation_prompt=True))
            ntoks.append(len(tok(p)["input_ids"]))
        res = llm.generate(prompts, sp)
        out[arm] = [{"repo": it["repo"], "hit": int(any(re.search(rf"\b{re.escape(g)}\b",
                     r.outputs[0].text) for g in it["gold"])), "n_tok": nt, "gold": it["gold"]}
                    for it, r, nt in zip(items, res, ntoks)]
        print(f"  {arm:<8} acc={sum(x['hit'] for x in out[arm])/len(out[arm]):.4f}  "
              f"tok={sum(x['n_tok'] for x in out[arm])/len(out[arm]):.0f}")
    hf_cache.commit()
    return {"model": model, "arms": out}


@app.local_entrypoint()
def main(out: str = "h11_results.json"):
    b = build.remote()
    print(f"\nbuild: n={b['n']}  ADDRESSABLE (>=1 query identifier resolves to a real "
          f"AST symbol): {b['addressable']}/{b['n']} = {b['addressable_frac']:.1%}\n")
    r = answer.remote(); r["build"] = b
    json.dump(r, open(out, "w"), indent=2)
    A = r["arms"]; n = len(A["RAG8"])
    acc = lambda a: sum(x["hit"] for x in A[a])/n
    tkn = lambda a: sum(x["n_tok"] for x in A[a])/n
    from math import comb
    print(f"{'='*80}\n{r['model']}  n={n}\n{'='*80}")
    print(f"{'arm':<9}{'acc':>9}{'tok':>8}{'x':>8}{'D vs RAG8':>12}{'vs RAG2 (matched)':>20}")
    print("-"*80)
    for a in ("RAG8","RAG2","FAST3","RERANK3","SYM3","SYMRR3"):
        cell = ""
        if a not in ("RAG8","RAG2"):
            f=[x["hit"] for x in A[a]]; g=[x["hit"] for x in A["RAG2"]]
            bb=sum(1 for i,j in zip(f,g) if i and not j); cc=sum(1 for i,j in zip(f,g) if j and not i)
            m=bb+cc; k=min(bb,cc)
            p=min(1.0, 2*sum(comb(m,i) for i in range(k+1))/2**m) if m else 1.0
            cell=f"{(acc(a)-acc('RAG2'))*100:+.1f}pp p={p:.3f}"
        print(f"{a:<9}{acc(a):>9.4f}{tkn(a):>8.0f}{tkn('RAG8')/tkn(a):>7.2f}x"
              f"{(acc('RAG8')-acc(a))*100:>11.1f}p{cell:>20}")
    wins=[a for a in ("FAST3","RERANK3","SYM3","SYMRR3") if acc(a) > acc("RAG2")]
    print(f"\n  arms beating the matched-budget RAG2 control: {wins or 'NONE'}")
    print("  -> NO-GO extends to strongest router + exact verifier" if not wins
          else "  -> ARCHITECTURE REVIVED on at least one arm; verify significance")
