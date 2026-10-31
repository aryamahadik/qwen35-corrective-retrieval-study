"""
H18 --- Execution IDF: can runtime evidence RANK the culprit, not merely contain it?

WHAT WENT WRONG TWICE, STATED PLAINLY
  H17  : ran the PARENT's test file, which lacks the regression test, so it passed and
         valid repros were discarded. n=3. Inconclusive.
  H17b : brought the fix's test file onto parent code -> ImportError at COLLECTION.
         pytest exits non-zero, my check called that a repro, and coverage captured
         only ~15 module-import symbols. 16 of 25 captures were exactly 15 symbols.
         Both defects were mine, not properties of tracing.

  The 7 genuine traces were all ~370 symbols. Containing the culprit is easy;
  RANKING it into a 496-token (~3 symbol) budget is the real problem -- the same
  obstacle that defeated relevance, rerankers, learned utility, signatures and
  self-consistency.

THE IDEA
  Rank by EXECUTION IDF, not executed-line count. A symbol run by this repro but by
  few other tests is discriminative; one run by every test (Flask, Blueprint, Request)
  is not. Ranking by line count actively promotes those hubs, which is why raw
  containment looked high and meant nothing.
      idf(s) = log(T / (1 + tests_executing(s)))
  where T = number of background test files profiled.

THREE FIXES
  1. genuine failure only: parse pytest's summary and require "failed"; reject runs
     whose summary shows "error" (collection/import failure).
  2. AST gold: map the diff's changed LINE NUMBERS to the INNERMOST enclosing
     function, instead of git funcname's enclosing CLASS. This is the granularity
     defect that has been present since H7.
  3. hub control: report containment for non-hub gold separately, hub-ness measured
     empirically from the background profile.

PRE-REGISTERED
  n >= 8 usable repros required; below that this is INCONCLUSIVE and no number is
  reported. GO if IDF top-3 non-hub gold containment beats retrieval's 57.5% by
  >=15pp. Otherwise runtime evidence does not solve ranking either, and the
  programme concludes with a characterisation.

COST: Modal CPU only, ~$0.30.
"""
import ast as A, json, os, re, subprocess, math, modal

image = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "build-essential")
    .pip_install("coverage==7.6.1", "pytest==8.3.3"))
app = modal.App("qcarve-h18b-idf")
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
REPO = "https://github.com/pallets/flask"


def sh(c, cwd=None, t=420):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT"


