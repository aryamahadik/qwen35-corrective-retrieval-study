"""
N1 --- CONVERSION was never attacked. All 39 experiments used ONE prompt.

THE OVERSIGHT, STATED PLAINLY
  accuracy = P(gold retrieved) x P(correct | gold present) = 0.60 x 0.41 = 0.26
  Eighteen mechanisms attacked the first term. The second was measured, treated as a
  property of the EVIDENCE, and never manipulated. But every experiment used:
      "Which single function or class must be modified? Answer with ONLY the name,
       nothing else."   with max_tokens=24
  That prompt FORBIDS reasoning and forces a 1-of-~24 discriminative choice -- the
  exact operation this whole session proved the model cannot do. So P(C|G)=0.41 may
  be measuring SELECTION UNDER A FORMAT THAT BANS THINKING, not comprehension.

  Diagnostic support: of failures with gold in context, 41.1% name ANOTHER symbol
  defined in the SAME chunk (gold `run` -> said `make_shell_context`). Those are
  near-misses under forced choice, not misunderstanding.

THE INVERSIONS (evidence held constant; only the ASK changes)
  BASE     the incumbent prompt                          P(C|G)=0.4051 measured
  COT      reason first, then answer                      never tried; CoT is worth
                                                          10-30% on 7B reasoning tasks
  PATCH    "write the code change" -> extract the function from the diff.
           Converts discriminative SELECTION into GENERATION, which is what a code
           model is actually trained for. Localisation becomes a BYPRODUCT.
  TOP3     name 3 candidates, score if any is gold. Tests whether the model KNOWS but
           the single-answer format discards the information.
  Scored identically to every prior experiment (gold name appears in output).

ISOLATION
  Run ONLY on gold-present queries. Evidence is then constant by construction and any
  movement is attributable to the ASK. This is the cleanest conversion measurement
  possible and it has never been made.

PRE-REGISTERED
  WIN  : some format raises P(C|G) by >=8pp over 0.4051 -> conversion is a FORMAT
         artifact, and every downstream number in the programme is understated.
  PART : +3 to 8pp.
  FAIL : <3pp -> conversion really is an evidence/capability property and the
         incumbent prompt was not costing anything.
  TOP3 is expected to win trivially (3 guesses vs 1) and is reported SEPARATELY as a
  diagnostic of latent knowledge, NOT as a comparable result.
  I expect PART for COT and PATCH. Stating this before the run.

COST: A10G 7B, ~1600 generations, longer outputs for CoT/PATCH => ~$0.60.
NOTE: new Modal account -> corpus must be rebuilt first (empty volumes).
"""
import ast as A, json, os, re, subprocess, modal
CHUNK_TOK, APPROX, TOP_K, SEP = 512, 0.27, 8, "\n\n---\n\n"
EMB = "BAAI/bge-small-en-v1.5"
FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")
EXCL = ("test", "tests", "vendor", "docs")
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
app = modal.App("qcarve-n1-format")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-data", create_if_missing=True)

HEAD = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
        "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n")
ASKS = {
 "BASE": (HEAD + "Which single function or class must be modified to fix this bug?\n"
                 "Answer with ONLY the name, nothing else.", 24),
 "COT":  (HEAD + "Which single function or class must be modified to fix this bug?\n"
                 "Think step by step about what the report describes and which code "
                 "could produce it. Then end your reply with a final line of the form:\n"
                 "ANSWER: <name>", 400),
 "PATCH":(HEAD + "Write the minimal code change that fixes this bug. Output a unified "
                 "diff or the edited function, including the `def` or `class` line of "
                 "whatever you change. Output only code.", 400),
 "TOP3": (HEAD + "List the 3 functions or classes most likely to need modification, "
                 "most likely first, one per line. Names only.", 60),
}


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


