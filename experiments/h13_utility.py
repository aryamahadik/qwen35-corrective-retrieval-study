"""
H13 --- Is downstream UTILITY learnable where relevance is not?

H12 established the fork: a <=850-token subset preserving RAG8 quality EXISTS
(S_oracle=0.5792 vs S_RAG8=0.3875, chance floor 0.2125, p=1.5e-25). The gain is
almost entirely POINTWISE -- complementarity contributes 0.4pp of 19.2pp -- so
set-level U(Q,S) is the wrong tool. The right problem is choosing ONE chunk.

AND relevance does not solve it: utility by RRF rank is 0.276 0.283 0.229 0.250
0.204 0.213 0.208 0.204 -- nearly FLAT, rank-1 above rank-0, and the winning chunk
is top-ranked in only 47.8% of solvable queries. That is why the H11 cross-encoder
(a RELEVANCE reranker) gained only +2.9pp.

HYPOTHESIS
  H13: P(model answers correctly | query, chunk) is predictable from cheap features
  ABOVE the relevance baseline, and selecting argmax beats rank-1 selection.

WHY THIS IS CHEAP
  H12 already generated the label for every (query, chunk) singleton. Selection is
  scored against those existing labels -- NO LLM generation at all. Feature
  extraction + training only.

CONTROLS AND HONESTY
  - LEAVE-ONE-REPO-OUT cross-validation. The model must generalise to an UNSEEN
    repository, not merely to held-out queries from repos it trained on.
  - Relevance-only baseline (cross-encoder score alone) is fit the same way, so any
    gain is attributable to UTILITY features, not to fitting per se.
  - A label-shuffled control bounds how much apparent gain is pure overfitting.

PRE-REGISTERED
  WIN   : LORO selection score > rank-0 baseline (0.2762) by >5pp AND > shuffled control.
  WEAK  : beats rank-0 by 0-5pp -- utility is learnable but thin.
  FAIL  : <= rank-0, or indistinguishable from the shuffled control -> utility is not
          learnable from cheap features; the signal needs a new source (execution traces).
  I expect WEAK-to-WIN. Relevance carries only +4.9pp, so there is room, but 240
  queries is a small training set and the labels are noisy. Stating this first.

COST: A10G, feature extraction only, no generation => ~$0.30.
"""
import json, re, modal

EMB_MODEL = "BAAI/bge-small-en-v1.5"
RERANKER = "BAAI/bge-reranker-base"
SEP = "\n\n---\n\n"

image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.48.3",
                 "rank-bm25==0.2.2", "numpy==1.26.4", "scikit-learn==1.5.2")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false"}))
app = modal.App("qcarve-h13-utility")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