def symbols_for(path, lines, body_only=True):
    """innermost enclosing def/class for each executed/changed line"""
    try:
        src = open(path, encoding="utf-8", errors="ignore").read(); tree = A.parse(src)
    except Exception:
        return {}
    spans = []
    for node in A.walk(tree):
        if isinstance(node, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
            # BODY only. coverage reports the `def foo():` header as executed at IMPORT
            # time, so including it makes every symbol look executed by every test
            # (272/274 "hubs"). Require a line strictly inside the body.
            if body_only:
                body = [c.lineno for c in getattr(node, "body", []) if hasattr(c, "lineno")]
                start = min(body) if body else node.lineno + 1
            else:
                start = node.lineno
            spans.append((start, getattr(node, "end_lineno", node.lineno), node.name))
    out = {}
    for l in lines:
        best = None
        for a, b, nm in spans:
            if a <= l <= b and (best is None or (b - a) < best[0]):
                best = (b - a, nm)          # INNERMOST = smallest span
        if best:
            out[best[1]] = out.get(best[1], 0) + 1
    return out


def cov_symbols(d, covfile="/tmp/c.json"):
    rc, _ = sh(["python", "-m", "coverage", "json", "-o", covfile], d)
    if rc != 0 or not os.path.exists(covfile):
        return {}
    try:
        C = json.load(open(covfile))
    except Exception:
        return {}
    syms = {}
    for f, info in C.get("files", {}).items():
        if "test" in f.lower():
            continue
        ex = info.get("executed_lines", [])
        p = os.path.join(d, f)
        if ex and os.path.exists(p):
            for nm, cnt in symbols_for(p, ex).items():
                syms[nm] = syms.get(nm, 0) + cnt
    return syms


@app.function(image=image, timeout=7200, volumes={"/data": data_vol}, cpu=4.0)
def pilot(max_commits=260, target=15, n_background=14):
    d = "/tmp/flask"
    if not os.path.exists(d):
        sh(["git", "clone", "--quiet", REPO, d])
    sh(["git", "checkout", "--quiet", "--force", "main"], d)
    sh(["pip", "install", "-e", ".", "-q", "--no-input"], d)

    # ---------- background profile: which symbols does EVERY test touch? ----------
    rc, tl = sh(["git", "ls-files", "tests"], d)
    tfiles = [t for t in tl.split("\n") if t.endswith(".py") and "test_" in t][:n_background]
    freq, T = {}, 0
    for t in tfiles:
        sh(["rm", "-f", ".coverage"], d)
        rc, out = sh(["python", "-m", "coverage", "run", "-m", "pytest", "-q", t], d, t=420)
        if "TIMEOUT" in out:
            continue
        s = cov_symbols(d)
        if not s:
            continue
        T += 1
        for nm in s:
            freq[nm] = freq.get(nm, 0) + 1
    print(f"[background] profiled {T} test files, {len(freq)} distinct symbols")
    hubs = {nm for nm, c in freq.items() if T and c / T > 0.5}
    print(f"[background] hub symbols (>50% of test files): {len(hubs)}")

    # ---------- repros ----------
    FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")
    log = sh(["git", "log", "--no-merges", "-n", "900", "--pretty=format:@@@%H|%s"], d)[1]
    fn = {"considered": 0, "test_change": 0, "ast_gold": 0, "installed": 0,
          "ran": 0, "genuine_fail": 0, "collection_error_rejected": 0, "traced": 0}
    rows = []
    for blk in log.split("@@@")[1:]:
        if fn["traced"] >= target or fn["considered"] >= max_commits:
            break
        try:
            sha, subj = blk.split("|", 1)
        except ValueError:
            continue
        sha = sha.strip(); subj = subj.split("\n")[0]
        if not any(w in subj.lower() for w in FIX):
            continue
        fn["considered"] += 1
        rc, files = sh(["git", "show", "--name-only", "--format=", sha], d)
        tests = [f.strip() for f in files.split("\n")
                 if f.strip().endswith(".py") and "test" in f.strip().lower()]
        srcs = [f.strip() for f in files.split("\n")
                if f.strip().endswith(".py") and "test" not in f.strip().lower()]
        if not tests or not srcs:
            continue
        fn["test_change"] += 1

        # ---- FIX 2: AST gold from changed line numbers, innermost symbol ----
        sh(["git", "checkout", "--quiet", "--force", sha], d)
        gold = {}
        rc, diff = sh(["git", "show", "--unified=0", "--format=", sha], d)
        cur, changed = None, {}
        for line in diff.split("\n"):
            m = re.match(r"\+\+\+ b/(.+)", line)
            if m:
                cur = m.group(1)
            h = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if h and cur and "test" not in cur.lower():
                st = int(h.group(1)); ln = int(h.group(2) or 1)
                changed.setdefault(cur, []).extend(range(st, st + max(1, ln)))
        for f, lns in changed.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                for nm in symbols_for(p, lns, body_only=False):
                    gold[nm] = 1
        if not gold:
            continue
        fn["ast_gold"] += 1

        sh(["git", "checkout", "--quiet", "--force", sha + "^"], d)
        rc, _ = sh(["pip", "install", "-e", ".", "-q", "--no-input"], d)
        if rc != 0:
            continue
        fn["installed"] += 1
        sh(["git", "checkout", sha, "--"] + tests, d)
        tgt = [t for t in tests if os.path.exists(os.path.join(d, t))]
        if not tgt:
            continue
        sh(["rm", "-f", ".coverage"], d)
        rc, out = sh(["python", "-m", "coverage", "run", "-m", "pytest", "-q"] + tgt, d)
        if "TIMEOUT" in out:
            continue
        fn["ran"] += 1
        # ---- FIX 1: genuine assertion failure, NOT a collection/import error ----
        tail = out[-1500:]
        n_failed = re.search(r"(\d+) failed", tail)
        n_error = re.search(r"(\d+) error", tail)
        if n_error and not n_failed:
            fn["collection_error_rejected"] += 1
            continue
        if not n_failed:
            continue
        fn["genuine_fail"] += 1

        syms = cov_symbols(d)
        if not syms:
            continue
        fn["traced"] += 1
        ranked_lines = sorted(syms, key=lambda s: -syms[s])
        ranked_idf = sorted(syms, key=lambda s: -(math.log(max(T,1) / (1 + freq.get(s, 0)))
                                                  * math.log(1 + syms[s])))
        rows.append({"sha": sha[:8], "gold": sorted(gold), "n_exec": len(syms),
                     "by_lines": ranked_lines[:25], "by_idf": ranked_idf[:25],
                     "nonhub_gold": sorted(set(gold) - hubs)})
        print(f"  repro {sha[:8]} gold={sorted(gold)[:4]} nonhub={sorted(set(gold)-hubs)[:4]} "
              f"exec={len(syms)}")
    json.dump({"funnel": fn, "rows": rows, "T": T, "n_hubs": len(hubs)},
              open("/data/h18b.json", "w")); data_vol.commit()
    return {"funnel": fn, "rows": rows, "T": T, "n_hubs": len(hubs)}


@app.local_entrypoint()
def main(out: str = "h18b_results.json"):
    r = pilot.remote(); json.dump(r, open(out, "w"), indent=2)
    f, rows = r["funnel"], r["rows"]
    print(f"\n{'='*74}\nH18 FUNNEL (background: {r['T']} test files, {r['n_hubs']} hubs)\n{'='*74}")
    for k, v in f.items():
        print(f"  {k:<28}{v:>5}")
    usable = [w for w in rows if w["nonhub_gold"]]
    print(f"\n  traced={len(rows)}   usable (has non-hub gold)={len(usable)}")
    if len(usable) < 8:
        print(f"\n  INCONCLUSIVE -- {len(usable)} usable repros is below the pre-registered")
        print("  minimum of 8. No containment number is reported; it would not be meaningful.")
        return
    print(f"\n{'='*74}\nRANKING: does execution IDF beat executed-line count?\n{'='*74}")
    for k in (1, 3, 5, 10):
        a = sum(1 for w in usable if set(w["by_lines"][:k]) & set(w["nonhub_gold"]))/len(usable)
        b = sum(1 for w in usable if set(w["by_idf"][:k]) & set(w["nonhub_gold"]))/len(usable)
        print(f"  top-{k:<3} non-hub gold containment:  by lines {a:.1%}   by IDF {b:.1%}")
    b3 = sum(1 for w in usable if set(w["by_idf"][:3]) & set(w["nonhub_gold"]))/len(usable)
    print(f"\n  retrieval reference: 57.5% of queries have a gold-defining chunk in RAG8's top-8")
    print(f"\n{'='*74}\nVERDICT\n{'='*74}")
    if b3 >= 0.725:
        print(f"  GO -- IDF top-3 reaches {b3:.1%}, clearing 72.5%. Runtime evidence RANKS")
        print("  the culprit where six text-derived mechanisms could not.")
    else:
        print(f"  NO -- IDF top-3 {b3:.1%} does not clear 72.5%. Runtime evidence contains")
        print("  but does not rank the culprit -- the same failure mode as everything else.")
