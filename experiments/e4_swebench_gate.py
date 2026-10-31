"""
E2 --- FEASIBILITY GATE: can we actually reproduce and trace SWE-bench Verified tasks?

WHY THIS AND NOT ANOTHER SCORER
  Static retrieval + prompting is exhausted. 18 mechanisms on recall, 4 formats on
  conversion (N1: BASE .5017, COT .4917, PATCH .5446 p=.237 n.s., TOP3 diagnostic).
  Conversion is robust to prompt format and improves mainly with model capability.
  Execution is the one remaining INDEPENDENT information source: it ELIMINATES
  candidates instead of ranking them.

WHY THE PREVIOUS TRACE PILOT DIED
  Git-mined commits: 1036 considered -> 157 touched tests -> 114 with AST gold ->
  6 genuine reproductions. The precondition (a test that actually fails at the parent)
  held for ~0.6% of commits. SWE-bench Verified ships human-validated reproductions
  (FAIL_TO_PASS) specifically to supply it.

THIS RUN MEASURES A FUNNEL, NOT ACCURACY
  loaded -> cloned -> installed -> test patch applied -> FAIL_TO_PASS actually FAILS
  -> coverage captured -> executed-function set extracted
  Then, on survivors:
      |executed set|                     how much execution narrows the space
      gold in executed set?              can runtime evidence SEE the culprit
      recall@1/3/5 under cheap rankings  can it RANK the culprit
  Gold = innermost enclosing def/class of each line the reference patch changes
  (the same AST construction used throughout, which fixed a 14.2pp name-match bias).

REPO FILTER
  Restricted to light-install repos (requests/flask/click/pylint/pytest/sphinx-ish).
  numpy/scipy-heavy repos (sympy, scikit-learn, matplotlib, astropy, xarray, seaborn)
  are excluded HERE only because historical builds of them are slow, not because they
  are uninteresting. Attrition is reported in full either way.

PRE-REGISTERED KILL CRITERION
  GO   : >=12 instances reach a captured trace AND execution-derived recall@3 beats
         similarity retrieval's file-aware 0.2750 by >=15pp (i.e. >=0.425).
  WEAK : traces captured but recall@3 in 0.275-0.425.
  STOP : <12 usable instances, or recall@3 <= 0.2750 -> execution adds nothing over
         similarity and the whole line closes.
  I expect the funnel to be the binding risk, not the signal: historical installs are
  where this died last time. Stating that before the run.

COST: Modal CPU only (no GPU), ~$0.50.
"""
import ast as A, json, os, re, subprocess, modal

image = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "build-essential")
    .pip_install("datasets==3.0.1", "coverage==7.6.1", "pytest==8.3.3"))
app = modal.App("qcarve-e4-swebench-gate")
data_vol = modal.Volume.from_name("qcarve-data", create_if_missing=True)
# E1b DIAGNOSIS: 8/10 failures were collection/import errors, not detection bugs.
# The 2 that worked were 2020/2022 commits; the 8 that failed were 2012-2015 (requests
# from 2012 targets Python 2.7 and cannot import under 3.11). So the binding constraint
# is PYTHON-ERA, not repo weight. Drop the light-repo filter, add a recency filter.
MIN_YEAR = 2019
# E2 RUN-1 EXPOSED A DESIGN FLAW, NOT A HANG: in the 2019+ window the pool is
#   django 227 | sympy 49 | sphinx 44 | matplotlib 34 | sklearn 24 | xarray 22
#   pytest 19 | astropy 18 | pylint 10 | seaborn 2
# django is 50% of it AND does not use pytest -- its FAIL_TO_PASS ids are
# "test_x (module.Class)", not pytest node ids, so this harness cannot run any of them.
# matplotlib/sklearn/astropy need compiled numerical builds (slow, often fail from source).
# Keep the pytest-native, pure-Python-ish repos.
PYTEST_NATIVE = ("sympy", "sphinx", "pytest-dev", "pylint", "xarray", "seaborn")


def sh(c, cwd=None, t=600):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT"


def innermost(src, lines):
    try: tree = A.parse(src)
    except Exception: return set()
    sp = [(n.lineno, getattr(n, "end_lineno", n.lineno), n.name) for n in A.walk(tree)
          if isinstance(n, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef))]
    out = set()
    for l in lines:
        best = None
        for a, b, nm in sp:
            if a <= l <= b and (best is None or (b - a) < best[0]): best = (b - a, nm)
        if best: out.add(best[1])
    return out


