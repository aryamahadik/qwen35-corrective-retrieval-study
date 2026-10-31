"""
H26 --- Can a LEARNED ranker close 45% of the selection gap where grounding closes 24%?

WHERE THIS STANDS
  H25 validated grounding as a gold-free ranking prior at k=1: 0.2143 vs 0.1582 for the
  matched rank-order control, McNemar 30/8, p=0.0005. It closes 24.2% of the
  rank-1 -> oracle gap (0.1582 -> 0.3903). Beating RAG8 (0.2628) needs 45.1%.

WHY THIS IS NOT A REPEAT OF H13
  H13's learned ranker tied its baseline and sat near a shuffled control. But it never
  had GROUNDING as a feature -- grounding requires generating an answer per chunk,
  which H13 did not do. It is now the only feature with a validated effect. Also
  unused: CHUNK LENGTH, which scored rec@1 = 0.431, ABOVE rank order's 0.405.

WHY IT IS ALMOST FREE
  At k=1 the outcome of picking chunk j IS the singleton label S7[i][j], already
  measured. So a new ranker is evaluated with NO generation.

FEATURES (all gold-free, all computable at serving time)
  grounded, rank, chunk length, answer vote count, answer rarity, answer length,
  whether the answer is empty, identifier overlap query<->chunk, definition count

CONTROLS
  - LEAVE-ONE-REPO-OUT: must generalise to an unseen repository.
  - grounding-only baseline (the thing to beat).
  - shuffled-label control, to bound overfitting on 392 queries.
  - evaluated ONLY on evidence-needed queries (contamination-corrected).

PRE-REGISTERED
  WIN  : learned ranker >= 0.2628 (RAG8) at ~500 tok, above the shuffled control.
  GAIN : beats grounding-only (0.2143) but not RAG8 -> report the new gap fraction.
  FAIL : <= grounding-only -> grounding is the whole signal; combination adds nothing.
  I expect GAIN, not WIN. Closing 45% from 24% is a large ask from 9 weak features on
  392 queries. Stating this before the run.

COST: Modal CPU only, ~$0.05.
"""
import json, os, re, modal
from collections import Counter
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "numpy==1.26.4", "scikit-learn==1.5.2")
app = modal.App("qcarve-h26-learned")
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


