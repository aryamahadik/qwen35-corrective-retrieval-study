"""
H29 --- ANSWER FIRST, THEN RETRIEVE. (and the cheap gate that decides if it can work)

THE INVERSION
  Ten mechanisms tried to pick the right chunk from a FIXED retrieval. All estimated
  P(useful | chunk) and all failed; the target is a delta function (63.4% of solvable
  queries have exactly ONE working chunk) and soft scores cannot hit it.

  But the measurements point somewhere else entirely:
    P(correct | chunk defines gold) = 0.819   -> find gold's DEFINITION and you are done
    model with ZERO evidence          = 0.183  -> its prior is real signal
    every model output IS a symbol name       -> exactly resolvable in a code index
    the bug report names gold only 20.4%      -> the REPORT is a bad retrieval key
  So use the model's own hypothesis as the key. Resolve it exactly, pull its
  NEIGHBOURHOOD (definition + callers + callees), answer again. No ranking, no
  selection, no delta function -- an exact lookup on generated text.

THE GATE (runs first, decides everything)
  When the model guesses WRONG, how far is the guess from gold in the call graph?
    dist 0  = guessed gold exactly
    dist 1  = guess directly calls, or is called by, gold   -> neighbourhood works
    dist 2  = two hops
    inf     = unrelated                                     -> the idea dies here
  If wrong guesses are mostly `inf`, hypothesis-driven retrieval cannot help and this
  reports that without spending on the pipeline.

ARMS (only run if the gate passes)
  BASE      RAG8, 3399 tok                             reference 0.2628 on need-subset
  HYP1      rank-1 chunk -> guess -> resolve guess's NEIGHBOURHOOD -> answer
  HYP0      zero context -> guess -> resolve neighbourhood -> answer  (pure prior seed)

PRE-REGISTERED
  GATE PASS : >=35% of wrong guesses are within 1 hop of gold.
  WIN       : HYP beats RAG8 (0.2628) at fewer tokens.
  FAIL      : otherwise; report the gate distribution, which is informative either way.
  I expect the gate to be marginal (~25-40%). Code call graphs are sparse and a wrong
  guess is often in a different subsystem entirely. Stating this before the run.

COST: A10G 7B, gate is CPU-ish + ~1700 generations => ~$0.25.
"""
import ast as A, json, os, re, modal
from collections import defaultdict, deque
SEP = "\n\n---\n\n"
llm_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h29-hypothesis")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

REPOS = {"flask": "https://github.com/pallets/flask", "httpx": "https://github.com/encode/httpx",
         "click": "https://github.com/pallets/click", "requests": "https://github.com/psf/requests",
         "jinja": "https://github.com/pallets/jinja", "werkzeug": "https://github.com/pallets/werkzeug",
         "attrs": "https://github.com/python-attrs/attrs", "urllib3": "https://github.com/urllib3/urllib3",
         "itsdangerous": "https://github.com/pallets/itsdangerous",
         "cachecontrol": "https://github.com/psf/cachecontrol"}
