"""
H38 --- DEFINITION-granularity evidence: the unit the diagnosis points to.

THE DIAGNOSIS THAT LED HERE
  Accuracy = P(gold retrieved) x P(correct | gold present). Sixteen mechanisms attacked
  the first term. The second was treated as a constant. It is not:
      conversion, all (query,chunk) pairs where the chunk defines gold : 44.9%
      ... excluding dunder gold (__init__ etc, unnameable)             : 51.4%
      ... restricted to chunks defining <=2 symbols                    : 58.7%
      ... both                                                         : 62.2%
      H31, gold DEFINITION alone (1 function, no neighbours)           : 54.9%
  A 512-token chunk holds 3.0 definitions on average, and 41.1% of failures name
  ANOTHER symbol defined in the SAME chunk (gold `run` -> said `make_shell_context`;
  gold `_find_package_path` -> said `find_spec`). The evidence unit BUILDS IN the
  confusion: we hand over three functions and ask which one function is buggy.

THE UNIT NEVER TESTED AS EVIDENCE
  signatures (22 tok)  -- too thin to reason from, conversion 43%
  chunks (495 tok)     -- 3 functions per unit, conversion 45%
  DEFINITIONS          -- exactly one function, full source. H31 priced it at 54.9%.
  H11 compared AST spans to chunks long ago, but on the old corpus, with name-based
  gold and no conversion analysis -- it measured answer quality, not this.

ARMS (identical queries, gold, scorer; only the retrieval UNIT changes)
  DEF4 / DEF8 / DEF12    top-k whole definitions, RRF over dense+BM25
  reference: RAG8 = 0.2628 on evidence-needed @3399 tok

PRE-REGISTERED
  WIN  : some DEF arm >= 0.2628 at <= 3399 tokens -> granularity alone beats RAG,
         with no selector, reranker, or generation anywhere in the pipeline.
  PART : beats RAG8 only above 3399 tokens.
  FAIL : below RAG8 at every budget -> definition units lose enough RECALL (fewer,
         larger units per token) to cancel their conversion advantage.
  The risk is explicit: definitions raise conversion but each costs ~350 tok versus a
  chunk's 495 covering 3 functions, so recall per token may fall. Conversion x recall
  is what decides it, and I do not know which dominates. Stating that before the run.

COST: A10G embed + 7B answer => ~$0.45.
"""
import ast as A, json, os, re, subprocess, modal
SEP = "\n\n---\n\n"
APPROX, EXCL = 0.27, ("test", "tests", "vendor", "docs")
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
app = modal.App("qcarve-h38-defretrieval")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


def defs_of(path, src):
    try: tree = A.parse(src)
    except Exception: return []
    L = src.split("\n"); out = []
    for nd in A.walk(tree):
        if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
            a = nd.lineno-1; b = getattr(nd, "end_lineno", a+1)
            body = "\n".join(L[a:b])
            if 40 < len(body) < 6000:
                out.append((nd.name, f"# {os.path.basename(path)}\n{body}"))
    return out


@app.function(image=emb_image, gpu="A10G", timeout=7200,
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
        dv = []
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            dv.extend(defs_of(p, s))
        if len(dv) < 12: continue
        txt = [t for _, t in dv]
        idx[nm] = (dv, m.encode(txt, batch_size=64, normalize_embeddings=True,
                   convert_to_numpy=True, show_progress_bar=False),
                   BM25Okapi([tk(t) for t in txt]))
        print(f"  {nm}: {len(dv)} definitions (mean {sum(len(t) for t in txt)/len(txt)*APPROX:.0f} tok)")
    out = []
    for it in items:
        nm = it["repo"]
        if nm not in idx: out.append(None); continue
        dv, E, bm = idx[nm]
        qv = m.encode([it["query"]], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = list(np.argsort(-(E @ qv))); br = list(np.argsort(-bm.get_scores(tk(it["query"]))))
        sc = {}
        for r_, j in enumerate(dr[:300]): sc[j] = sc.get(j, 0) + 1/(60+r_+1)
        for r_, j in enumerate(br[:300]): sc[j] = sc.get(j, 0) + 1/(60+r_+1)
        top = sorted(sc, key=lambda j: -sc[j])[:12]
        out.append({"defs": [dv[j][1] for j in top], "names": [dv[j][0] for j in top]})
    json.dump(out, open("/data/h38_ctx.json", "w")); data_vol.commit(); hf_cache.commit()
    return {"n": sum(1 for x in out if x)}


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def answer(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json"))
    ctx = json.load(open("/data/h38_ctx.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=16384,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key, nt = [], [], []
    for i, it in enumerate(items):
        c = ctx[i]
        if not c: continue
        for k in (4, 8, 12):
            body = TPL.format(q=it["query"], e=SEP.join(c["defs"][:k]))
            pr.append(body); key.append((i, f"DEF{k}")); nt.append(len(tok(body)["input_ids"]))
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
def main(out: str = "h38_results.json"):
    b = build.remote(); print(f"  contexts for {b['n']} items")
    r = answer.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json")); N = json.load(open("h24_results.json"))
    ctx = None
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = H["r7"]["n"]; null = N["NOCTX"]; P7 = H["r7"]["R"]
    real = set(i for i in range(n) if repos[i] not in SMALL)
    need = set(i for i in real if null[i] == 0)
    print(f"\n{'='*74}\nH38 -- DEFINITION-GRANULARITY EVIDENCE\n{'='*74}")
    print(f"  {'arm':<10}{'tokens':>8}{'all real':>11}{'evidence-needed':>18}")
    print("-"*74)
    best = 0
    for tag in ("DEF4", "DEF8", "DEF12"):
        v = r.get(tag, [])
        if not v: continue
        ar = [h for i, h, _ in v if i in real]; nd = [h for i, h, _ in v if i in need]
        t = sum(t for _, _, t in v)/len(v)
        a = sum(ar)/max(1, len(ar)); d = sum(nd)/max(1, len(nd))
        if t <= 3399: best = max(best, d)
        print(f"  {tag:<10}{t:>8.0f}{a:>11.4f}{d:>18.4f}")
    r8r = sum(P7[i] for i in real)/len(real); r8n = sum(P7[i] for i in need)/len(need)
    print(f"  {'RAG8':<10}{3399:>8}{r8r:>11.4f}{r8n:>18.4f}")
    print(f"\n  chunk conversion 44.9% vs definition-alone 54.9% (H31) -- the bet")
    print(f"\n{'='*74}\nVERDICT\n{'='*74}")
    if best >= r8n:
        print(f"  WIN -- {best:.4f} >= RAG8 {r8n:.4f} under 3399 tokens, from CHANGING THE")
        print("  RETRIEVAL UNIT alone. No selector, reranker, or generation anywhere.")
    else:
        allb = max((sum(h for i, h, _ in r[t] if i in need)/len(need))
                   for t in ("DEF4", "DEF8", "DEF12") if t in r)
        print(f"  {'PART' if allb >= r8n else 'FAIL'} -- best under budget {best:.4f}, "
              f"best overall {allb:.4f}, vs RAG8 {r8n:.4f}.")
        print("  Definition units did not convert their granularity advantage into accuracy.")
