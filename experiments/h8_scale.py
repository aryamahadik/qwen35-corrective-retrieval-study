"""
H7 --- Does the fast path lose ANSWER quality, or only PROXY quality?

THE JUMP
--------
H4/H5/H6 measured file-level retrieval recall and derived an oracle ceiling
1/(rho+e) = 2.05x < 4x. That ceiling has a PREMISE: quality == gold-file recall.
The goal's actual target is Delta = quality loss on ANSWERS.

Localisation recall is biased against the fast path in two concrete ways:
  1. gold sets from multi-file commits over-count (a fix touching 4 files scores a
     miss unless the retriever finds one of 4, but only 1 is usually causal);
  2. 3,900 tokens of diluted chunks is WORSE context for a model than 900 tokens of
     precise spans -- context dilution / lost-in-the-middle is a measured effect.
If either holds, Delta_answer << Delta_recall and the ceiling argument collapses.

HYPOTHESIS
----------
  H7: acc(FAST@3 spans) >= acc(RAG@8 chunks) - 1pp, at rho <= 0.25.

MATCHED CONTROL -- three arms, identical model, identical prompt, identical queries.
Only the evidence differs:
  A  RAG@8    8 x 512-tok chunks      ~3,900 tok   the strong baseline
  B  RAG@3    3 x 512-tok chunks      ~1,500 tok   TOKEN-MATCHED control
  C  FAST@3   3 function-level spans    ~900 tok   the fast path
Arm B is load-bearing: without it, a win for C cannot be attributed to SPANS
rather than merely to BREVITY.

GROUND TRUTH
------------
Gold = function/class names git itself reports as the enclosing context of each
changed hunk (`@@ -a,b +c,d @@ def NAME`). This is git's own funcname detection,
not my heuristic. Task: name the function that must change. Exact name match.

PRE-REGISTERED FALSIFICATION
----------------------------
  acc(A) - acc(C) >  1pp  => NO-GO CONFIRMED ON THE TRUE METRIC. Stop for real.
  acc(A) - acc(C) <= 1pp  => ceiling argument collapses; live candidate.
Stated before the run.

COST: A10G, ~15 min => ~$0.40.  NO MODEL RUNS ON THE PRINCIPAL'S MACHINE.
"""
import json, os, re, subprocess, modal

GPU = "A10G"
EMB_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "Qwen/Qwen2.5-14B-Instruct"

embed_image = (
    modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
llm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))

app = modal.App("qcarve-h8-scale")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

REPOS = ["https://github.com/pallets/flask", "https://github.com/encode/httpx",
         "https://github.com/pallets/click"]
FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")
EXCL = ("test", "tests", "vendor", "docs")
CHUNK_TOK, TOP_K_RAG, APPROX = 512, 8, 0.27

def _sh(c, cwd=None): return subprocess.run(c, cwd=cwd, capture_output=True, text=True).stdout
def _is_code(p):
    lo = p.lower()
    return not any(f"/{x}/" in f"/{lo}" for x in EXCL) and os.path.splitext(lo)[1] == ".py"
def _split_spans(t):
    L = t.split("\n"); b = [i for i, l in enumerate(L) if re.match(r"^\s{0,4}(def|class)\s", l)]
    if not b: return [t]
    b = [0] + b + [len(L)]
    return [s for s in ("\n".join(L[a:c]).strip() for a, c in zip(b[:-1], b[1:])) if s]
def _split_chunks(t):
    n = int(CHUNK_TOK / APPROX); return [t[i:i+n] for i in range(0, len(t), n)] or [t]


@app.function(image=embed_image, gpu=GPU, timeout=3000,
              volumes={"/hf": hf_cache, "/data": data_vol})
def build_evidence(per_repo=80):
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    emb = SentenceTransformer(EMB_MODEL, device="cuda")
    tokz = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    items = []

    for url in REPOS:
        name = url.rstrip("/").split("/")[-1]; d = f"/tmp/{name}"
        if not os.path.exists(d): _sh(["git", "clone", "--quiet", url, d])
        files = [p for p in _sh(["git","ls-files"], d).split("\n") if p and _is_code(p)]
        contents = {}
        for p in files:
            try:
                s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
                if 200 < len(s) < 200_000: contents[p] = s
            except OSError: pass
        if len(contents) < 8: continue

        chunks, chunk_owner, spans, span_owner = [], [], [], []
        for p, s in contents.items():
            for c in _split_chunks(s): chunks.append(c); chunk_owner.append(p)
            for c in _split_spans(s):  spans.append(c);  span_owner.append(p)

        E_c = emb.encode(chunks, batch_size=256, normalize_embeddings=True,
                         convert_to_numpy=True, show_progress_bar=False)
        E_s = emb.encode(spans,  batch_size=256, normalize_embeddings=True,
                         convert_to_numpy=True, show_progress_bar=False)
        bm_c, bm_s = BM25Okapi([tokz(c) for c in chunks]), BM25Okapi([tokz(c) for c in spans])

        def rrf(corpus, bm, E, q, k, kk=60):
            qv = emb.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
            dr = np.argsort(-(E @ qv)); br = np.argsort(-bm.get_scores(tokz(q)))
            sc = {}
            for r, i in enumerate(dr[:200]): sc[i] = sc.get(i, 0) + 1/(kk+r+1)
            for r, i in enumerate(br[:200]): sc[i] = sc.get(i, 0) + 1/(kk+r+1)
            return sorted(sc, key=lambda i: -sc[i])[:k]

        # queries: fix commits; gold = git's OWN funcname context on changed hunks
        log = _sh(["git","log","--no-merges","-n","1200","--pretty=format:@@@%H|%B<<<E>>>"], d)
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
            idx_r = rrf(chunks, bm_c, E_c, msg, TOP_K_RAG)
            idx_s = rrf(spans,  bm_s, E_s, msg, 3)
            items.append({
                "repo": name, "sha": sha[:8], "query": msg, "gold": sorted(gold),
                "RAG8":  "\n\n---\n\n".join(chunks[i] for i in idx_r),
                "RAG3":  "\n\n---\n\n".join(chunks[i] for i in idx_r[:3]),
                "FAST3": "\n\n---\n\n".join(spans[i]  for i in idx_s),
            })
            n += 1
        print(f"{name}: {n} queries, {len(contents)} files, {len(spans)} spans")

    with open("/data/h7_items.json", "w") as fh: json.dump(items, fh)
    data_vol.commit(); hf_cache.commit()
    return {"n_items": len(items), "per_repo": {r: sum(1 for i in items if i["repo"] == r)
                                                for r in {i["repo"] for i in items}}}