ASK = ("You are a code maintainer. A bug has been reported.\n\nBUG REPORT:\n{q}\n"
       "{ctx}\nWhich single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


def build_index(d):
    """symbol -> source text, and a call graph over symbol names."""
    defs, calls = {}, defaultdict(set)
    for root, _, files in os.walk(d):
        if any(x in root for x in ("/test", "/.git", "/docs")): continue
        for fn in files:
            if not fn.endswith(".py"): continue
            p = os.path.join(root, fn)
            try:
                src = open(p, encoding="utf-8", errors="ignore").read(); tree = A.parse(src)
            except Exception: continue
            lines = src.split("\n")
            for nd in A.walk(tree):
                if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
                    a = nd.lineno - 1; b = getattr(nd, "end_lineno", a + 1)
                    if nd.name not in defs:
                        defs[nd.name] = "\n".join(lines[a:b])[:2400]
                    for sub in A.walk(nd):
                        if isinstance(sub, A.Call):
                            f = sub.func
                            nm = getattr(f, "id", None) or getattr(f, "attr", None)
                            if nm and nm != nd.name:
                                calls[nd.name].add(nm); calls[nm].add(nd.name)
    return defs, calls


def hops(calls, src, tgts, cap=2):
    if not src or src in tgts: return 0
    seen = {src}; q = deque([(src, 0)])
    while q:
        u, dd = q.popleft()
        if dd >= cap: continue
        for v in calls.get(u, ()):
            if v in tgts: return dd + 1
            if v not in seen:
                seen.add(v); q.append((v, dd + 1))
    return 99


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(answers, model="Qwen/Qwen2.5-7B-Instruct"):
    import subprocess
    os.environ["HF_HOME"] = "/hf"
    items = json.load(open("/data/h21_items.json")); n = len(items)
    idx = {}
    for nm, url in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", url, d],
                           capture_output=True)
        idx[nm] = build_index(d)
        print(f"  index {nm}: {len(idx[nm][0])} symbols")
    norm = lambda t: (re.search(r"[A-Za-z_][\w.]*", (t or "").replace("`", "")).group(0)
                      .split(".")[-1] if re.search(r"[A-Za-z_][\w.]*",
                      (t or "").replace("`", "")) else "")

    # ---------- GATE: how far are WRONG guesses from gold in the call graph? ----------
    dist = defaultdict(int); n_wrong = 0
    for i, it in enumerate(items):
        defs, calls = idx[it["repo"]]
        g = set(it["gold"])
        guess = norm(answers[i][0])          # guess from the rank-1 chunk
        if not guess or guess in g: continue
        n_wrong += 1
        dist[hops(calls, guess, g)] += 1
    tot = max(1, n_wrong)
    within1 = (dist[1]) / tot
    print(f"\n[GATE] wrong guesses: {n_wrong}")
    for k in (1, 2, 99):
        print(f"  dist {k if k < 99 else 'unrelated':<10} {dist[k]:>5}  {dist[k]/tot:>6.1%}")
    print(f"  within 1 hop: {within1:.1%}   (pre-registered pass bar: 35%)")

    from vllm import LLM, SamplingParams
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)

    def neighbourhood(repo, sym, budget=1800):
        defs, calls = idx[repo]
        out, used = [], 0
        for s in [sym] + sorted(calls.get(sym, ()))[:6]:
            t = defs.get(s)
            if not t: continue
            t = t[:900]
            if used + len(t) > budget: break
            out.append(t); used += len(t)
        return SEP.join(out)

    # stage 1 guesses: HYP1 reuses the rank-1 answer we already have; HYP0 needs a pass
    pr0 = [ASK.format(q=it["query"], ctx="\n") for it in items]
    chat0 = [tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
             add_generation_prompt=True) for p in pr0]
    print(f"\n[stage1] {len(chat0)} zero-context guesses")
    g0 = [norm(o.outputs[0].text) for o in llm.generate(chat0, sp)]
    g1 = [norm(answers[i][0]) for i in range(n)]

    out = {}
    for tag, guesses in (("HYP0", g0), ("HYP1", g1)):
        pr, ntok = [], []
        for i, it in enumerate(items):
            ctx = neighbourhood(it["repo"], guesses[i])
            body = ASK.format(q=it["query"],
                              ctx=f"\nCODE NEAR YOUR HYPOTHESIS `{guesses[i]}`:\n{ctx}\n")
            pr.append(body); ntok.append(len(tok(body)["input_ids"]))
        chat = [tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
                add_generation_prompt=True) for p in pr]
        print(f"[stage2:{tag}] {len(chat)} generations")
        res = llm.generate(chat, sp)
        out[tag] = {"hit": [int(any(re.search(rf"\b{re.escape(x)}\b", o.outputs[0].text)
                                    for x in items[i]["gold"]))
                            for i, o in enumerate(res)],
                    "tok": sum(ntok)/len(ntok)}
    hf_cache.commit()
    return {"model": model, "n": n, "gate": {str(k): v for k, v in dist.items()},
            "n_wrong": n_wrong, "within1": within1, "arms": out}


@app.local_entrypoint()
def main(out: str = "h29_results.json"):
    H = json.load(open("h21_results.json")); H23 = json.load(open("h23_results.json"))
    N = json.load(open("h24_results.json"))
    r = run.remote(H23["answers"]); json.dump(r, open(out, "w"), indent=2)
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = r["n"]; null = N["NOCTX"]; P7 = H["r7"]["R"]; S7 = H["r7"]["S"]
    need = [i for i in range(n) if null[i] == 0 and repos[i] not in SMALL]
    f = lambda v: sum(v[i] for i in need)/len(need)
    rag8 = f(P7); rk1 = f([S7[i][0] for i in range(n)])
    orc = sum(max(S7[i]) for i in need)/len(need)
    print(f"\n{'='*76}\nH29 -- ANSWER FIRST, THEN RETRIEVE (n={len(need)} evidence-needed)\n{'='*76}")
    print(f"  GATE: {r['within1']:.1%} of wrong guesses are within 1 call-graph hop of gold")
    print(f"\n  {'arm':<28}{'score':>9}{'tokens':>9}{'vs RAG8':>10}")
    print("-"*76)
    print(f"  {'rank-1 chunk':<28}{rk1:>9.4f}{496:>9}{(rk1-rag8)*100:>9.1f}p")
    for tag in ("HYP0", "HYP1"):
        a = r["arms"][tag]; v = f(a["hit"])
        lab = "zero-ctx guess -> neighbourhood" if tag == "HYP0" else "rank-1 guess -> neighbourhood"
        print(f"  {lab:<28}{v:>9.4f}{a['tok']:>9.0f}{(v-rag8)*100:>9.1f}p")
    print(f"  {'RAG8':<28}{rag8:>9.4f}{3399:>9}{0.0:>9.1f}p")
    print(f"  {'ORACLE single chunk':<28}{orc:>9.4f}{496:>9}{(orc-rag8)*100:>9.1f}p")
    best = max(f(r["arms"][t]["hit"]) for t in ("HYP0", "HYP1"))
    bt = max(("HYP0", "HYP1"), key=lambda t: f(r["arms"][t]["hit"]))
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if best > rag8:
        print(f"  WIN -- {bt} reaches {best:.4f} vs RAG8 {rag8:.4f} at "
              f"{3399/r['arms'][bt]['tok']:.2f}x fewer tokens.")
        print("  Hypothesis-driven retrieval beats fixed retrieval. Selection is bypassed.")
    elif best > rk1:
        print(f"  PARTIAL -- {best:.4f} beats rank-1 ({rk1:.4f}) but not RAG8 ({rag8:.4f}).")
    else:
        print(f"  FAIL -- {best:.4f}. The model's hypothesis is not a better retrieval key.")
