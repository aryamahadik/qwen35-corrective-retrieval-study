"""
H4 --- Measure the four numbers that decide the project: p_slow, rho, gamma, v.

THE CONSTRAINT SYSTEM (from the goal)
-------------------------------------
    p     = Pr(slow full-RAG fallback)          target <= 0.05
    rho   = N_fast / N_RAG   (evidence tokens)  4x needs rho + p <= 0.25
    gamma = C_fast / C_RAG   (tool calls)       2x needs gamma + p <= 0.50
    Delta = fast-path quality loss              needs (1-p)*Delta <= 0.01

    p = e(1 - v)    where e = raw routing miss rate, v = cheap-verification repair rate

The project lives or dies on p. Every prior experiment measured hardware; none measured p.

GROUND TRUTH, FREE, FROM GIT
----------------------------
For a bug-fix commit, the files it touches ARE the support of "why does X fail?". Query = commit
subject line. Gold = files changed. This is a CONSERVATIVE over-estimate of true minimal support
(a fix may touch files that only needed a signature update), which biases e UP and the verdict
AGAINST the system. That is the direction we want.

WHAT IS COMPARED
----------------
  RAG baseline  : hybrid BM25 + dense + RRF over 512-token chunks, top-k=8  => N_RAG ~ 4096 tok
  Fast path     : same router, but top-1..3 FUNCTION-LEVEL spans            => N_fast
  Verification  : does the candidate span contain an identifier mentioned in the query?
                  Cheap, lexical, no model. Repairs a miss by escalating to top-10 spans.

PRE-REGISTERED THRESHOLDS
-------------------------
    p <= 0.05  and  rho + p <= 0.25   => 4x token reduction is REACHABLE on this workload
    p >  0.10  with rho > 0.25        => strong target structurally unavailable; STOP

NO MODEL RUNS ON THE PRINCIPAL'S MACHINE. All execution is remote on Modal.
Budget: A10G, under 15 min => ~$0.30.

Usage:
    modal run experiments/h4_pslow.py
"""

import json
import os
import re
import subprocess

import modal

GPU = "A10G"
EMB_MODEL = "BAAI/bge-small-en-v1.5"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")
    .pip_install(
        "torch==2.5.1",
        "sentence-transformers==3.3.1",
        "transformers==4.48.3",
        "rank-bm25==0.2.2",
        "numpy==1.26.4",
    )
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"})
)

app = modal.App("qcarve-h4-pslow")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)

REPOS = [
    "https://github.com/pallets/flask",
    "https://github.com/psf/requests",
    "https://github.com/encode/httpx",
    "https://github.com/pallets/click",
]

CODE_EXT = {".py"}
FIX = ("fix", "bug", "issue", "error", "crash", "regression", "broken", "fail")
EXCL = ("test", "tests", "vendor", "docs")
CHUNK_TOK = 512          # RAG chunk size
TOP_K_RAG = 8            # RAG retrieves 8 chunks => ~4096 tokens
APPROX_TOK_PER_CHAR = 0.27


def _sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True).stdout


def _is_code(p):
    lo = p.lower()
    if any(f"/{x}/" in f"/{lo}" for x in EXCL):
        return False
    return os.path.splitext(lo)[1] in CODE_EXT


def _split_spans(text):
    """Function/class-level spans. A cheap AST proxy: split on top-level def/class."""
    lines = text.split("\n")
    bounds = [i for i, l in enumerate(lines) if re.match(r"^\s{0,4}(def|class)\s", l)]
    if not bounds:
        return [text]
    bounds = [0] + bounds + [len(lines)]
    out = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        s = "\n".join(lines[a:b]).strip()
        if s:
            out.append(s)
    return out


def _split_chunks(text, tok=CHUNK_TOK):
    """Fixed-size chunks, the RAG baseline unit."""
    chars = int(tok / APPROX_TOK_PER_CHAR)
    return [text[i:i + chars] for i in range(0, len(text), chars)] or [text]


def _ntok(s):
    return max(1, int(len(s) * APPROX_TOK_PER_CHAR))


def _idents(s):
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", s))


