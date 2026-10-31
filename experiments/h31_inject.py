"""
H31 --- IDENTIFY the recall headroom by INTERVENTION, not observation.

THE CONFOUND
  Both my decomposition and the reviewer's estimate recall headroom by comparing
  gold-PRESENT queries to gold-ABSENT ones:
      v(recall) = RAG8 on gold-present  = 0.4051
      v(both)   = oracle on gold-present = 0.5696
  But presence is NOT random. Measured on the 392 evidence-needed queries:
      report names gold:  16.9% (present)  vs  4.5% (absent)   -- 3.8x
      gold symbols:        1.91 (present)  vs  1.34 (absent)
  Gold is retrieved precisely when the bug report names it -- i.e. when the answer is
  in the question. That is missing-not-at-random: the present subset is intrinsically
  easier for the SAME reason retrieval succeeded there. So "if recall were perfect"
  is not identified by that comparison, and the recall term is inflated more than the
  selection term.

THE INTERVENTION
  For the 155 gold-ABSENT queries, FORCE gold's definition into the context and
  measure. This is a do-operation, not a conditional, so it identifies the quantity
  both decompositions were estimating.

ARMS (gold-absent queries only)
  ABSENT_NOW      their current RAG8 context            reference, 0.0452
  ABSENT_GOLD1    gold's definition alone (~500 tok)    matched to oracle-single
  ABSENT_GOLD8    gold's definition + 7 retrieved chunks (RAG8-sized, gold swapped in)
  and for calibration, the same two arms on gold-PRESENT queries.

WHAT IT DECIDES
  If ABSENT_GOLD1 ~= 0.5696 (the present-subset oracle), the headroom is real and the
  Shapley numbers stand.
  If ABSENT_GOLD1 << 0.5696, absent queries stay hard even with perfect recall, the
  recall term is inflated, and the pivot is weaker than both of us claimed.

PRE-REGISTERED
  CONFIRMED : ABSENT_GOLD1 >= 0.45  -> recall headroom largely real.
  INFLATED  : 0.25-0.45              -> partially confounded; restate lower.
  ILLUSORY  : < 0.25                 -> recall headroom is mostly the confound.
  I expect INFLATED. The 3.8x gap in "report names gold" is large, and a report that
  never names the culprit is hard even when you hand over the right code.
  Stating this before the run.

COST: A10G 7B, ~800 generations => ~$0.10.
"""
import ast as A, json, os, re, subprocess, modal
SEP = "\n\n---\n\n"
llm_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h31-inject")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
REPOS = {"flask": "pallets/flask", "httpx": "encode/httpx", "click": "pallets/click",
         "requests": "psf/requests", "jinja": "pallets/jinja",
         "werkzeug": "pallets/werkzeug", "attrs": "python-attrs/attrs",
         "urllib3": "urllib3/urllib3"}
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(need, present, model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    items = json.load(open("/data/h21_items.json"))
    # index gold definitions (ALL duplicates kept, unlike build_index)
    defs = {}
    for nm, slug in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                            "https://github.com/" + slug, d], capture_output=True)
        dd = {}
        for root, _, fs in os.walk(d):
            if any(x in root for x in ("/test", "/.git", "/docs")): continue
            for fn in fs:
                if not fn.endswith(".py"): continue
                p = os.path.join(root, fn)
                try:
                    src = open(p, encoding="utf-8", errors="ignore").read(); t = A.parse(src)
                except Exception: continue
                L = src.split("\n")
                for nd in A.walk(t):
                    if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
                        a = nd.lineno-1; b = getattr(nd, "end_lineno", a+1)
                        dd.setdefault(nd.name, []).append("\n".join(L[a:b])[:1900])
        defs[nm] = dd
    from vllm import LLM, SamplingParams
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pres = set(present)
    pr, key, ntok = [], [], []
    skipped = 0
    for i in need:
        it = items[i]; dd = defs.get(it["repo"], {})
        gd = None
        for g in it["gold"]:
            if g in dd:
                gd = dd[g][0]; break
        if gd is None:
            skipped += 1; continue
        grp = "PRESENT" if i in pres else "ABSENT"
        for tag, ev in (("GOLD1", gd),
                        ("GOLD8", SEP.join([gd] + it["chunks"][:7]))):
            body = TPL.format(q=it["query"], e=ev)
            pr.append(body); key.append((i, f"{grp}_{tag}")); ntok.append(
                len(tok(body)["input_ids"]))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
            add_generation_prompt=True) for p in pr]
    print(f"[plan] {len(chat)} generations ({skipped} queries skipped: gold not in index)")
    res = llm.generate(chat, sp)
    out = {}
    for (i, tag), r, t in zip(key, res, ntok):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in items[i]["gold"]))
        out.setdefault(tag, []).append((i, hit, t))
    hf_cache.commit()
    return {"model": model, "out": out, "skipped": skipped}


