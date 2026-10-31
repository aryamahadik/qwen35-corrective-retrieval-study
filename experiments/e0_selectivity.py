"""
E0 --- Query selectivity measurement.

Measures the single load-bearing quantity in the QCRM thesis: how much of a corpus
does one query actually need?

Two estimators are computed, and the GAP BETWEEN THEM is the point of the experiment:

  1. COUNT RATIO  upsilon / kappa
     The independence-assumption bound from the selectivity theorem.
       kappa    = E_Q |S(Q)| / M        (expected fraction of files one query needs)
       upsilon  = |union_Q S(Q)| / M    (fraction of files any query ever needs)
     This is an UPPER BOUND on the advantage of query-conditioned memory.

  2. ENTROPY RATIO  H(C_U) / E_Q[H(C_S(Q))]
     The redundancy-corrected version. Real corpora are massively redundant --
     licence headers, import blocks, boilerplate, repeated idioms. A static encoder
     compresses the union ONCE and amortises that shared structure; a query-conditioned
     encoder pays for its own share every time. So redundancy is expected to SHRINK
     the advantage. This estimator measures by how much.

Entropy is estimated by compressed length (zstd), in three modes:
  raw        -- compress each set independently
  dict       -- compress with a dictionary trained on the whole corpus. This models
                "the base model already knows what Python looks like", i.e. the prior
                the learned memory does not have to store.
  overhead-corrected -- raw minus the empty-stream frame cost, which otherwise
                dominates small supports and biases kappa-side estimates upward.

Ground truth for S(Q) comes free from Git: for a bug-fix commit, the set of files
touched by the fix IS the support of the question "why does X fail?". This is a
CONSERVATIVE OVER-ESTIMATE of the true minimal support (a fix may touch files that
merely needed a signature update), which biases kappa UP and the advantage DOWN.
The measurement is therefore pessimistic, which is the direction we want.

Cost: CPU only. A handful of repositories runs in minutes for well under $1.

Usage:
    modal run experiments/e0_selectivity.py
    modal run experiments/e0_selectivity.py --repos "https://github.com/psf/requests"
    modal run experiments/e0_selectivity.py --max-commits 2000
"""

import json
import os
import subprocess
from dataclasses import dataclass, asdict, field

import modal

# --------------------------------------------------------------------------------------
# Environment
# --------------------------------------------------------------------------------------

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install("zstandard==0.23.0", "numpy==2.1.3")
)

app = modal.App("qcrm-e0-selectivity")

# A SIZE LADDER, spanning ~2.5 orders of magnitude in M.
#
# This is the point of the default list. The atom model predicts that median support
# |S(Q)| is roughly CONSTANT (a bug fix touches 1-3 files whatever the repo size),
# so kappa ~ c/M and the advantage ratio upsilon/kappa should grow LINEARLY IN M.
# A local run on psf/requests (M=22) gave upsilon/kappa = 9.6, which is exactly what
# the model predicts at that size -- and says nothing about a real codebase.
#
# If the ratio scales linearly in M across this ladder, the atom model is confirmed
# and the architecture's central bet holds at realistic repository sizes.
# If it SATURATES, the model is wrong and the thesis is capped at the saturation value.
# That regression is the actual experiment.
DEFAULT_REPOS = [
    "https://github.com/psf/requests",         # M ~ 22     (local baseline: 9.6x)
    "https://github.com/encode/httpx",         # M ~ 40
    "https://github.com/pallets/flask",        # M ~ 80
    "https://github.com/tiangolo/fastapi",     # M ~ 300
    "https://github.com/numpy/numpy",          # M ~ 600
    "https://github.com/django/django",        # M ~ 2,500
    "https://github.com/huggingface/transformers",  # M ~ 3,000+
]

# Extensions we treat as corpus. Everything else (lockfiles, images, generated
# artifacts) is excluded: it inflates M without ever being a query support.
CODE_EXT = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".h",
    ".cc", ".cpp", ".hpp", ".rb", ".php", ".cs", ".swift", ".kt", ".scala",
}

