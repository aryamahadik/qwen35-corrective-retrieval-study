"""
H36 --- Can a SIGNATURE LIST serve as the evidence, with no source code at all?

THE UNEXAMINED ASSUMPTION
  Every experiment this session equated "evidence" with SOURCE CODE, because H31
  measured definitions: gold definition alone = 0.5486 @349 tok vs RAG8 0.2628 @3399.
  But the task's answer is a NAME. Recognising the right name in a list is a different
  and much cheaper operation than reading an implementation.

WHY NOW
  H35 (file-aware, so not the +14.2pp name-match artifact) showed signatures dominate
  the LOCALISATION curve: sig@50 = 0.5729 @1225 tok beats chunk@16 = 0.5542 @7928 tok,
  6.5x cheaper. But it does not convert: fetching 3 definitions off sig@3 costs ~1121
  tok for 0.2750 recall, worse than chunk@2 (0.3187 @991). The advantage sits at
  k=25-50 and harvesting it needs a localiser that 14 experiments say does not exist.

  Unless no definition is needed. A 25-signature list is 613 tokens and contains the
  gold symbol 50.2% of the time. If the model can pick from it, that bypasses both the
  localiser AND the definition fetch.

ARMS (identical model, prompt shape, and queries; evidence representation differs)
  SIG10/25/50   top-k signature records as the whole evidence      245/613/1225 tok
  SIGDEF25      25 signatures + the full definition of the top-1   ~960 tok
  RAG8          8 chunks                                            3399 tok (reference)

PRE-REGISTERED
  WIN  : some SIG arm >= RAG8's 0.2628 at fewer tokens.
  PART : beats chunk@2-equivalent (~0.19 accuracy at ~990 tok) but not RAG8.
  FAIL : signature lists are not usable evidence; the model cannot pick a name from a
         list any better than it can localise, and the recall advantage is unharvestable.
  Ceiling note: accuracy is bounded by file-aware recall (sig@25 = 0.5021), and H14
  showed picking among 8 signatures closed only 9.7% of the rank-0 -> oracle gap, so
  I expect PART, not WIN. Stating this before the run.

COST: A10G 7B, ~2200 generations => ~$0.25.
"""
import ast as A, json, os, re, subprocess, modal
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
app = modal.App("qcarve-h36-sigevidence")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

TPL = ("You are a code maintainer. Below is a bug report and an index of functions "
       "from the repository.\n\nBUG REPORT:\n{q}\n\nCANDIDATE FUNCTIONS:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


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
            a = nd.lineno-1; b = getattr(nd, "end_lineno", a+1)
            out.append((nd.name, rec, "\n".join(src.split("\n")[a:b])[:1900]))
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
        sg, defs = [], []
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for name, rec, body in sigs(p, s): sg.append(rec); defs.append(body)
        if len(sg) < 20: continue
        idx[nm] = (sg, defs, m.encode(sg, batch_size=256, normalize_embeddings=True,
                   convert_to_numpy=True, show_progress_bar=False),
                   BM25Okapi([tk(c) for c in sg]))
        print(f"  {nm}: {len(sg)} signatures")
    out = []
    for it in items:
        nm = it["repo"]
        if nm not in idx: out.append(None); continue
        sg, defs, E, bm = idx[nm]
        qv = m.encode([it["query"]], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = list(np.argsort(-(E @ qv))); br = list(np.argsort(-bm.get_scores(tk(it["query"]))))
        sc = {}
        for r_, j in enumerate(dr[:300]): sc[j] = sc.get(j, 0) + 1/(60+r_+1)
        for r_, j in enumerate(br[:300]): sc[j] = sc.get(j, 0) + 1/(60+r_+1)
        top = sorted(sc, key=lambda j: -sc[j])[:50]
        out.append({"sigs": [sg[j] for j in top], "top_def": defs[top[0]] if top else ""})
    json.dump(out, open("/data/h36_ctx.json", "w")); data_vol.commit(); hf_cache.commit()
    return {"n": sum(1 for x in out if x)}


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def answer(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json"))
    ctx = json.load(open("/data/h36_ctx.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key, nt = [], [], []
    for i, it in enumerate(items):
        c = ctx[i]
        if not c: continue
        for tag, ev in (("SIG10", "\n".join(c["sigs"][:10])),
                        ("SIG25", "\n".join(c["sigs"][:25])),
                        ("SIG50", "\n".join(c["sigs"][:50])),
                        ("SIGDEF25", "\n".join(c["sigs"][:25]) +
                         "\n\nFULL SOURCE OF THE TOP CANDIDATE:\n" + c["top_def"])):
            body = TPL.format(q=it["query"], e=ev)
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
def main(out: str = "h36_results.json"):
    b = build.remote(); print(f"  contexts built for {b['n']} items")
    r = answer.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json")); N = json.load(open("h24_results.json"))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = H["r7"]["n"]; null = N["NOCTX"]; P7 = H["r7"]["R"]
    need = set(i for i in range(n) if null[i] == 0 and repos[i] not in SMALL)
    real = set(i for i in range(n) if repos[i] not in SMALL)
    print(f"\n{'='*76}\nH36 -- SIGNATURE LIST AS EVIDENCE (no source code)\n{'='*76}")
    print(f"  {'arm':<12}{'tokens':>8}{'all real':>11}{'evidence-needed':>18}")
    print("-"*76)
    best = 0
    for tag in ("SIG10", "SIG25", "SIG50", "SIGDEF25"):
        v = r.get(tag, [])
        if not v: continue
        ar = [h for i, h, _ in v if i in real]; nd = [h for i, h, _ in v if i in need]
        t = sum(t for _, _, t in v)/len(v)
        a = sum(ar)/max(1, len(ar)); d = sum(nd)/max(1, len(nd))
        best = max(best, d)
        print(f"  {tag:<12}{t:>8.0f}{a:>11.4f}{d:>18.4f}")
    r8r = sum(P7[i] for i in real)/len(real); r8n = sum(P7[i] for i in need)/len(need)
    print(f"  {'RAG8':<12}{3399:>8}{r8r:>11.4f}{r8n:>18.4f}")
    print(f"\n  ceiling: file-aware sig@25 recall = 0.5021 (H35)")
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if best >= r8n:
        print(f"  WIN -- a signature list alone reaches {best:.4f} vs RAG8 {r8n:.4f},")
        print("  with NO source code. Localisation and evidence collapse into one cheap stage.")
    elif best >= 0.19:
        print(f"  PART -- {best:.4f} vs RAG8 {r8n:.4f}. Usable evidence, but below full RAG.")
    else:
        print(f"  FAIL -- {best:.4f}. A signature list is not usable evidence; the recall")
        print("  advantage at k=25-50 cannot be harvested.")
