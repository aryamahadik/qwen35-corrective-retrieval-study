"""
H19 --- Does H12's +19.2pp headline survive CORRECTED gold labels?

THE DEFECT
  Every result from H7 onward used gold from `git show`'s funcname on hunk headers,
  which reports the ENCLOSING CLASS for a method-level change. H18 proved the damage
  concretely: commit 7203feab was labelled ['Flask'] when the method actually changed
  was ['run']. Class-level gold is both too coarse (hub classes match trivially) and
  too strict (a model naming the correct METHOD scores wrong).

  H12/H15 were never re-run with corrected labels. Their within-model deltas should be
  robust (label noise is common-mode across arms) but that is an ARGUMENT, not a
  measurement. This measures it.

THE FIX
  Gold = innermost enclosing def/class of each CHANGED LINE in non-test files, via AST
  on the post-commit tree -- the same construction H18 validated.

ARMS (identical items, chunks, prompts, model; only the LABELS change)
  RAG8      full 8 chunks
  singleton oracle   best single chunk per query
  chance floor       best-of-N over chunks from a DIFFERENT query

PRE-REGISTERED
  HOLDS    : oracle - RAG8 stays >= +15pp  -> headline robust, report as is.
  WEAKENED : gap falls to +5..15pp          -> headline overstated, restate with the number.
  COLLAPSES: gap < +5pp                     -> H12's result was largely a label artifact
             and must be RETRACTED.
  I expect HOLDS. Noise is common-mode across arms and the oracle/RAG8 contrast is
  within-model. But H18 showed the defect is large, so this is a real test, and if it
  collapses I will say so plainly.

COST: CPU gold rebuild + A10G 7B ~2400 generations => ~$0.30.
"""
import ast as A, json, os, re, subprocess, modal
SEP = "\n\n---\n\n"
MODEL = "Qwen/Qwen2.5-7B-Instruct"

cpu_image = modal.Image.debian_slim(python_version="3.11").apt_install("git")
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h19-goldfix")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
REPOS = {"flask": "https://github.com/pallets/flask",
         "httpx": "https://github.com/encode/httpx",
         "click": "https://github.com/pallets/click"}


def sh(c, cwd=None, t=300):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -9, ""


def innermost(path, lines):
    try:
        tree = A.parse(open(path, encoding="utf-8", errors="ignore").read())
    except Exception:
        return set()
    spans = [(n.lineno, getattr(n, "end_lineno", n.lineno), n.name) for n in A.walk(tree)
             if isinstance(n, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef))]
    out = set()
    for l in lines:
        best = None
        for a, b, nm in spans:
            if a <= l <= b and (best is None or (b - a) < best[0]):
                best = (b - a, nm)
        if best:
            out.add(best[1])
    return out