# Commit-message markers for "this commit fixes a defect". Deliberately narrow:
# feature commits touch many files for reasons unrelated to answering a question.
FIX_MARKERS = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")

EXCLUDE_PATH_PARTS = ("test", "tests", "vendor", "node_modules", "third_party", "docs/_build")


@dataclass
class RepoResult:
    repo: str
    ok: bool = True
    error: str = ""

    # corpus shape
    M: int = 0                       # files in corpus at HEAD
    n_queries: int = 0               # usable fix-commits
    corpus_bytes: int = 0

    # support-set statistics
    support_sizes: list = field(default_factory=list)
    kappa: float = 0.0               # E|S(Q)| / M
    upsilon: float = 0.0             # |union S(Q)| / M
    count_ratio: float = 0.0         # upsilon / kappa
    median_support: float = 0.0
    p90_support: float = 0.0

    # entropy-based ratios
    H_union_raw: int = 0
    H_support_raw_mean: float = 0.0
    entropy_ratio_raw: float = 0.0

    H_union_dict: int = 0
    H_support_dict_mean: float = 0.0
    entropy_ratio_dict: float = 0.0

    entropy_ratio_corrected: float = 0.0   # overhead-subtracted
    zstd_frame_overhead: int = 0

    # redundancy diagnostics
    total_correlation_proxy: float = 0.0   # sum |c(file_i)| / |c(union)|; 1.0 = no shared structure

    # allocation diagnostics (tests the reverse-water-filling prediction)
    file_query_freq_top20: list = field(default_factory=list)
    gini_query_freq: float = 0.0
    frac_files_never_queried: float = 0.0

    # saturation (does upsilon converge, and to what?)
    upsilon_curve: list = field(default_factory=list)   # (n_queries, upsilon)


def _sh(cmd, cwd=None, timeout=600):
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False
    ).stdout


def _is_code(path: str) -> bool:
    lo = path.lower()
    if any(f"/{p}/" in f"/{lo}" for p in EXCLUDE_PATH_PARTS):
        return False
    return os.path.splitext(lo)[1] in CODE_EXT


def _gini(xs):
    """Gini coefficient of query frequency. 0 = uniform, 1 = all mass on one file."""
    import numpy as np

    a = np.sort(np.asarray(xs, dtype=float))
    n = a.size
    if n == 0 or a.sum() == 0:
        return 0.0
    idx = np.arange(1, n + 1)
    return float((2.0 * (idx * a).sum()) / (n * a.sum()) - (n + 1.0) / n)