@app.local_entrypoint()
def main(out: str = "h31_results.json"):
    H = json.load(open("h21_results.json")); N = json.load(open("h24_results.json"))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    items = json.load(open("/tmp/h21_items.json"))
    n = H["r7"]["n"]; S7 = H["r7"]["S"]; P7 = H["r7"]["R"]; null = N["NOCTX"]
    need = [i for i in range(n) if null[i] == 0 and repos[i] not in SMALL]
    dfn = lambda c, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c))
    present = [i for i in need if any(dfn(c, g) for c in items[i]["chunks"]
                                      for g in items[i]["gold"])]
    absent = [i for i in need if i not in set(present)]
    r = run.remote(need, present); json.dump(r, open(out, "w"), indent=2)
    O = r["out"]
    m = lambda tag: (sum(h for _, h, _ in O.get(tag, []))/max(1, len(O.get(tag, []))),
                     len(O.get(tag, [])),
                     sum(t for _, _, t in O.get(tag, []))/max(1, len(O.get(tag, []))))
    f = lambda v, ix: sum(v[i] for i in ix)/len(ix)
    print(f"\n{'='*78}\nH31 -- FORCED GOLD INJECTION (do-operation)\n{'='*78}")
    print(f"  skipped {r['skipped']} queries whose gold symbol is absent from the index\n")
    print(f"  {'condition':<34}{'score':>9}{'n':>6}{'tokens':>9}")
    print("-"*78)
    print(f"  {'ABSENT: current RAG8':<34}{f(P7,absent):>9.4f}{len(absent):>6}{3399:>9}")
    for tag, lab in (("ABSENT_GOLD1", "ABSENT: gold definition ALONE"),
                     ("ABSENT_GOLD8", "ABSENT: gold + 7 chunks")):
        s, c, t = m(tag); print(f"  {lab:<34}{s:>9.4f}{c:>6}{t:>9.0f}")
    print(f"  {'PRESENT: current RAG8':<34}{f(P7,present):>9.4f}{len(present):>6}{3399:>9}")
    for tag, lab in (("PRESENT_GOLD1", "PRESENT: gold definition ALONE"),
                     ("PRESENT_GOLD8", "PRESENT: gold + 7 chunks")):
        s, c, t = m(tag); print(f"  {lab:<34}{s:>9.4f}{c:>6}{t:>9.0f}")
    oracle_present = sum(max(S7[i]) for i in present)/len(present)
    a1 = m("ABSENT_GOLD1")[0]
    print(f"\n  reference: oracle on gold-PRESENT = {oracle_present:.4f}")
    print(f"             (this is the 0.5696 both decompositions assumed)")
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if a1 >= 0.45:
        print(f"  CONFIRMED -- forcing gold in lifts absent queries to {a1:.4f},")
        print("  close to the present-subset oracle. Recall headroom is largely real.")
    elif a1 >= 0.25:
        print(f"  INFLATED -- {a1:.4f} vs the assumed {oracle_present:.4f}. Absent queries")
        print("  stay harder even with perfect recall. Restate recall headroom LOWER:")
        print(f"  true ceiling ~= {(len(present)*oracle_present+len(absent)*a1)/len(need):.4f}, "
              f"not {oracle_present:.4f}.")
    else:
        print(f"  ILLUSORY -- {a1:.4f}. Recall headroom is mostly the confound;")
        print("  handing over the right code does not help when the report never names it.")
