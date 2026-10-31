"""
T2 --- Trace-guided fetch: same recall, 6.8x fewer tokens. Does it hold end-to-end?

THE ARITHMETIC T1 EXPOSED
  On the traceback subset (58 instances), exact (file,symbol) recall:
      top-3 traceback frames : 0.310    ~3 functions   ~500 tok
      similarity RAG8        : 0.2750   8 chunks      ~3400 tok
  Comparable recall at 6.8x fewer evidence tokens. That IS the >=4x token target --
  IF it survives generation.

WHY NOT FULL EXECUTION INSTEAD
  A traceback is the execution path AT THE MOMENT OF FAILURE: ~8 frames, already
  ordered by causality. Full coverage (E1/E3 measured 109-350 executed symbols) is a
  SUPERSET -- better "gold appears anywhere", far worse ranking. Since the most
  concentrated 8 frames contain gold only 44.8% of the time, 350 noisier ones will not
  rank it better. Docker-faithful execution buys fidelity, not signal.

ARMS (same 58 instances, same model, same prompt, same scorer)
  RAG8      8 similarity chunks from the repo at base_commit   ~3400 tok
  TRACE3    source of the 3 DEEPEST traceback frames            ~500 tok
  TRACE5    source of the 5 deepest frames                      ~850 tok
  HYBRID    3 deepest frames + 2 top similarity chunks          ~1400 tok
  Evidence for trace arms is the FULL FUNCTION SOURCE at each frame, fetched by
  (file, line) -> innermost enclosing def/class.

PRE-REGISTERED
  WIN  : a trace arm matches RAG8 accuracy within 1pp at <=850 tok (>=4x reduction).
  PART : within 3pp at <=850 tok.
  FAIL : >3pp worse -> the recall parity does not survive generation.
  Coverage stays a SEPARATE axis: this applies to the ~11.6% of issues carrying a
  traceback, so any claim is conditional-on-availability, never a replacement for RAG.
  n=58 is small; a 1pp difference is <1 instance, so I will report McNemar and treat
  sub-3pp gaps as ties rather than wins.

COST: A10G 7B + CPU indexing, ~$0.45.
"""
import ast as A, json, os, re, subprocess, modal
SEP = "\n\n---\n\n"
CHUNK_TOK, APPROX = 512, 0.27
EMB = "BAAI/bge-small-en-v1.5"
FRAME = re.compile(r'File "([^"]+)", line (\d+), in (\S+)')
emb_image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
    .pip_install("datasets==3.0.1", "torch==2.5.1", "sentence-transformers==3.3.1",
                 "transformers==4.48.3", "rank-bm25==0.2.2", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-t2-tracefetch")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


def sh(c, cwd=None, t=900):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -9, ""


def enclosing(src, line):
    try: tree = A.parse(src)
    except Exception: return None
    best = None
    for n in A.walk(tree):
        if isinstance(n, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
            a, b = n.lineno, getattr(n, "end_lineno", n.lineno)
            if a <= line <= b and (best is None or (b-a) < best[0]): best = (b-a, a, b, n.name)
    if not best: return None
    L = src.split("\n")
    return "\n".join(L[best[1]-1:best[2]])[:2400], best[3]


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
              volumes={"/hf": hf_cache, "/data": data_vol}, cpu=8.0)
def build():
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from datasets import load_dataset
    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    m = SentenceTransformer(EMB, device="cuda")
    tk = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    rows = [r for r in ds if FRAME.search(r["problem_statement"] or "")]
    print(f"[subset] {len(rows)} instances with a traceback")
    out = []
    for r in rows:
        d = "/tmp/" + r["repo"].replace("/", "__")
        if not os.path.exists(d):
            sh(["git", "clone", "--quiet", "--filter=blob:none",
                f"https://github.com/{r['repo']}", d], t=1500)
        if sh(["git", "checkout", "--quiet", "--force", r["base_commit"]], d)[0] != 0:
            continue
        # gold
        cur, changed = None, {}
        for line in (r["patch"] or "").split("\n"):
            mm = re.match(r"\+\+\+ b/(.+)", line)
            if mm: cur = mm.group(1)
            h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if h and cur and cur.endswith(".py"):
                st = int(h.group(1)); ln = int(h.group(2) or 1)
                changed.setdefault(cur, []).extend(range(st, st+max(1, ln)))
        gold = set()
        for f, lns in changed.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                try: gold |= innermost(open(p, encoding="utf-8", errors="ignore").read(), lns)
                except OSError: pass
        if not gold: continue
        # trace-guided fetch: deepest frames first, resolve file+line -> enclosing function
        frames = FRAME.findall(r["problem_statement"])[::-1]
        tsrc = []
        for fp, ln, _ in frames:
            cand = [p for p in sh(["git", "ls-files", "--", f"*{os.path.basename(fp)}"], d)[1].split("\n") if p]
            if not cand: continue
            p = os.path.join(d, cand[0])
            if not os.path.exists(p): continue
            try: src = open(p, encoding="utf-8", errors="ignore").read()
            except OSError: continue
            e = enclosing(src, int(ln))
            if e: tsrc.append(f"# {cand[0]}\n{e[0]}")
            if len(tsrc) >= 5: break
        if not tsrc: continue
        # similarity index over the repo at this commit
        files = [p for p in sh(["git", "ls-files"], d)[1].split("\n")
                 if p.endswith(".py") and not any(x in p.split("/")[:-1]
                 for x in ("test", "tests", "testing"))]
        ch = []; nch = int(CHUNK_TOK/APPROX)
        for p in files[:4000]:
            fp = os.path.join(d, p)
            try: s = open(fp, encoding="utf-8", errors="ignore").read()
            except OSError: continue
            if not (200 < len(s) < 200_000): continue
            for i in range(0, len(s), nch): ch.append(s[i:i+nch])
        if len(ch) < 8: continue
        E = m.encode(ch, batch_size=256, normalize_embeddings=True,
                     convert_to_numpy=True, show_progress_bar=False)
        bm = BM25Okapi([tk(c) for c in ch])
        q = (r["problem_statement"] or "")[:1500]
        qv = m.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
        dr = [int(x) for x in np.argsort(-(E @ qv))]
        br = [int(x) for x in np.argsort(-bm.get_scores(tk(q)))]
        sc = {}
        for i2, j in enumerate(dr[:200]): sc[j] = sc.get(j, 0) + 1/(60+i2+1)
        for i2, j in enumerate(br[:200]): sc[j] = sc.get(j, 0) + 1/(60+i2+1)
        top = [int(j) for j in sorted(sc, key=lambda j: -sc[j])[:8]]
        out.append({"id": r["instance_id"], "repo": r["repo"], "query": q,
                    "gold": sorted(gold), "trace": tsrc,
                    "chunks": [ch[j] for j in top]})
        print(f"  built {r['instance_id']}  gold={len(gold)} frames={len(tsrc)}")
    json.dump(out, open("/data/t2_ctx.json", "w")); data_vol.commit(); hf_cache.commit()
    return {"n": len(out)}


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def answer(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    ctx = json.load(open("/data/t2_ctx.json"))
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=16384,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    arms = {"RAG8": lambda c: SEP.join(c["chunks"]),
            "TRACE3": lambda c: SEP.join(c["trace"][:3]),
            "TRACE5": lambda c: SEP.join(c["trace"][:5]),
            "HYBRID": lambda c: SEP.join(c["trace"][:3] + c["chunks"][:2])}
    pr, key, nt = [], [], []
    for i, c in enumerate(ctx):
        for tag, f in arms.items():
            body = TPL.format(q=c["query"], e=f(c))
            ids = tok(body)["input_ids"]
            if len(ids) > 15000: body = tok.decode(ids[:15000])
            pr.append(tok.apply_chat_template([{"role": "user", "content": body}],
                      tokenize=False, add_generation_prompt=True))
            key.append((i, tag)); nt.append(min(len(ids), 15000))
    print(f"[plan] {len(pr)} generations over {len(ctx)} instances")
    res = llm.generate(pr, sp)
    out = {}
    for (i, tag), r, t in zip(key, res, nt):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in ctx[i]["gold"]))
        out.setdefault(tag, []).append({"i": i, "hit": hit, "tok": t})
    hf_cache.commit()
    return out


