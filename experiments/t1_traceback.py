"""
T1 --- The runtime evidence was already in the bug report.

THE PIVOT
  Four harness iterations tried to PRODUCE execution traces (E1-E4). All died on
  environment fidelity: 131/133 non-reproductions were collection/import errors,
  because `pip install -e .` pulls modern deps against historical code. SWE-bench
  ships Docker images precisely for this, and replicating that would consume the
  budget on infrastructure rather than on the question.

  But 11.6% of SWE-bench Verified issues CONTAIN A PASTED PYTHON TRACEBACK. That is
  runtime evidence the reporter already collected: exact files and functions, zero
  execution, zero environment. A probe found the traceback names a gold file or
  function in 44/58 = 75.9% of those, against similarity retrieval's 27.5% recall@3.

WHY 75.9% IS NOT YET A RESULT
  (a) LOOSE: it counted a file match OR a symbol match, anywhere in the trace.
  (b) UNRANKED: any of a mean 8.3 frames counted, so it is really recall@8.
  (c) TRACES SHOW WHERE IT BLEW UP, NOT WHAT IS BROKEN. Sample django-10554: the
      trace is entirely db/utils.py machinery while gold is compiler.py/query.py.
      Astropy samples are exact; Django ones are not. That difference must be measured,
      not averaged over.

WHAT THIS MEASURES
  Gold = (file, symbol) pairs the reference patch edits, via innermost-AST mapping.
  Frames are ranked DEEPEST-FIRST (the error site, how a human reads a traceback) and
  also SHALLOWEST-FIRST as a control, since which end carries the signal is unknown.
  Reported: exact (file,symbol) recall@1/3/5/all, file-only recall, and per-repo split.

PRE-REGISTERED
  WIN  : exact recall@3 >= 0.425 on the traceback subset (the same bar E1-E4 carried),
         beating similarity's 0.2750 by >=15pp.
  PART : 0.275-0.425.
  FAIL : <= 0.275 -> tracebacks point at the crash site, not the defect, and add
         nothing over similarity.
  COVERAGE IS A SEPARATE AXIS and must not be blended into the headline: this signal
  exists for ~12% of instances. A hybrid would be "use the trace when present, else
  retrieve", so the honest claim is conditional-on-availability.
  I expect PART-to-WIN on exact@3 with a large spread by repo. Stating this first.

COST: Modal CPU only, no GPU, ~$0.10.
"""
import ast as A, json, os, re, subprocess, modal
image = (modal.Image.debian_slim(python_version="3.11").apt_install("git")
         .pip_install("datasets==3.0.1"))
app = modal.App("qcarve-t1-traceback")
data_vol = modal.Volume.from_name("qcarve-data", create_if_missing=True)
FRAME = re.compile(r'File "([^"]+)", line (\d+), in (\S+)')


def sh(c, cwd=None, t=600):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -9, ""


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


