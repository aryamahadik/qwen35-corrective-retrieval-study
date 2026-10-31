"""
E1b --- WHY did only 6/77 SWE-bench Verified instances produce a genuine failure?

These are HUMAN-VERIFIED reproductions. Applying the test patch to unfixed code should
fail by construction. Two candidate causes, and they have opposite implications:

  (a) MY DETECTION is wrong again -- pytest summary parsed incorrectly, or the
      FAIL_TO_PASS node IDs are not valid pytest selectors in that checkout.
      -> cheap fix, gate re-runs.
  (b) ENVIRONMENT INFIDELITY -- `pip install -e .` pulls MODERN dependencies against
      HISTORICAL code, so tests ERROR on import instead of FAILING on assertion.
      My filter correctly rejects errors, so they never count as reproductions.
      -> needs per-instance environments (SWE-bench ships Docker images), which is a
      real cost, not a bug.

This captures the ACTUAL pytest tail for 10 instances and classifies it, instead of
guessing. No pre-registration needed: it is a diagnostic, not a hypothesis test.
"""
import json, os, re, subprocess, modal
image = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "build-essential")
    .pip_install("datasets==3.0.1", "coverage==7.6.1", "pytest==8.3.3"))
app = modal.App("qcarve-e1b-diag")
LIGHT = ("requests", "flask", "click", "pylint", "pytest", "sphinx", "jinja", "werkzeug")


def sh(c, cwd=None, t=600):
    try:
        p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=t)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT"


@app.function(image=image, timeout=5400, cpu=8.0)
def diag(n=10):
    from datasets import load_dataset
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    rows = [r for r in ds if any(k in r["repo"].lower() for k in LIGHT)][:n]
    out = []
    for r in rows:
        slug = r["repo"].replace("/", "__"); d = f"/tmp/{slug}"
        if not os.path.exists(d):
            sh(["git", "clone", "--quiet", f"https://github.com/{r['repo']}", d], t=900)
        sh(["git", "checkout", "--quiet", "--force", r["base_commit"]], d)
        rc_i, _ = sh(["pip", "install", "-e", ".", "-q", "--no-input"], d, t=900)
        with open("/tmp/tp.diff", "w") as fh: fh.write(r["test_patch"])
        rc_p, _ = sh(["git", "apply", "--whitespace=nowarn", "/tmp/tp.diff"], d)
        try: f2p = json.loads(r["FAIL_TO_PASS"])
        except Exception: f2p = []
        rc_t, log = sh(["python", "-m", "coverage", "run", "-m", "pytest", "-q",
                        "-p", "no:cacheprovider"] + f2p[:2], d, t=600)
        tail = log[-1200:]
        summ = re.findall(r"(\d+) (failed|passed|error[s]?|skipped|deselected)", tail)
        cls = ("collection/import error" if re.search(r"ERROR|ImportError|ModuleNotFound|"
               r"INTERNALERROR|errors? during collection", tail) else
               "no tests collected" if "no tests ran" in tail or "collected 0" in tail else
               "assertion FAILED (good)" if re.search(r"\d+ failed", tail) else
               "tests PASSED (bug absent?)" if re.search(r"\d+ passed", tail) else "unknown")
        out.append({"id": r["instance_id"], "install_rc": rc_i, "patch_rc": rc_p,
                    "pytest_rc": rc_t, "n_f2p": len(f2p), "summary": summ,
                    "class": cls, "f2p0": (f2p[0] if f2p else ""),
                    "tail": tail[-420:]})
        print(f"  {r['instance_id']:<34} {cls}")
    return out


@app.local_entrypoint()
def main():
    r = diag.remote(); json.dump(r, open("e1b_diag.json", "w"), indent=2)
    from collections import Counter
    print(f"\n{'='*76}\nE1b -- CLASSIFICATION OF THE 'NO GENUINE FAILURE' CASES\n{'='*76}")
    for k, v in Counter(x["class"] for x in r).most_common():
        print(f"  {k:<32}{v:>4}/{len(r)}")
    print(f"\n  install non-zero: {sum(1 for x in r if x['install_rc'])}/{len(r)}"
          f"   test-patch apply non-zero: {sum(1 for x in r if x['patch_rc'])}/{len(r)}")
    print(f"\n{'='*76}\nSAMPLE TAILS\n{'='*76}")
    for x in r[:4]:
        print(f"\n--- {x['id']}  [{x['class']}]  f2p[0]={x['f2p0'][:70]}")
        print("   " + x["tail"].replace("\n", "\n   ")[:600])
    ce = sum(1 for x in r if "error" in x["class"])
    print(f"\n{'='*76}\nREAD\n{'='*76}")
    if ce >= len(r)*0.5:
        print("  ENVIRONMENT INFIDELITY dominates -> modern deps vs historical code.")
        print("  Fix is per-instance environments (SWE-bench Docker images), a real cost.")
    else:
        print("  Not dominated by import errors -> re-examine detection/selector logic.")