@app.function(image=image, gpu=GPU, timeout=3000, volumes={"/hf": hf_cache})
def measure(max_commits=1500, max_queries=250):
    os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from rank_bm25 import BM25Okapi
    from sentence_transformers import SentenceTransformer

    enc = SentenceTransformer(EMB_MODEL, cache_folder="/hf", device="cuda")
    report = []

    for url in REPOS:
        name = url.rstrip("/").split("/")[-1]
        work = f"/tmp/{name}"
        _sh(["git", "clone", "--quiet", f"--depth={max_commits}", url, work])
        if not os.path.isdir(f"{work}/.git"):
            continue

        files = [p for p in _sh(["git", "ls-files"], cwd=work).splitlines() if _is_code(p)]
        contents = {}
        for p in files:
            try:
                if os.path.getsize(f"{work}/{p}") > 400_000:
                    continue
                contents[p] = open(f"{work}/{p}", encoding="utf-8", errors="ignore").read()
            except OSError:
                pass
        if len(contents) < 15:
            continue

        # ---- queries from fix commits -------------------------------------------
        log = _sh(["git", "log", f"--max-count={max_commits}", "--no-merges",
                   "--pretty=format:@@@%s", "--name-only"], cwd=work)
        queries, msg, touched = [], None, []

        def flush():
            nonlocal msg, touched
            if msg and any(k in msg.lower() for k in FIX):
                g = {f for f in touched if f in contents}
                if 1 <= len(g) <= 5:
                    queries.append((msg, sorted(g)))
            msg, touched = None, []

        for ln in log.splitlines():
            if ln.startswith("@@@"):
                flush(); msg = ln[3:]
            elif ln.strip():
                touched.append(ln.strip())
        flush()
        queries = queries[:max_queries]
        if len(queries) < 25:
            continue

        # ---- build both index granularities -------------------------------------
        chunks, chunk_owner, spans, span_owner = [], [], [], []
        for f, txt in contents.items():
            for c in _split_chunks(txt):
                chunks.append(c); chunk_owner.append(f)
            for s in _split_spans(txt):
                spans.append(s); span_owner.append(f)

        def build(units):
            bm = BM25Okapi([re.findall(r"\w+", u.lower()) for u in units])
            emb = enc.encode(units, batch_size=256, convert_to_numpy=True,
                             normalize_embeddings=True, show_progress_bar=False)
            return bm, emb

        bm_c, emb_c = build(chunks)
        bm_s, emb_s = build(spans)

        def rrf(units, owner, bm, emb, q, k, kk=60):
            qe = enc.encode([q], convert_to_numpy=True, normalize_embeddings=True)[0]
            dense = np.argsort(-(emb @ qe))
            lex = np.argsort(-bm.get_scores(re.findall(r"\w+", q.lower())))
            score = {}
            for rank, i in enumerate(dense[:200]):
                score[i] = score.get(i, 0) + 1.0 / (kk + rank + 1)
            for rank, i in enumerate(lex[:200]):
                score[i] = score.get(i, 0) + 1.0 / (kk + rank + 1)
            top = sorted(score, key=lambda i: -score[i])[:k]
            return top, [owner[i] for i in top]

        # ---- measure -------------------------------------------------------------
        rag_hits = fast_hits = repaired = 0
        rag_tok, fast_tok = [], []

        for q, gold in queries:
            gold_set = set(gold)
            qi = _idents(q)

            idx_c, own_c = rrf(chunks, chunk_owner, bm_c, emb_c, q, TOP_K_RAG)
            if gold_set & set(own_c):
                rag_hits += 1
            rag_tok.append(sum(_ntok(chunks[i]) for i in idx_c))

            idx_s, own_s = rrf(spans, span_owner, bm_s, emb_s, q, 3)
            hit = bool(gold_set & set(own_s))
            if hit:
                fast_hits += 1
            fast_tok.append(sum(_ntok(spans[i]) for i in idx_s))

            if not hit:  # cheap lexical verification -> escalate to top-10 spans
                idx10, own10 = rrf(spans, span_owner, bm_s, emb_s, q, 10)
                verified = [j for j, i in enumerate(idx10) if qi & _idents(spans[i])]
                if verified and gold_set & {own10[j] for j in verified}:
                    repaired += 1

        n = len(queries)
        e = 1 - fast_hits / n
        v = repaired / max(1, n - fast_hits)
        p = e * (1 - v)
        rho = float(np.mean(fast_tok)) / float(np.mean(rag_tok))

        report.append({
            "repo": name, "files": len(contents), "queries": n,
            "chunks": len(chunks), "spans": len(spans),
            "rag_recall@8": round(rag_hits / n, 4),
            "fast_recall@3": round(fast_hits / n, 4),
            "e_raw_miss": round(e, 4),
            "v_repair_rate": round(v, 4),
            "p_slow": round(p, 4),
            "N_RAG_tok": round(float(np.mean(rag_tok)), 1),
            "N_fast_tok": round(float(np.mean(fast_tok)), 1),
            "rho": round(rho, 4),
            "rho_plus_p": round(rho + p, 4),
            "token_reduction_x": round(1.0 / (rho + p), 2) if rho + p > 0 else None,
        })

    hf_cache.commit()
    return {"emb_model": EMB_MODEL, "top_k_rag": TOP_K_RAG, "report": report}