@app.function(image=llm_image, gpu="A100-40GB", timeout=3600,
              volumes={"/hf": hf_cache, "/data": data_vol})
def answer(model=LLM_MODEL):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h7_items.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=False, disable_log_stats=True)
    tok = llm.get_tokenizer()
    sp = SamplingParams(temperature=0.0, max_tokens=24)

    TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
           "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
           "Which single function or class must be modified to fix this bug?\n"
           "Answer with ONLY the name, nothing else.")

    out = {}
    for arm in ("RAG8", "RAG3", "FAST3"):
        prompts, ntoks = [], []
        for it in items:
            ev = it[arm]
            ids = tok(TPL.format(q=it["query"], e=ev))["input_ids"]
            if len(ids) > 7800:                       # truncate evidence, keep question
                ev = tok.decode(tok(ev)["input_ids"][:7800 - 400])
            p = TPL.format(q=it["query"], e=ev)
            prompts.append(tok.apply_chat_template([{"role": "user", "content": p}],
                                                   tokenize=False, add_generation_prompt=True))
            ntoks.append(len(tok(p)["input_ids"]))
        res = llm.generate(prompts, sp)
        recs = []
        for it, r, nt in zip(items, res, ntoks):
            txt = r.outputs[0].text.strip()
            hit = any(re.search(rf"\b{re.escape(g)}\b", txt) for g in it["gold"])
            recs.append({"repo": it["repo"], "sha": it["sha"], "hit": int(hit),
                         "n_tok": nt, "pred": txt[:60], "gold": it["gold"]})
        out[arm] = recs
        print(f"{arm}: acc={sum(r['hit'] for r in recs)/len(recs):.4f}  "
              f"mean_tok={sum(r['n_tok'] for r in recs)/len(recs):.0f}")
    hf_cache.commit()
    return {"model": model, "arms": out}


@app.local_entrypoint()
def main(out: str = "h8_results.json"):
    print(f"H8 -- DOES THE SLOPE FLATTEN WITH MODEL SCALE? LLM = {LLM_MODEL}\n")
    r = answer.remote()
    json.dump(r, open(out, "w"), indent=2)
    arms = r["arms"]; n = len(arms["RAG8"])
    acc = lambda a: sum(x["hit"] for x in arms[a]) / n
    tk  = lambda a: sum(x["n_tok"] for x in arms[a]) / n
    print(f"\n{'='*78}\nANSWER ACCURACY, n={n}, identical model/prompt/queries\n{'='*78}")
    print(f"{'arm':<8}{'accuracy':>10}{'mean tok':>10}{'tokens x':>10}{'D vs RAG8':>12}")
    print("-"*78)
    for a in ("RAG8", "RAG3", "FAST3"):
        print(f"{a:<8}{acc(a):>10.4f}{tk(a):>10.0f}{tk('RAG8')/tk(a):>9.2f}x"
              f"{(acc('RAG8')-acc(a))*100:>11.1f}pp")
    d = (acc("RAG8") - acc("FAST3")) * 100
    rho = tk("FAST3") / tk("RAG8")
    print(f"\n{'='*78}\nVERDICT (pre-registered: NO-GO confirmed if D > 1.0pp)\n{'='*78}")
    print(f"  Delta_answer = {d:.2f}pp     rho = {rho:.4f}  ({1/rho:.2f}x fewer tokens)")
    if d > 1.0:
        print("\n  NO-GO CONFIRMED ON THE TRUE METRIC. The proxy was not the problem.")
    else:
        print("\n  CEILING ARGUMENT COLLAPSES. Answer quality is preserved at "
              f"{1/rho:.2f}x fewer tokens.")
        print(f"  Attribution check -- RAG3 (token-matched) D = "
              f"{(acc('RAG8')-acc('RAG3'))*100:.2f}pp:")
        print("    if RAG3 also holds, the win is BREVITY. If only FAST3 holds, it is SPANS.")
    print(f"\n  per-repo Delta:")
    for rp in sorted({x['repo'] for x in arms['RAG8']}):
        f = lambda a: [x for x in arms[a] if x['repo'] == rp]
        m = len(f("RAG8"))
        print(f"    {rp:<7} n={m:<4} RAG8={sum(x['hit'] for x in f('RAG8'))/m:.3f}  "
              f"RAG3={sum(x['hit'] for x in f('RAG3'))/m:.3f}  "
              f"FAST3={sum(x['hit'] for x in f('FAST3'))/m:.3f}")