def patch_targets(patch, root):
    """(file, symbol) pairs the reference patch actually edits"""
    cur, changed = None, {}
    for line in patch.split("\n"):
        m = re.match(r"\+\+\+ b/(.+)", line)
        if m: cur = m.group(1)
        h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if h and cur and cur.endswith(".py") and not (
                any(x in ("test", "tests", "testing")
                    for x in cur.replace("\\", "/").split("/")[:-1])
                or cur.split("/")[-1].startswith("test_")):
            st = int(h.group(1)); ln = int(h.group(2) or 1)
            changed.setdefault(cur, []).extend(range(st, st + max(1, ln)))
    out = set()
    for f, lns in changed.items():
        p = os.path.join(root, f)
        if os.path.exists(p):
            try: src = open(p, encoding="utf-8", errors="ignore").read()
            except OSError: continue
            for s in innermost(src, lns): out.add((f, s))
    return out


@app.function(image=image, timeout=7200, volumes={"/data": data_vol}, cpu=8.0)
def gate(n_target=30):
    from datasets import load_dataset
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    def yr(r):
        try: return int(str(r.get("created_at", ""))[:4])
        except Exception: return 0
    rows = [r for r in ds if yr(r) >= MIN_YEAR
            and any(k in r["repo"].lower() for k in PYTEST_NATIVE)]
    from collections import Counter
    print(f"[dataset] {len(ds)} verified, {len(rows)} pytest-native from {MIN_YEAR}+")
    print(f"[dataset] year spread (all): "
          f"{sorted(Counter(yr(r) for r in ds).items())}")
    print(f"[dataset] repos in window: {Counter(r['repo'] for r in rows).most_common(10)}")

    nonrep = []
    fn = {"considered": 0, "cloned": 0, "installed": 0, "patched": 0,
          "test_ran": 0, "genuine_fail": 0, "traced": 0}
    out = []
    for r in rows:
        if fn["traced"] >= n_target: break
        fn["considered"] += 1
        slug = r["repo"].replace("/", "__")
        d = f"/tmp/{slug}"
        if not os.path.exists(d):
            rc, _ = sh(["git", "clone", "--quiet", "--filter=blob:none",
                        f"https://github.com/{r['repo']}", d], t=900)
            if rc != 0: continue
        rc, _ = sh(["git", "checkout", "--quiet", "--force", r["base_commit"]], d)
        if rc != 0: continue
        fn["cloned"] += 1
        rc, log = sh(["pip", "install", "-e", ".", "-q", "--no-input"], d, t=900)
        if rc != 0:
            rc, log = sh(["pip", "install", "-e", ".[test]", "-q", "--no-input"], d, t=900)
        if rc != 0:
            continue
        sh(["pip", "install", "-q", "--no-input", "pytest-xdist", "hypothesis"], d, t=300)
        fn["installed"] += 1
        # apply ONLY the test patch: code stays buggy, tests become the reproduction
        with open("/tmp/tp.diff", "w") as fh: fh.write(r["test_patch"])
        rc, _ = sh(["git", "apply", "--whitespace=nowarn", "/tmp/tp.diff"], d)
        if rc != 0: continue
        fn["patched"] += 1
        try: f2p = json.loads(r["FAIL_TO_PASS"])
        except Exception: f2p = []
        if not f2p: continue
        sh(["rm", "-f", ".coverage"], d)
        rc, log = sh(["python", "-m", "coverage", "run", "--branch", "-m",
                      "pytest", "-q", "-p", "no:cacheprovider"] + f2p[:3], d, t=900)
        if "TIMEOUT" in log: continue
        fn["test_ran"] += 1
        tail = log[-2000:]
        nf = re.search(r"(\d+) failed", tail); ne = re.search(r"(\d+) error", tail)
        if not nf:
            cls = ("collection/import error" if ne or re.search(
                       r"ERROR|ImportError|ModuleNotFound|during collection", tail)
                   else "no tests collected" if re.search(
                       r"no tests ran|collected 0", tail)
                   else "tests PASSED" if re.search(r"\d+ passed", tail)
                   else "unknown")
            nonrep.append({"id": r["instance_id"], "class": cls,
                           "f2p0": (f2p[0] if f2p else "")[:80], "tail": tail[-300:]})
            continue
        fn["genuine_fail"] += 1
        rc, _ = sh(["python", "-m", "coverage", "json", "-o", "/tmp/c.json"], d)
        if rc != 0 or not os.path.exists("/tmp/c.json"): continue
        try: C = json.load(open("/tmp/c.json"))
        except Exception: continue
        execed = {}
        def is_testfile(p):
            parts = p.replace("\\", "/").split("/")
            return (any(x in ("test", "tests", "testing") for x in parts[:-1])
                    or parts[-1].startswith("test_") or parts[-1].endswith("_test.py"))
        for f, info in C.get("files", {}).items():
            if is_testfile(f): continue
            ex = info.get("executed_lines", [])
            p = os.path.join(d, f)
            if not ex or not os.path.exists(p): continue
            try: src = open(p, encoding="utf-8", errors="ignore").read()
            except OSError: continue
            try: tree = A.parse(src)
            except Exception: continue
            for nd in A.walk(tree):
                if isinstance(nd, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
                    body = [c.lineno for c in getattr(nd, "body", []) if hasattr(c, "lineno")]
                    st = min(body) if body else nd.lineno + 1
                    en = getattr(nd, "end_lineno", st)
                    hits = len([l for l in ex if st <= l <= en])
                    if hits:
                        execed[(f, nd.name)] = execed.get((f, nd.name), 0) + hits
        if not execed: continue
        fn["traced"] += 1
        gold = patch_targets(r["patch"], d)
        out.append({"id": r["instance_id"], "repo": r["repo"],
                    "gold": sorted(f"{a}::{b}" for a, b in gold),
                    "n_exec": len(execed),
                    "exec": sorted(((f"{a}::{b}", c) for (a, b), c in execed.items()),
                                   key=lambda t: -t[1])[:80]})
        sh(["git", "checkout", "--quiet", "--force", r["base_commit"]], d)
        print(f"  traced {r['instance_id']}  gold={len(gold)} exec_syms={len(execed)}")
    from collections import Counter
    print(f"[nonrep] {len(nonrep)} ran but did not reproduce: "
          f"{Counter(x['class'] for x in nonrep).most_common()}")
    json.dump({"funnel": fn, "rows": out, "nonrep": nonrep[:40]},
              open("/data/e4.json", "w")); data_vol.commit()
    return {"funnel": fn, "rows": out, "nonrep": nonrep[:40]}


@app.local_entrypoint()
def main(out: str = "e4_results.json"):
    r = gate.remote(); json.dump(r, open(out, "w"), indent=2)
    f, rows = r["funnel"], r["rows"]
    print(f"\n{'='*74}\nE4 FUNNEL (test-path bug fixed + non-repro diagnosis) (attrition reported in full)\n{'='*74}")
    for k in ("considered", "cloned", "installed", "patched", "test_ran",
              "genuine_fail", "traced"):
        print(f"  {k:<18}{f[k]:>5}")
    from collections import Counter
    nr = r.get("nonrep", [])
    if nr:
        print(f"\n  WHY 'ran but did not reproduce' (n={len(nr)} sampled):")
        for k, v in Counter(x["class"] for x in nr).most_common():
            print(f"    {k:<28}{v:>4}")
        for x in nr[:3]:
            print(f"\n    --- {x['id']} [{x['class']}] f2p0={x['f2p0'][:60]}")
            print("       " + x["tail"].replace("\n", "\n       ")[:340])
    usable = [w for w in rows if w["gold"]]
    print(f"\n  traced={len(rows)}  with non-empty gold={len(usable)}")
    if len(usable) < 12:
        print(f"\n  STOP (funnel) -- {len(usable)} usable < 12 pre-registered minimum.")
        print("  No recall number reported; it would not be meaningful.")
        return
    import statistics as st
    print(f"\n{'='*74}\nDOES EXECUTION SEE THE CULPRIT?\n{'='*74}")
    print(f"  mean executed symbols per repro: {st.mean(w['n_exec'] for w in usable):.0f}")
    print(f"  median                         : {st.median(w['n_exec'] for w in usable):.0f}")
    anyhit = sum(1 for w in usable if set(w["gold"]) & {s for s, _ in w["exec"]})
    print(f"  gold ANYWHERE in executed set  : {anyhit}/{len(usable)} = {anyhit/len(usable):.1%}")
    print(f"\n  {'ranking':<26}{'@1':>8}{'@3':>8}{'@5':>8}{'@10':>8}")
    print("-"*74)
    for lab, key in (("by executed-line count", lambda w: [s for s, _ in w["exec"]]),):
        rec = {}
        for k in (1, 3, 5, 10):
            rec[k] = sum(1 for w in usable if set(w["gold"]) & set(key(w)[:k]))/len(usable)
        print(f"  {lab:<26}" + "".join(f"{rec[k]:>8.3f}" for k in (1, 3, 5, 10)))
    r3 = sum(1 for w in usable if set(w["gold"]) & {s for s, _ in w["exec"][:3]})/len(usable)
    print(f"\n  similarity baseline (file-aware, prior corpus): recall@1 0.2062, @3 0.2750")
    print(f"\n{'='*74}\nGATE\n{'='*74}")
    if r3 >= 0.425:
        print(f"  GO -- execution recall@3 = {r3:.3f}, beating similarity's 0.2750 by "
              f"{(r3-0.275)*100:+.1f}pp.")
        print("  Runtime evidence is a genuinely better localiser. Build the pipeline.")
    elif r3 > 0.275:
        print(f"  WEAK -- {r3:.3f} vs 0.2750 ({(r3-0.275)*100:+.1f}pp). Real but under the bar.")
    else:
        print(f"  STOP -- {r3:.3f} <= 0.2750. Execution does not beat similarity at")
        print("  localisation, and the execution line closes.")
