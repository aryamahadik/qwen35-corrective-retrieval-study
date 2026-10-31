"""
H17 (pilot) --- Does RUNTIME evidence identify the culprit where text cannot?

WHY, PRECISELY
  H12: a sufficient <=850-tok context EXISTS (+19.2pp over RAG8).
  H15: the target is STABLE across models (kappa 0.67); 14B on 7B's pick scores
       0.4000 @496 tok vs 0.3083 @3399 for RAG8.
  H13/H14/H16 + relevance + rank: SIX text-derived mechanisms recover almost none of
       the 30pp gap. Every one of them is a view of the same text similarity.
  Execution traces are the one NON-TEXT source available.

  Note on the earlier WORLD A gate: it showed content CONTAINS the signal (82% answer
  rate given a gold-defining chunk). It did NOT show the culprit is IDENTIFIABLE.
  Those are different questions and only the first was answered.

DESIGN -- the legitimate signal, no leakage
  For fix commit C with parent P:
    1. checkout P  (the buggy state)
    2. find test files C modified -- a fix usually lands its regression test
    3. run those tests AT P. They should FAIL. That failing test is the repro a real
       user would have. Using it is legitimate; using C's diff would be leakage.
    4. record the coverage trace of the failing test
    5. candidate context = functions executed by the failing test
  Then compare, at a MATCHED ~496-token budget, how often the context contains the
  gold symbol definition: TRACE-derived vs RAG8's top-8 chunks.

CHEAP GATE FIRST
  This run is CPU-only and computes COVERAGE, not answers. Generation happens only if
  trace context beats retrieval on gold containment. Cheap diagnostic gates the
  expensive confirmation.

PRE-REGISTERED
  GO : trace gold-containment at <=496 tok exceeds RAG8's by >=15pp -> run generation.
  NO : otherwise -> runtime evidence does not solve identification either; the
       programme concludes with a characterisation, not a mechanism.
  Reported honestly either way: the FUNNEL (checkout/install/test-found/test-fails/
  trace-captured), since attrition is the main risk and a small surviving n must not
  be presented as a clean result.

COST: Modal CPU only, ~$0.05.
"""
import json, os, re, subprocess, modal

image = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "build-essential")
    .pip_install("coverage==7.6.1", "pytest==8.3.3", "virtualenv==20.26.6"))
app = modal.App("qcarve-h17b-trace")
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

REPOS = ["https://github.com/pallets/flask", "https://github.com/pallets/click",
         "https://github.com/encode/httpx"]
MAX_COMMITS = 400


def sh(c, cwd=None, t=300):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT"