@app.local_entrypoint()
def main(out: str = "h4_results.json"):
    r = measure.remote()
    with open(out, "w") as fh:
        json.dump(r, fh, indent=2)

    rows = r["report"]
    if not rows:
        print("No repo produced a usable measurement.")
        return

    print(f"\nembedder: {r['emb_model']}   RAG top-k = {r['top_k_rag']}\n")
    print(f"{'repo':<10} {'Q':>4} {'RAG@8':>7} {'fast@3':>7} {'e':>7} {'v':>7} "
          f"{'p_slow':>7} {'N_RAG':>7} {'N_fast':>7} {'rho':>6} {'rho+p':>7} {'tok x':>6}")
    print("-" * 96)
    for w in rows:
        print(f"{w['repo']:<10} {w['queries']:>4} {w['rag_recall@8']:>7.3f} "
              f"{w['fast_recall@3']:>7.3f} {w['e_raw_miss']:>7.3f} {w['v_repair_rate']:>7.3f} "
              f"{w['p_slow']:>7.3f} {w['N_RAG_tok']:>7.0f} {w['N_fast_tok']:>7.0f} "
              f"{w['rho']:>6.3f} {w['rho_plus_p']:>7.3f} {w['token_reduction_x'] or 0:>6.2f}")

    import statistics as st
    mp = st.median(w["p_slow"] for w in rows)
    mr = st.median(w["rho"] for w in rows)
    mrp = st.median(w["rho_plus_p"] for w in rows)

    print(f"\n{'='*96}\nMEDIANS\n{'='*96}")
    print(f"  p_slow  = {mp:.4f}    target <= 0.05   {'PASS' if mp <= 0.05 else 'FAIL'}")
    print(f"  rho     = {mr:.4f}")
    print(f"  rho + p = {mrp:.4f}    4x needs <= 0.25 {'PASS' if mrp <= 0.25 else 'FAIL'}"
          f"   6x needs <= 0.1667 {'PASS' if mrp <= 0.1667 else 'FAIL'}")
    print(f"  implied token reduction = {1/mrp:.2f}x" if mrp > 0 else "")

    print(f"\n{'='*96}\nVERDICT\n{'='*96}")
    if mp <= 0.05 and mrp <= 0.25:
        print(f"  TARGET REACHABLE. p_slow={mp:.3f} <= 0.05 and rho+p={mrp:.3f} <= 0.25.")
        print(f"  {1/mrp:.1f}x token reduction is supported on this workload. Proceed to")
        print("  latency and quality measurement.")
    elif mp > 0.10 and mrp > 0.25:
        print(f"  STOP. p_slow={mp:.3f} > 0.10 AND rho+p={mrp:.3f} > 0.25.")
        print("  The strong target is structurally unavailable on this workload.")
        print("  This is the pre-registered stopping rule firing.")
    else:
        print(f"  PARTIAL. p_slow={mp:.3f}, rho+p={mrp:.3f}.")
        print("  One constraint binds. The next experiment must push exactly that one down:")
        if mp > 0.05:
            print(f"    -> p_slow is binding ({mp:.3f}). Improve routing or verification repair v.")
        if mrp > 0.25:
            print(f"    -> rho+p is binding ({mrp:.3f}). Shrink fast-path evidence.")

    print(f"\n  Full results -> {out}\n")