@app.function(image=emb_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def build(per_repo=60):
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    emb = SentenceTransformer(EMB, device="cuda")
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    sh = lambda c, d=None: subprocess.run(c, cwd=d, capture_output=True, text=True).stdout
    items = []
    for nm, slug in REPOS.items():
        d = "/tmp/" + nm
        if not os.path.exists(d):
            sh(["git", "clone", "--quiet", "https://github.com/"+slug, d])
        sh(["git", "checkout", "--quiet", "--force", "HEAD"], d)
        files = [p for p in sh(["git", "ls-files"], d).split("\n")
                 if p.endswith(".py") and not any(f"/{x}/" in f"/{p.lower()}" for x in EXCL)]
        cont = {}
        for p in files:
            try: s = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if 200 < len(s) < 200_000: cont[p] = s
        if len(cont) < 8: continue
        ch, own = [], []
        n_ch = int(CHUNK_TOK/APPROX)
        for p, s in cont.items():
            for i in range(0, len(s), n_ch): ch.append(s[i:i+n_ch]); own.append(p)
        E = emb.encode(ch, batch_size=256, normalize_embeddings=True,
                       convert_to_numpy=True, show_progress_bar=False)
        bm = BM25Okapi([tk(c) for c in ch])
        cnt = 0
        log = sh(["git", "log", "--no-merges", "-n", "1500",
                  "--pretty=format:@@@%H|%B<<<E>>>"], d)
        for blk in log.split("@@@")[1:]:
            if cnt >= per_repo: break
            try: sha, rest = blk.split("|", 1)
            except ValueError: continue
            msg = rest.split("<<<E>>>")[0].strip().replace("\n", " ")[:900]
            if not any(w in msg.lower() for w in FIX) or len(msg) < 25: continue
            sh(["git", "checkout", "--quiet", "--force", sha], d)
            diff = sh(["git", "show", "--unified=0", "--format=", sha], d)
            cur, changed = None, {}
            for line in diff.split("\n"):
                m = re.match(r"\+\+\+ b/(.+)", line)
                if m: cur = m.group(1)
                h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
                if h and cur and cur.endswith(".py") and "test" not in cur.lower():
                    st = int(h.group(1)); ln = int(h.group(2) or 1)
                    changed.setdefault(cur, []).extend(range(st, st+max(1, ln)))
            gold = set()
            for f, lns in changed.items():
                p = os.path.join(d, f)
                if os.path.exists(p):
                    try: gold |= innermost(open(p, encoding="utf-8", errors="ignore").read(), lns)
                    except OSError: pass
            if not (1 <= len(gold) <= 5): continue
            qv = emb.encode([msg], normalize_embeddings=True, convert_to_numpy=True)[0]
            dr = [int(x) for x in np.argsort(-(E @ qv))]
            br = [int(x) for x in np.argsort(-bm.get_scores(tk(msg)))]
            sc = {}
            for r_, i in enumerate(dr[:200]): sc[i] = sc.get(i, 0) + 1/(60+r_+1)
            for r_, i in enumerate(br[:200]): sc[i] = sc.get(i, 0) + 1/(60+r_+1)
            idx = [int(j) for j in sorted(sc, key=lambda j: -sc[j])[:TOP_K]]
            items.append({"repo": nm, "sha": sha[:8], "query": msg,
                          "gold": sorted(gold), "chunks": [ch[i] for i in idx]})
            cnt += 1
        sh(["git", "checkout", "--quiet", "--force", "HEAD"], d)
        print(f"  {nm}: {cnt} queries")
    json.dump(items, open("/data/n1_items.json", "w")); data_vol.commit(); hf_cache.commit()
    return {"n": len(items)}


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/n1_items.json"))
    dfn = lambda t, g: bool(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", t))
    # ISOLATION: gold-present queries only -> evidence constant, ask varies
    G = [i for i, it in enumerate(items)
         if any(dfn(c, g) for c in it["chunks"] for g in it["gold"])]
    print(f"[isolate] {len(G)}/{len(items)} gold-present queries")
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer()
    out = {}
    for tag, (tpl, mx) in ASKS.items():
        sp = SamplingParams(temperature=0.0, max_tokens=mx)
        pr, nt = [], []
        for i in G:
            it = items[i]
            body = tpl.format(q=it["query"], e=SEP.join(it["chunks"]))
            pr.append(tok.apply_chat_template([{"role": "user", "content": body}],
                      tokenize=False, add_generation_prompt=True))
            nt.append(len(tok(body)["input_ids"]))
        res = llm.generate(pr, sp)
        recs = []
        for i, r, t in zip(G, res, nt):
            txt = r.outputs[0].text
            if tag == "COT":
                m = re.search(r"ANSWER:\s*(.+)", txt)
                txt = m.group(1) if m else txt[-200:]
            hit = int(any(re.search(rf"\b{re.escape(g)}\b", txt) for g in items[i]["gold"]))
            recs.append({"i": i, "hit": hit, "in_tok": t,
                         "out_tok": len(r.outputs[0].token_ids), "pred": txt.strip()[:120]})
        out[tag] = recs
        print(f"  {tag:<6} P(C|G)={sum(x['hit'] for x in recs)/len(recs):.4f}  "
              f"out_tok={sum(x['out_tok'] for x in recs)/len(recs):.0f}")
    hf_cache.commit()
    return {"model": model, "n_gold_present": len(G), "arms": out}


@app.local_entrypoint()
def main(out: str = "n1_results.json"):
    b = build.remote(); print(f"\ncorpus rebuilt: {b['n']} queries\n")
    r = run.remote(); json.dump(r, open(out, "w"), indent=2)
    A_ = r["arms"]; n = r["n_gold_present"]
    base = sum(x["hit"] for x in A_["BASE"])/n
    print(f"\n{'='*74}\nN1 -- CONVERSION BY ASK FORMAT (gold-present only, n={n})\n{'='*74}")
    print(f"  {'format':<8}{'P(C|G)':>10}{'vs BASE':>10}{'out tok':>10}")
    print("-"*74)
    for tag in ("BASE", "COT", "PATCH", "TOP3"):
        v = sum(x["hit"] for x in A_[tag])/n
        ot = sum(x["out_tok"] for x in A_[tag])/n
        note = "  <- diagnostic only (3 guesses)" if tag == "TOP3" else ""
        print(f"  {tag:<8}{v:>10.4f}{(v-base)*100:>9.1f}p{ot:>10.0f}{note}")
    best = max(sum(x["hit"] for x in A_[t])/n for t in ("COT", "PATCH"))
    print(f"\n  prior measurement of this quantity: 0.4051 (7B), 0.5105 (32B)")
    print(f"\n{'='*74}\nVERDICT\n{'='*74}")
    if best - base >= 0.08:
        print(f"  WIN -- {best:.4f} vs {base:.4f}. Conversion is substantially a FORMAT")
        print("  artifact. Every downstream number in the programme is understated.")
    elif best - base >= 0.03:
        print(f"  PART -- {(best-base)*100:+.1f}pp from changing only the ask.")
    else:
        print(f"  FAIL -- {(best-base)*100:+.1f}pp. Conversion is an evidence/capability")
        print("  property; the incumbent prompt was not costing anything.")