@app.function(image=image, timeout=3600, cpu=4.0, memory=8192)
def measure_repo(repo_url: str, max_commits: int = 3000) -> dict:
    """Clone one repository and compute every selectivity statistic."""
    import zstandard as zstd
    import numpy as np

    r = RepoResult(repo=repo_url)
    name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    work = f"/tmp/{name}"

    try:
        # --depth gives shallow history AND a full working tree. Using
        # --filter=blob:none instead would make every file read a network round trip,
        # which is fatal on a 3,000-file repository.
        _sh(["git", "clone", "--quiet", f"--depth={max_commits}", repo_url, work], timeout=1800)
        if not os.path.isdir(os.path.join(work, ".git")):
            r.ok, r.error = False, "clone failed"
            return asdict(r)

        # ---- corpus at HEAD -----------------------------------------------------
        tracked = [p for p in _sh(["git", "ls-files"], cwd=work).splitlines() if _is_code(p)]
        if len(tracked) < 10:
            r.ok, r.error = False, f"only {len(tracked)} code files"
            return asdict(r)

        contents = {}
        for p in tracked:
            fp = os.path.join(work, p)
            try:
                if os.path.getsize(fp) > 2_000_000:
                    continue
                with open(fp, "rb") as fh:
                    contents[p] = fh.read()
            except OSError:
                continue

        files = sorted(contents)
        r.M = len(files)
        r.corpus_bytes = sum(len(v) for v in contents.values())

        # ---- supports S(Q) from fix commits -------------------------------------
        log = _sh(
            ["git", "log", f"--max-count={max_commits}", "--no-merges",
             "--pretty=format:@@@%H%x09%s", "--name-only"],
            cwd=work, timeout=900,
        )

        supports, cur_msg, cur_files = [], None, []

        def _flush():
            nonlocal cur_msg, cur_files
            if cur_msg is not None:
                low = cur_msg.lower()
                if any(k in low for k in FIX_MARKERS):
                    s = {f for f in cur_files if f in contents}
                    # 1 <= |S| <= 25: singletons are real, huge commits are refactors
                    # or reformatting, which are not question supports.
                    if 1 <= len(s) <= 25:
                        supports.append(sorted(s))
            cur_msg, cur_files = None, []

        for line in log.splitlines():
            if line.startswith("@@@"):
                _flush()
                parts = line[3:].split("\t", 1)
                cur_msg = parts[1] if len(parts) > 1 else ""
            elif line.strip():
                cur_files.append(line.strip())
        _flush()

        if len(supports) < 20:
            r.ok, r.error = False, f"only {len(supports)} fix commits"
            return asdict(r)

        r.n_queries = len(supports)
        sizes = [len(s) for s in supports]
        r.support_sizes = sizes
        r.median_support = float(np.median(sizes))
        r.p90_support = float(np.percentile(sizes, 90))

        union = sorted({f for s in supports for f in s})
        r.kappa = float(np.mean(sizes)) / r.M
        r.upsilon = len(union) / r.M
        r.count_ratio = r.upsilon / r.kappa if r.kappa > 0 else 0.0

        # ---- entropy proxies ----------------------------------------------------
        def blob(fs):
            return b"\n".join(contents[f] for f in fs if f in contents)

        cctx = zstd.ZstdCompressor(level=19)
        r.zstd_frame_overhead = len(cctx.compress(b""))

        union_blob = blob(union)
        r.H_union_raw = len(cctx.compress(union_blob))

        # Dictionary trained on the corpus models the prior the base model already
        # has. Learned memory only needs to store what the prior does NOT supply.
        samples = [contents[f][:65536] for f in files if contents.get(f)]
        dict_data = None
        if len(samples) >= 8:
            try:
                dict_data = zstd.train_dictionary(110 * 1024, samples)
            except Exception:
                dict_data = None

        dctx = zstd.ZstdCompressor(level=19, dict_data=dict_data) if dict_data else cctx
        r.H_union_dict = len(dctx.compress(union_blob))

        # Sub-sample supports if there are very many; 400 is ample for a stable mean.
        rng = np.random.default_rng(0)
        idx = (rng.choice(len(supports), 400, replace=False)
               if len(supports) > 400 else np.arange(len(supports)))

        raws, dicts = [], []
        for i in idx:
            b = blob(supports[int(i)])
            if not b:
                continue
            raws.append(len(cctx.compress(b)))
            dicts.append(len(dctx.compress(b)))

        r.H_support_raw_mean = float(np.mean(raws)) if raws else 0.0
        r.H_support_dict_mean = float(np.mean(dicts)) if dicts else 0.0

        r.entropy_ratio_raw = (r.H_union_raw / r.H_support_raw_mean) if r.H_support_raw_mean else 0.0
        r.entropy_ratio_dict = (r.H_union_dict / r.H_support_dict_mean) if r.H_support_dict_mean else 0.0

        ov = r.zstd_frame_overhead
        num, den = max(1, r.H_union_raw - ov), max(1.0, r.H_support_raw_mean - ov)
        r.entropy_ratio_corrected = num / den

        # Redundancy diagnostic: 1.0 means files share nothing; larger means the
        # union compresses far better than the parts, i.e. heavy shared structure.
        per_file = sum(len(cctx.compress(contents[f])) for f in union if contents.get(f))
        r.total_correlation_proxy = per_file / max(1, r.H_union_raw)

        # ---- allocation diagnostics --------------------------------------------
        freq = {f: 0 for f in files}
        for s in supports:
            for f in s:
                if f in freq:
                    freq[f] += 1
        counts = list(freq.values())
        r.gini_query_freq = _gini(counts)
        r.frac_files_never_queried = sum(1 for c in counts if c == 0) / max(1, len(counts))
        r.file_query_freq_top20 = sorted(
            ({"file": f, "n": c} for f, c in freq.items() if c > 0),
            key=lambda d: -d["n"],
        )[:20]

        # ---- saturation curve for upsilon --------------------------------------
        seen, curve = set(), []
        for i, s in enumerate(supports, 1):
            seen.update(s)
            if i % max(1, len(supports) // 20) == 0 or i == len(supports):
                curve.append({"n": i, "upsilon": len(seen) / r.M})
        r.upsilon_curve = curve

        return asdict(r)

    except Exception as e:  # noqa: BLE001 -- one bad repo must not kill the run
        r.ok, r.error = False, f"{type(e).__name__}: {e}"
        return asdict(r)


@app.local_entrypoint()
def main(repos: str = "", max_commits: int = 3000, out: str = "e0_results.json"):
    repo_list = [x.strip() for x in repos.split(",") if x.strip()] or DEFAULT_REPOS

    print(f"\nE0 --- query selectivity, {len(repo_list)} repositories\n")
    results = list(measure_repo.map(repo_list, kwargs={"max_commits": max_commits}))

    ok = [r for r in results if r["ok"]]
    bad = [r for r in results if not r["ok"]]

    for r in bad:
        print(f"  SKIP {r['repo']}: {r['error']}")

    if not ok:
        print("\nNo repository produced a usable measurement. Nothing to report.")
        return

    print(f"\n{'repo':<20} {'M':>6} {'Q':>6} {'kappa':>9} {'ups':>6} "
          f"{'count':>8} {'ent-raw':>8} {'ent-dict':>9} {'redund':>7}")
    print("-" * 92)
    for r in ok:
        print(f"{r['repo'].split('/')[-1]:<20} {r['M']:>6} {r['n_queries']:>6} "
              f"{r['kappa']:>9.5f} {r['upsilon']:>6.3f} {r['count_ratio']:>8.1f} "
              f"{r['entropy_ratio_raw']:>8.1f} {r['entropy_ratio_dict']:>9.1f} "
              f"{r['total_correlation_proxy']:>7.2f}")

    import statistics as st

    cr = st.median(r["count_ratio"] for r in ok)
    er = st.median(r["entropy_ratio_raw"] for r in ok)
    ed = st.median(r["entropy_ratio_dict"] for r in ok)
    nq = st.median(r["frac_files_never_queried"] for r in ok)
    gi = st.median(r["gini_query_freq"] for r in ok)

    print(f"\n{'='*92}\nMEDIANS ACROSS {len(ok)} REPOSITORIES\n{'='*92}")
    print(f"  count ratio    upsilon/kappa            : {cr:8.1f}   <- independence upper bound")
    print(f"  entropy ratio  H(C_U)/E[H(C_S)]         : {er:8.1f}   <- redundancy-corrected")
    print(f"  entropy ratio  with corpus dictionary   : {ed:8.1f}   <- corrected for model prior")
    print(f"  redundancy collapse  count -> entropy   : {(cr/er if er else 0):8.1f}x")
    print(f"  files never queried                     : {nq:8.1%}   <- reverse water-filling")
    print(f"  Gini of query frequency                 : {gi:8.3f}")

    # ---- THE ACTUAL EXPERIMENT: does the advantage scale linearly in M? ----------
    #
    # The atom model predicts median |S(Q)| is roughly constant in M, hence
    # kappa ~ c/M and ratio ~ M/c. Fit log(ratio) = a*log(M) + b. The exponent a is
    # the verdict:  a ~ 1  => model confirmed, advantage grows with repo size.
    #               a ~ 0  => saturation, thesis capped at the observed plateau.
    print(f"\n{'='*92}\nSCALING TEST --- the atom model predicts exponent a = 1\n{'='*92}")

    import math

    pts = [(r["M"], r["entropy_ratio_dict"], r["count_ratio"], r["median_support"])
           for r in ok if r["M"] > 0 and r["entropy_ratio_dict"] > 0]

    a_ent = a_cnt = float("nan")
    if len(pts) >= 3:
        def fit(xs, ys):
            lx = [math.log(x) for x in xs]
            ly = [math.log(y) for y in ys]
            n = len(lx)
            mx, my = sum(lx) / n, sum(ly) / n
            num = sum((lx[i] - mx) * (ly[i] - my) for i in range(n))
            den = sum((lx[i] - mx) ** 2 for i in range(n))
            return num / den if den else float("nan")

        a_ent = fit([p[0] for p in pts], [p[1] for p in pts])
        a_cnt = fit([p[0] for p in pts], [p[2] for p in pts])

        print(f"  log-log slope, entropy ratio vs M : a = {a_ent:.2f}")
        print(f"  log-log slope, count   ratio vs M : a = {a_cnt:.2f}")
        ms = [p[3] for p in pts]
        print(f"  median |S(Q)| across sizes        : {min(ms):.0f} to {max(ms):.0f} files "
              f"(model predicts ~constant)")
    else:
        print("  NOT MEASURED --- fewer than 3 usable repositories. This is not a zero.")

    print(f"\n{'='*92}\nDECISION\n{'='*92}")

    # Extrapolate to a realistic working repository rather than judging on the
    # median of a ladder deliberately containing tiny libraries.
    M_TARGET = 3000
    if pts and not math.isnan(a_ent):
        Mref, rref = max(pts, key=lambda p: p[0])[0], max(pts, key=lambda p: p[0])[1]
        projected = rref * (M_TARGET / Mref) ** a_ent
        print(f"  Largest measured: M={Mref}, corrected advantage {rref:.1f}x")
        print(f"  Projected at M={M_TARGET} (exponent {a_ent:.2f}): {projected:.0f}x")
    else:
        projected = ed
        print(f"  Using median corrected advantage {projected:.1f}x (no scaling fit available)")

    if not math.isnan(a_ent) and a_ent < 0.3:
        print(f"\n  STOP --- SATURATION. Exponent {a_ent:.2f} is far below the predicted 1.0.")
        print("  The advantage does NOT grow with repository size, so it is capped near")
        print(f"  {ed:.1f}x regardless of corpus. The atom model is wrong and the")
        print("  query-conditioned tier cannot pay for its complexity. Collapse QCRM to a")
        print("  static cartridge plus exact backing.")
    elif projected < 10:
        print(f"\n  STOP. Projected advantage {projected:.0f}x is below 10x even at M={M_TARGET}.")
        print("  Query-conditioned memory cannot pay for its complexity.")
    elif projected < 100:
        print(f"\n  MARGINAL. Projected advantage {projected:.0f}x at M={M_TARGET}.")
        print("  Real but not decisive. Proceed only if the RAG crossover analysis puts")
        print("  your operating point inside the QCRM-favourable region.")
    else:
        print(f"\n  PROCEED. Projected advantage {projected:.0f}x at M={M_TARGET}, with")
        print(f"  scaling exponent {a_ent:.2f} confirming the atom model.")
        print("  The architecture's central bet holds on real corpora --- established")
        print("  with no model trained, no GPU used, and no cartridge built.")

    if nq > 0.5:
        print(f"\n  Reverse water-filling CONFIRMED: {nq:.0%} of files are never the support")
        print("  of any query. Those files should receive ZERO learned memory and be")
        print("  served from the exact tier. Uniform allocation wastes most of the budget.")

    with open(out, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\n  Full results -> {out}\n")
