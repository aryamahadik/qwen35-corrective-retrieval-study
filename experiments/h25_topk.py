"""
H25 --- Does GROUNDING-RANKED top-k actually beat RAG8 when generated?

THE CORRECTION THAT LED HERE
  H23 concluded grounding failed. That test was wrong: it used grounding as a HARD
  FILTER over all 480 queries and measured P(correct | grounded) = 0.1517 vs 0.2098.
  Grounding fires on winners AND on many losers, so precision is low -- but winners are
  almost always grounded (UNgrounded ranks BELOW random). As a RANKING PRIOR on the
  subset where selection matters (evidence-needed AND solvable, n=153):

    scorer        rec@1  rec@2  rec@3  rec@4
    grounded      0.549  0.732  0.843  0.915
    rank order    0.405  0.673  0.784  0.830
    random        0.218  0.389  0.522  0.626

  Grounding beats random 2.5x at rec@1 and beats rank order at every k.

WHAT THIS TESTS
  Recall of the winner is not the same as ANSWERING correctly: a top-k bundle adds
  distractors, and H12 showed distractors actively hurt. So generate with the
  grounding-ranked top-1/2/3/4 and measure, against RAG8 and rank-ordered top-k at
  MATCHED token budgets.

ARMS (7B answerer; 14B/32B via the same bundles for the cascade claim)
  GND1..GND4   grounding-ranked top-k chunks
  RNK1..RNK4   rank-ordered top-k (matched tokens, isolates the SIGNAL not the budget)
  RAG8         reference

HONEST COST NOTE
  Computing the grounding signal costs 8 singleton generations = 3,968 tok of 7B,
  MORE than RAG8's 3,399. This is only economical as a CROSS-MODEL cascade: 7B labels
  + 32B answer = 43,648 param-tokens vs 32B RAG8 = 108,768, i.e. 60% cheaper. Same-model
  it is NOT a win, and that is reported either way.

PRE-REGISTERED (on the 392 evidence-needed queries, contamination-corrected)
  WIN  : some GNDk beats RAG8 (0.2628) at fewer tokens AND beats matched RNKk.
  WEAK : beats RNKk but not RAG8 -> grounding is real signal, insufficient alone.
  FAIL : does not beat matched RNKk -> the recall@k advantage does not survive
         generation, and the ranking signal is illusory.
  I expect WEAK-to-WIN. rec@3 = 0.843 is a large margin over rank order's 0.784, but
  distractor damage is the known risk. Stating this before the run.

COST: A10G 7B ~3800 generations => ~$0.30.
"""
import json, os, re, modal
from collections import Counter
SEP = "\n\n---\n\n"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h25-topk")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A10G", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(answers, model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    norm = lambda t: (re.search(r"[A-Za-z_][\w.]*", (t or "").replace("`", "")).group(0)
                      .split(".")[-1] if re.search(r"[A-Za-z_][\w.]*",
                      (t or "").replace("`", "")) else "")
    order_g = []
    for i, it in enumerate(items):
        ch = it["chunks"]; v = [norm(a) for a in answers[i]]
        g = [1 if v[k] and re.search(rf"(?:def|class)\s+{re.escape(v[k])}\b", ch[k]) else 0
             for k in range(8)]
        order_g.append(sorted(range(8), key=lambda k: -(g[k]*10 - k*0.1)))

    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key = [], []
    for i, it in enumerate(items):
        ch = it["chunks"]
        for k in (1, 2, 3, 4):
            pr.append(TPL.format(q=it["query"], e=SEP.join(ch[j] for j in order_g[i][:k])))
            key.append((i, f"GND{k}"))
            pr.append(TPL.format(q=it["query"], e=SEP.join(ch[:k])))
            key.append((i, f"RNK{k}"))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in pr]
    print(f"[plan] {len(chat)} generations")
    res = llm.generate(chat, sp)
    out = {}
    ntok = {}
    for (i, arm), r, p in zip(key, res, pr):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in items[i]["gold"]))
        out.setdefault(arm, [0]*n)[i] = hit
        ntok.setdefault(arm, []).append(len(tok(p)["input_ids"]))
    hf_cache.commit()
    return {"model": model, "n": n, "arms": out,
            "tok": {k: sum(v)/len(v) for k, v in ntok.items()},
            "order_g": order_g}


@app.local_entrypoint()
def main(out: str = "h25_results.json"):
    H = json.load(open("h21_results.json")); H23 = json.load(open("h23_results.json"))
    N = json.load(open("h24_results.json"))
    r = run.remote(H23["answers"]); json.dump(r, open(out, "w"), indent=2)
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = r["n"]; S7 = H["r7"]["S"]; P7 = H["r7"]["R"]; null = N["NOCTX"]
    real = [i for i in range(n) if repos[i] not in SMALL]
    need = [i for i in real if null[i] == 0]
    A = r["arms"]; T = r["tok"]
    f = lambda v, ix: sum(v[i] for i in ix)/len(ix)
    rag8 = f(P7, need); rag8all = f(P7, real)
    print(f"\n{'='*86}\nH25 -- GROUNDING-RANKED top-k, 7B\n{'='*86}")
    print(f"  evidence-needed queries n={len(need)} (contamination-corrected); "
          f"all real n={len(real)}")
    print(f"\n  {'arm':<8}{'tokens':>8}{'x vs RAG8':>11}{'need-only':>12}{'vs RAG8':>10}"
          f"{'all real':>11}")
    print("-"*86)
    best = (0, None)
    for k in (1, 2, 3, 4):
        for pre in ("RNK", "GND"):
            a = f"{pre}{k}"
            v = f(A[a], need)
            if pre == "GND" and v > best[0]: best = (v, a)
            print(f"  {a:<8}{T[a]:>8.0f}{3399/T[a]:>10.2f}x{v:>12.4f}"
                  f"{(v-rag8)*100:>9.1f}p{f(A[a], real):>11.4f}")
    print(f"  {'RAG8':<8}{3399:>8}{1.00:>10.2f}x{rag8:>12.4f}{0.0:>9.1f}p{rag8all:>11.4f}")
    print(f"\n{'='*86}\nVERDICT\n{'='*86}")
    bv, ba = best
    k = int(ba[-1]); rnk = f(A[f"RNK{k}"], need)
    print(f"  best grounding arm: {ba} = {bv:.4f} @{T[ba]:.0f} tok "
          f"({3399/T[ba]:.2f}x fewer)")
    print(f"  matched rank-order control RNK{k} = {rnk:.4f}   -> grounding adds "
          f"{(bv-rnk)*100:+.1f}pp")
    print(f"  RAG8 = {rag8:.4f} @3399 tok")
    if bv > rag8 and bv > rnk:
        print(f"\n  WIN -- a GOLD-FREE selector beats RAG8 by {(bv-rag8)*100:+.1f}pp at "
              f"{3399/T[ba]:.2f}x fewer tokens,")
        print("  and beats its matched-budget rank-order control. First gold-free win.")
    elif bv > rnk:
        print(f"\n  WEAK -- beats matched control by {(bv-rnk)*100:+.1f}pp but not RAG8.")
    else:
        print(f"\n  FAIL -- does not beat matched rank-order control; the recall@k")
        print("  advantage does not survive generation.")