@app.function(image=image, gpu="A10G", timeout=3600,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(labels):
    """labels[i][k] = 1 if the model answered correctly from chunk k of query i alone."""
    import os; os.environ["HF_HOME"] = "/hf"
    import numpy as np
    from sentence_transformers import SentenceTransformer, CrossEncoder
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import GradientBoostingClassifier

    items = json.load(open("/data/h7_items.json"))
    n = len(items)
    emb = SentenceTransformer(EMB_MODEL, device="cuda")
    rr = CrossEncoder(RERANKER, device="cuda", max_length=512)
    idents = lambda s: set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", s))

    rows, y, qid, repo = [], [], [], []
    pairs, meta = [], []
    for i, it in enumerate(items):
        ch = it["RAG8"].split(SEP)
        for k, c in enumerate(ch):
            pairs.append([it["query"], c[:1800]]); meta.append((i, k, c))
    ce = rr.predict(pairs, batch_size=64, show_progress_bar=False)

    Q = emb.encode([it["query"] for it in items], normalize_embeddings=True,
                   convert_to_numpy=True, show_progress_bar=False)
    C = emb.encode([m[2][:2000] for m in meta], normalize_embeddings=True,
                   convert_to_numpy=True, show_progress_bar=False)

    for idx, (i, k, c) in enumerate(meta):
        it = items[i]; qi = idents(it["query"]); ci = idents(c)
        defs = set(re.findall(r"(?:def|class)\s+([A-Za-z_]\w+)", c))
        rows.append([
            float(ce[idx]),                       # cross-encoder RELEVANCE
            float(Q[i] @ C[idx]),                 # dense similarity
            float(k),                             # RRF rank
            len(c) / 2000.0,                      # chunk length
            len(qi & ci) / max(len(qi), 1),       # identifier coverage
            len(qi & defs) / max(len(qi), 1),     # query names a symbol DEFINED here
            float(len(defs)),                     # definition density
            float(c.count("\n")) / 100.0,         # line count
            float(c.lstrip().startswith(("import", "from"))),  # import/boilerplate block
            float(len(ci)) / 100.0,               # identifier richness
        ])
        y.append(labels[i][k]); qid.append(i); repo.append(it["repo"])

    X = np.array(rows); y = np.array(y); qid = np.array(qid); repo = np.array(repo)
    print(f"[data] {X.shape[0]} (query,chunk) pairs, positive rate {y.mean():.4f}")

    def select_score(scores):
        """mean label of the argmax-scored chunk per query"""
        tot = 0
        for i in range(n):
            m = qid == i
            if not m.any(): continue
            tot += int(y[m][int(np.argmax(scores[m]))])
        return float(tot) / n

    def loro(cols, model_fn, yy):
        s = np.zeros(len(yy))
        for rp in sorted(set(repo)):
            tr, te = repo != rp, repo == rp
            mdl = model_fn().fit(X[tr][:, cols], yy[tr])
            s[te] = mdl.predict_proba(X[te][:, cols])[:, 1]
        return s

    ALL = list(range(X.shape[1])); REL = [0, 1, 2]
    LR = lambda: LogisticRegression(max_iter=2000, C=1.0)
    GB = lambda: GradientBoostingClassifier(n_estimators=120, max_depth=3, random_state=0)

    base_rank0 = select_score(-X[:, 2])            # pick RRF rank 0
    base_rel   = select_score(X[:, 0])             # pick highest cross-encoder relevance
    oracle     = sum(max(labels[i]) for i in range(n)) / n
    res = {"rank0": float(base_rank0), "relevance_raw": float(base_rel),
           "oracle_singleton": float(oracle)}
    for nm, cols, fn in (("relevance_fit_LR", REL, LR), ("utility_LR", ALL, LR),
                         ("utility_GB", ALL, GB)):
        res[nm] = float(select_score(loro(cols, fn, y)))
    rng = np.random.default_rng(0)
    ysh = y.copy()
    for i in range(n):
        m = qid == i; v = ysh[m].copy(); rng.shuffle(v); ysh[m] = v
    res["shuffled_control_GB"] = float(select_score(loro(ALL, GB, ysh)))

    mdl = GB().fit(X[:, ALL], y)
    names = ["cross_enc_rel", "dense_sim", "rrf_rank", "chunk_len", "ident_cov",
             "defines_query_sym", "n_defs", "n_lines", "is_import_block", "ident_rich"]
    res["feature_importance"] = sorted(zip(names, [float(v) for v in mdl.feature_importances_]),
                                       key=lambda t: -t[1])
    hf_cache.commit()
    return res


@app.local_entrypoint()
def main(out: str = "h13_results.json"):
    h12 = json.load(open("h12_results.json")); n = h12["n_items"]
    labels = [[0]*8 for _ in range(n)]
    for x in h12["records"]:
        if x["arm"] == "ORACLE" and len(x["subset"]) == 1:
            labels[x["i"]][x["subset"][0]] = x["hit"]
    r = run.remote(labels)
    json.dump(r, open(out, "w"), indent=2)

    print(f"\n{'='*76}\nH13 -- SELECTION SCORE (leave-one-repo-out), pick 1 chunk ~496 tok\n{'='*76}")
    order = ["rank0", "relevance_raw", "relevance_fit_LR", "utility_LR", "utility_GB",
             "shuffled_control_GB", "oracle_singleton"]
    lab = {"rank0": "RRF rank-0 (baseline)", "relevance_raw": "cross-encoder relevance",
           "relevance_fit_LR": "relevance features, fit", "utility_LR": "UTILITY model (LR)",
           "utility_GB": "UTILITY model (GB)", "shuffled_control_GB": "shuffled-label control",
           "oracle_singleton": "ORACLE (upper bound)"}
    b = r["rank0"]
    for k in order:
        d = (r[k] - b) * 100
        print(f"  {lab[k]:<28} {r[k]:.4f}   {d:+6.1f}pp vs rank-0")
    print(f"\n  RAG8 reference = 0.3875 @ 3399 tok   |   these use ~496 tok (6.85x)")
    best = max(r["utility_LR"], r["utility_GB"])
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if best <= r["shuffled_control_GB"] + 0.01:
        print("  FAIL -- utility model is indistinguishable from the shuffled-label control.")
        print("  Utility is NOT learnable from these cheap features. Need a new signal source.")
    elif (best - b) * 100 > 5:
        print(f"  WIN -- utility selection beats rank-0 by {(best-b)*100:+.1f}pp at 6.85x compression.")
        print("  Relevance != utility is exploitable. Next: richer features / learned encoder.")
    elif best > b:
        print(f"  WEAK -- {(best-b)*100:+.1f}pp over rank-0. Learnable but thin at this sample size.")
    else:
        print("  FAIL -- no gain over rank-0.")
    print("\n  feature importance:")
    for nm, v in r["feature_importance"]:
        print(f"    {nm:<20} {v:.4f}")
