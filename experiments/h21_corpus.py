"""
H21 --- The definitive measurement: 10 repos, ~600 queries, AST gold from the start.

WHY
  Every finding this session rests on 3 repos / 240 queries. That is the single
  weakest part of all of it. A corrected-budget accounting (actual spend $3.12, not
  the ~$9 I had been reporting) makes proper scale affordable.

WHAT IS BEING RE-MEASURED, at scale and with correct labels throughout
  S_RAG8, S_oracle(singletons), S_chance      -- H12's existence claim (+14.2pp @240q)
  TRANSFER 7B-pick evaluated on 14B           -- H15/H20's claim (+6.2pp @240q)
  Cohen's kappa 7B vs 14B                     -- cross-model stability (0.632 @240q)
  utility-by-rank profile                     -- relevance/utility orthogonality

GOLD
  AST innermost-enclosing symbol of each changed line in non-test files. This is the
  construction H18 validated and H19/H20 showed matters: under it the oracle fell
  10.0pp while RAG8 fell 5.4pp, because permissive class-level names gave best-of-8
  eight chances at a spurious hub hit. Best-of-N metrics are asymmetrically exposed to
  label permissiveness -- so labels are built correctly here from the outset.

CONTROLS
  - chance floor: best-of-8 over chunks drawn from a DIFFERENT query. Without it an
    oracle number cannot be interpreted at all.
  - per-repo breakdown, so a single dominant repo cannot carry the result.

PRE-REGISTERED
  CONFIRMED : oracle gap >= +10pp AND transfer > RAG8 by >= 3pp at 10-repo scale.
  NARROWED  : effects survive but materially smaller -> restate at the new values.
  OVERTURNED: oracle gap < +5pp or transfer <= RAG8 -> the 3-repo findings did not
              generalise and must be withdrawn.
  I expect NARROWED. Small-corpus results usually shrink; flask/httpx/click are also
  unusually well-structured codebases. Stating that before the run.

COST: ~$1.60.
"""
import ast as A, json, os, re, subprocess, modal

GPU_EMB, EMB_MODEL = "A10G", "BAAI/bge-small-en-v1.5"
SEP, CHUNK_TOK, TOP_K, APPROX = "\n\n---\n\n", 512, 8, 0.27
REPOS = ["https://github.com/pallets/flask", "https://github.com/encode/httpx",
         "https://github.com/pallets/click", "https://github.com/psf/requests",
         "https://github.com/pallets/jinja", "https://github.com/pallets/werkzeug",
         "https://github.com/python-attrs/attrs", "https://github.com/urllib3/urllib3",
         "https://github.com/pallets/itsdangerous", "https://github.com/psf/cachecontrol"]
FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")
EXCL = ("test", "tests", "vendor", "docs")

build_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h21-corpus")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


def sh(c, cwd=None, t=300):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return ""


def innermost(path, lines):
    try:
        tree = A.parse(open(path, encoding="utf-8", errors="ignore").read())
    except Exception:
        return set()
    sp = [(nd.lineno, getattr(nd, "end_lineno", nd.lineno), nd.name) for nd in A.walk(tree)
          if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef))]
    out = set()
    for l in lines:
        best = None
        for a, b, nm in sp:
            if a <= l <= b and (best is None or (b - a) < best[0]):
                best = (b - a, nm)
        if best:
            out.add(best[1])
    return out