@app.function(image=cpu_image, timeout=3600, volumes={"/data": data_vol}, cpu=4.0)
def rebuild_gold():
    items = json.load(open("/data/h7_items.json"))
    for nm, url in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            sh(["git", "clone", "--quiet", url, d])
    stats = {"total": 0, "changed": 0, "empty": 0, "same": 0}
    for it in items:
        stats["total"] += 1
        d = "/tmp/" + it["repo"]
        sh(["git", "checkout", "--quiet", "--force", it["sha"]], d)
        rc, diff = sh(["git", "show", "--unified=0", "--format=", it["sha"]], d)
        cur, changed = None, {}
        for line in diff.split("\n"):
            m = re.match(r"\+\+\+ b/(.+)", line)
            if m:
                cur = m.group(1)
            h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if h and cur and "test" not in cur.lower() and cur.endswith(".py"):
                st = int(h.group(1)); ln = int(h.group(2) or 1)
                changed.setdefault(cur, []).extend(range(st, st + max(1, ln)))
        g = set()
        for f, lns in changed.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                g |= innermost(p, lns)
        old = set(it["gold"])
        it["gold_ast"] = sorted(g) if g else sorted(old)
        if not g:
            stats["empty"] += 1
        elif g == old:
            stats["same"] += 1
        else:
            stats["changed"] += 1
    json.dump(items, open("/data/h19_items.json", "w")); data_vol.commit()
    ex = [(i["sha"], i["gold"], i["gold_ast"]) for i in items[:6]]
    return {"stats": stats, "examples": ex}


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def relabel(model=MODEL):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h19_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
           "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
           "Which single function or class must be modified to fix this bug?\n"
           "Answer with ONLY the name, nothing else.")
    prompts, key = [], []
    for i, it in enumerate(items):
        ch = it["RAG8"].split(SEP)
        alt = items[(i + 120) % n]["RAG8"].split(SEP)
        for k, c in enumerate(ch):
            prompts.append(TPL.format(q=it["query"], e=c)); key.append((i, "S", k))
        for k, c in enumerate(alt):
            prompts.append(TPL.format(q=it["query"], e=c)); key.append((i, "C", k))
        prompts.append(TPL.format(q=it["query"], e=it["RAG8"])); key.append((i, "R", 0))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in prompts]
    print(f"[plan] {len(chat)} generations")
    res = llm.generate(chat, sp)
    out = {"S": [[0]*8 for _ in range(n)], "C": [[0]*8 for _ in range(n)], "R": [0]*n,
           "S_old": [[0]*8 for _ in range(n)], "R_old": [0]*n}
    for (i, arm, k), r in zip(key, res):
        t = r.outputs[0].text
        new = int(any(re.search(rf"\b{re.escape(g)}\b", t) for g in items[i]["gold_ast"]))
        old = int(any(re.search(rf"\b{re.escape(g)}\b", t) for g in items[i]["gold"]))
        if arm == "R":
            out["R"][i] = new; out["R_old"][i] = old
        elif arm == "S":
            out["S"][i][k] = new; out["S_old"][i][k] = old
        else:
            out["C"][i][k] = new
    hf_cache.commit()
    return {"model": model, "n": n, **out}


@app.local_entrypoint()
def main(out: str = "h19_results.json"):
    b = rebuild_gold.remote()
    print(f"\ngold rebuild: {b['stats']}")
    for sha, old, new in b["examples"]:
        print(f"  {sha}  funcname={old}  ->  AST={new}")
    r = relabel.remote(); r["gold_stats"] = b["stats"]
    json.dump(r, open(out, "w"), indent=2)
    n = r["n"]
    S = lambda v: sum(v)/n
    rag_new, rag_old = S(r["R"]), S(r["R_old"])
    orc_new = S([max(x) for x in r["S"]]); orc_old = S([max(x) for x in r["S_old"]])
    chc_new = S([max(x) for x in r["C"]])
    print(f"\n{'='*76}\nH19 -- H12 HEADLINE UNDER CORRECTED GOLD, n={n}\n{'='*76}")
    print(f"  {'':<26}{'funcname gold':>16}{'AST gold':>12}")
    print("-"*76)
    print(f"  {'S_RAG8':<26}{rag_old:>16.4f}{rag_new:>12.4f}")
    print(f"  {'S_oracle (singletons)':<26}{orc_old:>16.4f}{orc_new:>12.4f}")
    print(f"  {'gap (oracle - RAG8)':<26}{(orc_old-rag_old)*100:>15.1f}p{(orc_new-rag_new)*100:>11.1f}p")
    print(f"  {'S_chance floor':<26}{'--':>16}{chc_new:>12.4f}")
    gap = (orc_new - rag_new) * 100
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if gap >= 15:
        print(f"  HOLDS -- gap {gap:+.1f}pp under corrected gold. H12's headline is robust;")
        print("  the label defect was common-mode across arms, as argued.")
    elif gap >= 5:
        print(f"  WEAKENED -- gap falls to {gap:+.1f}pp. H12 was overstated; restate at this value.")
    else:
        print(f"  COLLAPSES -- gap {gap:+.1f}pp. H12's result was largely a label artifact")
        print("  and the +19.2pp headline must be RETRACTED.")