@app.function(image=image, timeout=1800, volumes={"/data": data_vol})
def learn(answers, S7, null, repos, small):
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import GradientBoostingClassifier
    items = json.load(open("/data/h21_items.json")); n = len(items)
    norm = lambda t: (re.search(r"[A-Za-z_][\w.]*", (t or "").replace("`", "")).group(0)
                      .split(".")[-1] if re.search(r"[A-Za-z_][\w.]*",
                      (t or "").replace("`", "")) else "")
    idents = lambda s: set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", s))
    X, Y, Q, RP = [], [], [], []
    for i, it in enumerate(items):
        ch = it["chunks"]; v = [norm(a) for a in answers[i]]
        cnt = Counter(x for x in v if x); qi = idents(it["query"])
        for k in range(8):
            c = ch[k]
            g = 1.0 if v[k] and re.search(rf"(?:def|class)\s+{re.escape(v[k])}\b", c) else 0.0
            X.append([g, float(k), len(c)/2000.0, float(cnt[v[k]]) if v[k] else 0.0,
                      -float(cnt[v[k]]) if v[k] else 0.0, float(len(v[k])),
                      1.0 if not v[k] else 0.0,
                      len(qi & idents(c))/max(len(qi), 1),
                      float(len(re.findall(r"(?:def|class)\s+\w+", c)))])
            Y.append(S7[i][k]); Q.append(i); RP.append(repos[i])
    X = np.array(X); Y = np.array(Y); Q = np.array(Q); RP = np.array(RP)
    need = [i for i in range(n) if null[i] == 0 and repos[i] not in small]
    need_set = set(need)

    def sel(score):
        tot = 0
        for i in need:
            m = Q == i
            tot += Y[m][int(np.argmax(score[m]))]
        return tot/len(need)

    def loro(yy, cols):
        s = np.zeros(len(yy))
        for rp in sorted(set(RP)):
            tr, te = RP != rp, RP == rp
            if tr.sum() == 0 or te.sum() == 0: continue
            m = GradientBoostingClassifier(n_estimators=150, max_depth=3, random_state=0)
            m.fit(X[tr][:, cols], yy[tr])
            s[te] = m.predict_proba(X[te][:, cols])[:, 1]
        return s
    ALL = list(range(X.shape[1]))
    out = {}
    out["rank_only"] = sel(-X[:, 1])
    out["grounding_only"] = sel(X[:, 0]*10 - X[:, 1]*0.1)
    out["length_only"] = sel(X[:, 2])
    out["learned_GB"] = sel(loro(Y, ALL))
    out["learned_noGND"] = sel(loro(Y, [c for c in ALL if c != 0]))
    rng = np.random.default_rng(0); ysh = Y.copy()
    for i in range(n):
        m = Q == i; v2 = ysh[m].copy(); rng.shuffle(v2); ysh[m] = v2
    out["shuffled_control"] = sel(loro(ysh, ALL))
    out["ORACLE"] = float(np.mean([max(S7[i]) for i in need]))
    mdl = GradientBoostingClassifier(n_estimators=150, max_depth=3, random_state=0).fit(X, Y)
    nm = ["grounded", "rank", "chunk_len", "votes", "rarity", "ans_len",
          "ans_empty", "ident_overlap", "n_defs"]
    out["importance"] = sorted(zip(nm, [float(v) for v in mdl.feature_importances_]),
                               key=lambda t: -t[1])
    out["n_need"] = len(need)
    return out


@app.local_entrypoint()
def main(out: str = "h26_results.json"):
    H = json.load(open("h21_results.json")); H23 = json.load(open("h23_results.json"))
    N = json.load(open("h24_results.json"))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    r = learn.remote(H23["answers"], H["r7"]["S"], N["NOCTX"], repos,
                     ["itsdangerous", "cachecontrol"])
    json.dump(r, open(out, "w"), indent=2)
    RAG8 = 0.2628; base = r["rank_only"]; orc = r["ORACLE"]
    print(f"\n{'='*74}\nH26 -- LEARNED RANKER at k=1, evidence-needed n={r['n_need']}\n{'='*74}")
    print(f"  {'selector':<22}{'score':>9}{'gap closed':>13}")
    print("-"*74)
    for k in ("rank_only", "length_only", "grounding_only", "learned_noGND",
              "learned_GB", "shuffled_control", "ORACLE"):
        v = r[k]
        print(f"  {k:<22}{v:>9.4f}{(v-base)/(orc-base):>12.1%}")
    print(f"  {'RAG8 @3399 tok':<22}{RAG8:>9.4f}{(RAG8-base)/(orc-base):>12.1%}")
    best = max(r["learned_GB"], r["grounding_only"])
    print(f"\n{'='*74}\nVERDICT\n{'='*74}")
    if r["learned_GB"] >= RAG8 and r["learned_GB"] > r["shuffled_control"] + 0.02:
        print(f"  WIN -- learned ranker {r['learned_GB']:.4f} >= RAG8 {RAG8:.4f} at 6.6x")
        print("  fewer tokens. A gold-free selector beats full RAG.")
    elif r["learned_GB"] > r["grounding_only"] + 0.01:
        print(f"  GAIN -- {r['learned_GB']:.4f} beats grounding-only "
              f"({r['grounding_only']:.4f}); still under RAG8.")
    else:
        print(f"  FAIL -- learned {r['learned_GB']:.4f} does not beat grounding-only "
              f"({r['grounding_only']:.4f}). Grounding is the whole signal.")
    print("\n  feature importance:")
    for nm, v in r["importance"]:
        print(f"    {nm:<16}{v:.4f}")