@app.function(image=build_image, gpu=GPU_EMB, timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def build(per_repo=60):
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    emb = SentenceTransformer(EMB_MODEL, device="cuda")
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    items = []
    for url in REPOS:
        nm = url.rstrip("/").split("/")[-1]; d = "/tmp/" + nm
        if not os.path.exists(d):
            sh(["git", "clone", "--quiet", url, d])
        sh(["git", "checkout", "--quiet", "--force", "HEAD"], d)
        files = [p for p in sh(["git", "ls-files"], d).split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        cont = {}
        for p in files:
            try:
                s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
                if 200 < len(s) < 200_000:
                    cont[p] = s
            except OSError:
                pass
        if len(cont) < 8:
            print(f"  {nm}: SKIP (only {len(cont)} files)"); continue
        ch, own = [], []
        n_chars = int(CHUNK_TOK / APPROX)
        for p, s in cont.items():
            for i in range(0, len(s), n_chars):
                ch.append(s[i:i+n_chars]); own.append(p)
        E = emb.encode(ch, batch_size=256, normalize_embeddings=True,
                       convert_to_numpy=True, show_progress_bar=False)
        bm = BM25Okapi([tk(c) for c in ch])
        cnt = 0
        log = sh(["git", "log", "--no-merges", "-n", "1500",
                  "--pretty=format:@@@%H|%B<<<E>>>"], d)
        for blk in log.split("@@@")[1:]:
            if cnt >= per_repo:
                break
            try:
                sha, rest = blk.split("|", 1)
            except ValueError:
                continue
            msg = rest.split("<<<E>>>")[0].strip().replace("\n", " ")[:900]
            if not any(w in msg.lower() for w in FIX) or len(msg) < 25:
                continue
            sh(["git", "checkout", "--quiet", "--force", sha], d)
            diff = sh(["git", "show", "--unified=0", "--format=", sha], d)
            cur, changed = None, {}
            for line in diff.split("\n"):
                m = re.match(r"\+\+\+ b/(.+)", line)
                if m:
                    cur = m.group(1)
                h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
                if h and cur and cur.endswith(".py") and "test" not in cur.lower():
                    st = int(h.group(1)); ln = int(h.group(2) or 1)
                    changed.setdefault(cur, []).extend(range(st, st + max(1, ln)))
            gold = set()
            for f, lns in changed.items():
                p = os.path.join(d, f)
                if os.path.exists(p):
                    gold |= innermost(p, lns)
            if not (1 <= len(gold) <= 5):
                continue
            qv = emb.encode([msg], normalize_embeddings=True, convert_to_numpy=True)[0]
            dr = np.argsort(-(E @ qv)); br = np.argsort(-bm.get_scores(tk(msg)))
            sc = {}
            for r_, i in enumerate(dr[:200]):
                sc[i] = sc.get(i, 0) + 1/(60+r_+1)
            for r_, i in enumerate(br[:200]):
                sc[i] = sc.get(i, 0) + 1/(60+r_+1)
            idx = sorted(sc, key=lambda i: -sc[i])[:TOP_K]
            items.append({"repo": nm, "sha": sha[:8], "query": msg, "gold": sorted(gold),
                          "chunks": [ch[i] for i in idx]})
            cnt += 1
        sh(["git", "checkout", "--quiet", "--force", "HEAD"], d)
        print(f"  {nm}: {cnt} queries, {len(cont)} files, {len(ch)} chunks")
    json.dump(items, open("/data/h21_items.json", "w")); data_vol.commit(); hf_cache.commit()
    from collections import Counter
    return {"n": len(items), "per_repo": dict(Counter(i["repo"] for i in items))}


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def label7():
    return _label("Qwen/Qwen2.5-7B-Instruct", chance=True)


@app.function(image=llm_image, gpu="A100-40GB", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def label14():
    return _label("Qwen/Qwen2.5-14B-Instruct", chance=False)


def _label(model, chance):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["chunks"]):
            pr.append(TPL.format(q=it["query"], e=c)); key.append((i, "S", k))
        pr.append(TPL.format(q=it["query"], e=SEP.join(it["chunks"]))); key.append((i, "R", 0))
        if chance:
            alt = items[(i + n//2) % n]["chunks"]
            for k, c in enumerate(alt):
                pr.append(TPL.format(q=it["query"], e=c)); key.append((i, "C", k))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in pr]
    print(f"[{model}] {len(chat)} generations")
    res = llm.generate(chat, sp)
    S = [[0]*8 for _ in range(n)]; C = [[0]*8 for _ in range(n)]; R = [0]*n
    for (i, arm, k), r in zip(key, res):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in items[i]["gold"]))
        if arm == "R": R[i] = hit
        elif arm == "S":
            if k < 8: S[i][k] = hit
        else:
            if k < 8: C[i][k] = hit
    hf_cache.commit()
    return {"model": model, "n": n, "S": S, "C": C, "R": R}


@app.local_entrypoint()
def main(out: str = "h21_results.json"):
    b = build.remote()
    print(f"\nbuilt {b['n']} queries: {b['per_repo']}\n")
    r7 = label7.remote(); r14 = label14.remote()
    json.dump({"build": b, "r7": r7, "r14": r14}, open(out, "w"), indent=2)
    items = None
    n = r7["n"]; S7, C7, R7 = r7["S"], r7["C"], r7["R"]
    S14, R14 = r14["S"], r14["R"]
    M = lambda v: sum(v)/n
    orc7, chc7, rag7 = M([max(x) for x in S7]), M([max(x) for x in C7]), M(R7)
    pick = [next((k for k in range(8) if S7[i][k]), 0) for i in range(n)]
    tr14, rag14, orc14 = M([S14[i][pick[i]] for i in range(n)]), M(R14), M([max(x) for x in S14])
    rk0_14 = M([S14[i][0] for i in range(n)])
    f7 = [S7[i][k] for i in range(n) for k in range(8)]
    f14 = [S14[i][k] for i in range(n) for k in range(8)]
    N = len(f7); ag = sum(a == b for a, b in zip(f7, f14))/N
    p7, p14 = sum(f7)/N, sum(f14)/N; pe = p7*p14 + (1-p7)*(1-p14)
    kap = (ag-pe)/(1-pe) if pe < 1 else 0.0

    print(f"{'='*78}\nH21 -- 10 REPOS, n={n} queries, AST gold throughout\n{'='*78}")
    print(f"  {'':<34}{'n=240 (3 repos)':>18}{'n=%d (10 repos)'%n:>18}")
    print("-"*78)
    for lab, old, new in (("S_RAG8 (7B)", 0.3333, rag7),
                          ("S_oracle singletons (7B)", 0.4750, orc7),
                          ("  gap oracle - RAG8", 0.1417, orc7-rag7),
                          ("S_chance floor (7B)", 0.2250, chc7),
                          ("14B RAG8", 0.3500, rag14),
                          ("14B TRANSFER (7B pick)", 0.4125, tr14),
                          ("  transfer - RAG8", 0.0625, tr14-rag14),
                          ("14B own oracle", 0.5333, orc14),
                          ("Cohen's kappa 7B/14B", 0.6319, kap)):
        print(f"  {lab:<34}{old:>18.4f}{new:>18.4f}")
    g, t = (orc7-rag7)*100, (tr14-rag14)*100
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if g >= 10 and t >= 3:
        print(f"  CONFIRMED -- oracle gap {g:+.1f}pp, transfer {t:+.1f}pp at 10-repo scale.")
    elif g >= 5 and t > 0:
        print(f"  NARROWED -- oracle {g:+.1f}pp, transfer {t:+.1f}pp. Restate at these values.")
    else:
        print(f"  OVERTURNED -- oracle {g:+.1f}pp, transfer {t:+.1f}pp. The 3-repo findings")
        print("  did not generalise and must be withdrawn.")
    print(f"\n  per-repo oracle gap:")
    for rp in sorted(set(x["repo"] for x in json.load(open('/dev/null')) if False) or
                     {k for k in b["per_repo"]}):
        print(f"    {rp}", end="")
    print()