@app.function(image=image, timeout=5400, volumes={"/data": data_vol}, cpu=4.0)
def trace_pilot():
    all_rows = []
    funnel = {"considered": 0, "has_test_change": 0, "has_nontest_gold": 0,
              "checked_out": 0, "installed": 0, "test_ran": 0,
              "test_failed_at_parent": 0, "trace_captured": 0}
    rows = []
    FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")

    for REPO in REPOS:
      d = "/tmp/" + REPO.rstrip("/").split("/")[-1]
      if not os.path.exists(d): sh(["git", "clone", "--quiet", REPO, d])
      log = sh(["git", "log", "--no-merges", "-n", "900", "--pretty=format:@@@%H|%s"], d)[1]
      for blk in log.split("@@@")[1:]:
          if funnel["trace_captured"] >= 30: break
          if funnel["considered"] >= MAX_COMMITS: break
          try:
              sha, subj = blk.split("|", 1)
          except ValueError:
              continue
          sha = sha.strip(); subj = subj.split("\n")[0]
          if not any(w in subj.lower() for w in FIX):
              continue
          funnel["considered"] += 1

          rc, files = sh(["git", "show", "--name-only", "--format=", sha], d)
          tests = [f.strip() for f in files.split("\n")
                   if f.strip().endswith(".py") and "test" in f.strip().lower()]
          if not tests:
              continue
          funnel["has_test_change"] += 1

          # gold = symbols whose hunks the fix touched, in NON-test files
          rc, diff = sh(["git", "show", "--unified=0", "--format=", sha], d)
          gold = set()
          cur_test = False
          for line in diff.split("\n"):
              if line.startswith("+++ "):
                  cur_test = "test" in line.lower()
              m = re.match(r"@@ .*? @@\s*(?:async\s+)?(?:def|class)\s+(\w+)", line)
              if m and not cur_test:
                  gold.add(m.group(1))
          if not gold:
              continue
          funnel["has_nontest_gold"] += 1

          rc, _ = sh(["git", "checkout", "--quiet", "--force", sha + "^"], d)
          if rc != 0:
              continue
          funnel["checked_out"] += 1

          rc, out = sh(["pip", "install", "-e", ".", "-q", "--no-input"], d, t=420)
          if rc != 0:
              continue
          funnel["installed"] += 1

          # code stays at the parent; bring in the fix commit's TEST files only, so the
          # regression test actually exists and can fail. Without this the parent's older
          # test file simply passes and a valid repro is discarded.
          sh(["git", "checkout", sha, "--"] + tests, d)
          tgt = [t for t in tests if os.path.exists(os.path.join(d, t))]
          if not tgt:
              continue
          rc, out = sh(["python", "-m", "coverage", "run", "--branch", "-m",
                        "pytest", "-x", "-q"] + tgt, d, t=420)
          if "TIMEOUT" in out:
              continue
          funnel["test_ran"] += 1
          if rc == 0:
              continue                      # test passes at parent -> not a repro
          funnel["test_failed_at_parent"] += 1

          rc, cov = sh(["python", "-m", "coverage", "json", "-o", "/tmp/cov.json"], d)
          if rc != 0 or not os.path.exists("/tmp/cov.json"):
              continue
          try:
              C = json.load(open("/tmp/cov.json"))
          except Exception:
              continue
          executed = {}
          for f, info in C.get("files", {}).items():
              if "test" in f.lower():
                  continue
              ex = info.get("executed_lines", [])
              if ex:
                  executed[f] = set(ex)
          if not executed:
              continue
          funnel["trace_captured"] += 1

          # which executed functions? map executed lines -> enclosing def/class via AST
          import ast as A
          hit_syms = []
          for f, lines in executed.items():
              p = os.path.join(d, f)
              if not os.path.exists(p):
                  continue
              try:
                  src = open(p, encoding="utf-8", errors="ignore").read()
                  tree = A.parse(src)
              except Exception:
                  continue
              for node in A.walk(tree):
                  if isinstance(node, (A.FunctionDef, A.AsyncFunctionDef, A.ClassDef)):
                      a = node.lineno; b = getattr(node, "end_lineno", a)
                      n_ex = len([l for l in lines if a <= l <= b])
                      if n_ex:
                          hit_syms.append({"file": f, "name": node.name,
                                           "lines": b - a + 1, "executed": n_ex})
          hit_syms.sort(key=lambda s: -s["executed"])
          rows.append({"sha": sha[:8], "subject": subj[:90], "gold": sorted(gold),
                       "n_exec_syms": len(hit_syms), "top": hit_syms[:40]})
          print(f"  traced {sha[:8]}  gold={sorted(gold)}  exec_syms={len(hit_syms)}")

    json.dump({"funnel": funnel, "rows": rows}, open("/data/h17b_trace.json", "w"))
    data_vol.commit()
    return {"funnel": funnel, "rows": rows}


@app.local_entrypoint()
def main(out: str = "h17b_results.json"):
    r = trace_pilot.remote(); json.dump(r, open(out, "w"), indent=2)
    f = r["funnel"]; rows = r["rows"]
    print(f"\n{'='*76}\nH17 PILOT -- FUNNEL (attrition is the main risk; reported in full)\n{'='*76}")
    for k in ("considered", "has_test_change", "has_nontest_gold", "checked_out", "installed",
              "test_ran", "test_failed_at_parent", "trace_captured"):
        print(f"  {k:<26}{f[k]:>5}")
    if not rows:
        print("\n  NO TRACES CAPTURED -- pilot inconclusive, not a negative result.")
        return
    TOKS_PER_SYM = 496 / 3          # ~3 symbols fit a 496-token budget
    print(f"\n{'='*76}\nGOLD CONTAINMENT at a matched ~496-token budget\n{'='*76}")
    for topk in (1, 3, 5, 10, 40):
        hit = sum(1 for w in rows
                  if set(s["name"] for s in w["top"][:topk]) & set(w["gold"]))
        print(f"  trace top-{topk:<3} by executed-line count contains gold: "
              f"{hit}/{len(rows)} = {hit/len(rows):.1%}")
    anyhit = sum(1 for w in rows if set(s["name"] for s in w["top"]) & set(w["gold"]))
    print(f"\n  gold appears ANYWHERE in the executed trace: {anyhit}/{len(rows)} "
          f"= {anyhit/len(rows):.1%}   <- ceiling for trace-based selection")
    print(f"  mean executed symbols per repro: "
          f"{sum(w['n_exec_syms'] for w in rows)/len(rows):.0f}")
    print(f"\n  RAG8 reference (different corpus, 240 q): a gold-DEFINING chunk is present")
    print(f"  for 57.5% of queries; chunk-level gold containment was 6.0% of pairs.")
    top3 = sum(1 for w in rows if set(s["name"] for s in w["top"][:3]) & set(w["gold"]))/len(rows)
    print(f"\n{'='*76}\nGATE\n{'='*76}")
    if top3 >= 0.575 + 0.15:
        print(f"  GO -- trace top-3 gold containment {top3:.1%} clears the bar. Runtime")
        print("  evidence identifies the culprit far better than retrieval. Run generation.")
    else:
        print(f"  NO -- trace top-3 containment {top3:.1%} does not clear 72.5%.")
        print("  Runtime evidence does not solve identification at this budget either.")