@app.function(image=image, timeout=5400, volumes={"/data": data_vol}, cpu=8.0)
def run():
    from datasets import load_dataset
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    rows = [r for r in ds if FRAME.search(r["problem_statement"] or "")]
    print(f"[subset] {len(rows)}/{len(ds)} instances have a pasted traceback")
    out = []
    for r in rows:
        slug = r["repo"].replace("/", "__"); d = "/tmp/" + slug
        if not os.path.exists(d):
            sh(["git", "clone", "--quiet", "--filter=blob:none",
                f"https://github.com/{r['repo']}", d], t=1200)
        if sh(["git", "checkout", "--quiet", "--force", r["base_commit"]], d)[0] != 0:
            continue
        # gold = (basename, symbol) the reference patch edits, innermost-AST
        cur, changed = None, {}
        for line in (r["patch"] or "").split("\n"):
            m = re.match(r"\+\+\+ b/(.+)", line)
            if m: cur = m.group(1)
            h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if h and cur and cur.endswith(".py"):
                st = int(h.group(1)); ln = int(h.group(2) or 1)
                changed.setdefault(cur, []).extend(range(st, st+max(1, ln)))
        gold = set()
        for f, lns in changed.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                try: src = open(p, encoding="utf-8", errors="ignore").read()
                except OSError: continue
                for s in innermost(src, lns): gold.add((os.path.basename(f), s))
        if not gold: continue
        fr = FRAME.findall(r["problem_statement"])
        frames = [(os.path.basename(f), s) for f, _, s in fr]
        out.append({"id": r["instance_id"], "repo": r["repo"],
                    "gold": sorted(f"{a}::{b}" for a, b in gold),
                    "gold_files": sorted({a for a, _ in gold}),
                    "frames_deep": [f"{a}::{b}" for a, b in frames[::-1]],
                    "frames_shallow": [f"{a}::{b}" for a, b in frames],
                    "frame_files_deep": [a for a, _ in frames[::-1]]})
    json.dump(out, open("/data/t1.json", "w")); data_vol.commit()
    print(f"[usable] {len(out)} with non-empty AST gold")
    return out


@app.local_entrypoint()
def main(out: str = "t1_results.json"):
    rows = run.remote(); json.dump(rows, open(out, "w"), indent=2)
    n = len(rows)
    if n < 12:
        print(f"\n  INCONCLUSIVE -- {n} usable < 12."); return
    import statistics as st
    from collections import Counter
    print(f"\n{'='*78}\nT1 -- TRACEBACK AS LOCALISER (n={n} instances with a pasted trace)\n{'='*78}")
    print(f"  frames per trace: mean {st.mean(len(w['frames_deep']) for w in rows):.1f}  "
          f"median {st.median(len(w['frames_deep']) for w in rows):.0f}")
    def rec(key, k, exact=True):
        h = 0
        for w in rows:
            cand = w[key][:k] if k else w[key]
            if exact: h += bool(set(w["gold"]) & set(cand))
            else:
                cf = {c.split("::")[0] for c in cand}
                h += bool(set(w["gold_files"]) & cf)
        return h/n
    print(f"\n  {'ordering':<22}{'@1':>8}{'@3':>8}{'@5':>8}{'all':>8}")
    print("-"*78)
    for lab, key in (("deepest-first (error)", "frames_deep"),
                     ("shallowest-first", "frames_shallow")):
        print(f"  {lab:<22}" + "".join(f"{rec(key,k):>8.3f}" for k in (1,3,5,None)))
    print(f"\n  file-only, deepest-first" + "".join(
        f"{rec('frames_deep',k,exact=False):>8.3f}" for k in (1,3,5,None)))
    best = max(rec("frames_deep",3), rec("frames_shallow",3))
    print(f"\n  similarity baseline (file-aware): recall@1 0.2062, @3 0.2750")
    print(f"\n  per-repo exact@3 (deepest-first):")
    for rp in sorted({w['repo'] for w in rows}):
        g = [w for w in rows if w['repo']==rp]
        v = sum(1 for w in g if set(w["gold"]) & set(w["frames_deep"][:3]))/len(g)
        print(f"    {rp:<28}{len(g):>4}{v:>9.3f}")
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if best >= 0.425:
        print(f"  WIN -- exact recall@3 = {best:.3f} vs similarity 0.2750 "
              f"({(best-0.275)*100:+.1f}pp), from evidence ALREADY IN THE BUG REPORT.")
    elif best > 0.275:
        print(f"  PART -- {best:.3f} vs 0.2750 ({(best-0.275)*100:+.1f}pp).")
    else:
        print(f"  FAIL -- {best:.3f} <= 0.2750. Traces mark the crash site, not the defect.")
    print(f"\n  COVERAGE (separate axis, do NOT blend): this signal exists for ~11.6% of")
    print(f"  instances. Any deployable use is 'trace when present, else retrieve'.")