@app.local_entrypoint()
def main(out: str = "t2_results.json"):
    b = build.remote(); print(f"\ncontexts: {b['n']}\n")
    r = answer.remote(); json.dump(r, open(out, "w"), indent=2)
    from math import comb
    n = len(r["RAG8"])
    print(f"{'='*76}\nT2 -- TRACE-GUIDED FETCH (n={n}, traceback subset)\n{'='*76}")
    print(f"  {'arm':<9}{'accuracy':>10}{'tokens':>9}{'x vs RAG8':>11}{'vs RAG8':>10}")
    print("-"*76)
    base = sum(x["hit"] for x in r["RAG8"])/n
    bt = sum(x["tok"] for x in r["RAG8"])/n
    for tag in ("RAG8", "TRACE3", "TRACE5", "HYBRID"):
        v = sum(x["hit"] for x in r[tag])/n; t = sum(x["tok"] for x in r[tag])/n
        print(f"  {tag:<9}{v:>10.4f}{t:>9.0f}{bt/t:>10.2f}x{(v-base)*100:>9.1f}p")
    print(f"\n  McNemar vs RAG8:")
    for tag in ("TRACE3", "TRACE5", "HYBRID"):
        f={x["i"]:x["hit"] for x in r[tag]}; g={x["i"]:x["hit"] for x in r["RAG8"]}
        bb=sum(1 for k in f if f[k] and not g[k]); cc=sum(1 for k in f if g[k] and not f[k])
        m=bb+cc; k=min(bb,cc)
        p=min(1.0,2*sum(comb(m,j) for j in range(k+1))/2**m) if m else 1.0
        print(f"    {tag:<8}{bb}/{cc} discordant, p={p:.4f}"
              + ("  (n small: treat <3pp as a tie)" if p>=0.05 else ""))
    best = max((sum(x["hit"] for x in r[t])/n, sum(x["tok"] for x in r[t])/n, t)
               for t in ("TRACE3", "TRACE5"))
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if best[0] >= base - 0.01 and best[1] <= 850:
        print(f"  WIN -- {best[2]} matches RAG8 within 1pp at {best[1]:.0f} tok "
              f"({bt/best[1]:.1f}x reduction).")
    elif best[0] >= base - 0.03:
        print(f"  PART -- {best[2]} within 3pp at {best[1]:.0f} tok ({bt/best[1]:.1f}x).")
    else:
        print(f"  FAIL -- {(best[0]-base)*100:+.1f}pp; recall parity did not survive generation.")
    print(f"\n  COVERAGE: applies to ~11.6% of issues (those carrying a traceback).")
