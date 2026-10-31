"""
H16 --- Can the winning chunk be identified WITHOUT gold, via self-consistency?

WHERE THIS COMES FROM
  H15 proved the selection target is STABLE (kappa 0.67): the chunk that works for 7B
  works for 14B, and 14B on 7B's pick scores 0.4000 @496 tok vs 0.3083 @3399 tok for
  full RAG8 -- +9.2pp at 6.85x fewer tokens. In params x tokens that cascade is 27%
  cheaper than RAG8 (60% against a 32B answerer).

  But "7B's pick" meant the chunk where 7B answered CORRECTLY, which needs gold.
  It is an oracle-assisted upper bound, not a router. This experiment removes the gold.

HYPOTHESIS
  H16: running 7B on each of the 8 chunks yields 8 candidate answers whose AGREEMENT
  structure identifies the right one. Concretely, a symbol proposed from several
  independent chunks is more likely correct than one proposed from a single chunk.

ARMS (all gold-free, all decided from the 8 candidate strings alone)
  MAJORITY     most frequent non-empty answer across the 8 chunks
  WEIGHTED     majority weighted by each chunk's retrieval rank (1/(rank+1))
  AGREE_PICK   pick the CHUNK whose answer is the majority answer -> hand that chunk on
  SINGLETON    rank-0 chunk's answer (baseline)
  plus the H15 ORACLE pick as the unreachable ceiling.

WHY MAJORITY MIGHT WORK WHERE EVERYTHING ELSE FAILED
  H13/H14 tried to predict utility from the QUERY and the CHUNK. This instead uses the
  model's own behaviour ON that chunk as the signal -- a different information source,
  and the only one so far not derived from text similarity.

PRE-REGISTERED
  WIN  : some gold-free arm >= 0.35 (beats 14B RAG8 0.3083 and 7B RAG2 0.3292)
  WEAK : beats rank-0 (0.2750) but under RAG2
  FAIL : <= rank-0 -> agreement carries no selection signal; the stable target of H15
         is real but not identifiable without gold, and the cascade stays an upper bound.
  I expect WEAK-to-WIN: 68% of 7B's correct answers are also 14B-correct, which implies
  correct answers are less idiosyncratic than wrong ones, so they should agree more.

COST: A10G, 7B, 1920 short generations, answers captured as STRINGS => ~$0.25.
"""
import json, re, modal
from collections import Counter
SEP = "\n\n---\n\n"
MODEL = "Qwen/Qwen2.5-7B-Instruct"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h16-consistency")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A10G", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def capture(model=MODEL):
    import os; os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h7_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    prompts, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["RAG8"].split(SEP)):
            body = TPL.format(q=it["query"], e=c)
            prompts.append(tok.apply_chat_template([{"role": "user", "content": body}],
                                                   tokenize=False, add_generation_prompt=True))
            key.append((i, k))
    print(f"[plan] {len(prompts)} generations, capturing ANSWER STRINGS")
    res = llm.generate(prompts, sp)
    ans = [[""]*8 for _ in range(n)]
    for (i, k), r in zip(key, res):
        ans[i][k] = r.outputs[0].text.strip()
    hf_cache.commit()
    return {"model": model, "answers": ans, "gold": [it["gold"] for it in items], "n": n}


def norm(t):
    m = re.search(r"[A-Za-z_][\w.]*", (t or "").replace("`", ""))
    return m.group(0).split(".")[-1] if m else ""


@app.local_entrypoint()
def main(out: str = "h16_results.json"):
    r = capture.remote(); json.dump(r, open(out, "w"), indent=2)
    A, G, n = r["answers"], r["gold"], r["n"]
    L14 = json.load(open('h15_results.json'))["labels"]
    h12 = json.load(open('h12_results.json'))
    L7 = [[0]*8 for _ in range(n)]
    for x in h12["records"]:
        if x["arm"] == "ORACLE" and len(x["subset"]) == 1:
            L7[x["i"]][x["subset"][0]] = x["hit"]
    ok = lambda i, s: int(bool(s) and any(re.fullmatch(re.escape(g), s) for g in G[i]))

    maj, wgt, pick_agree = [], [], []
    vote_hist = Counter()
    for i in range(n):
        v = [norm(a) for a in A[i]]
        c = Counter(x for x in v if x)
        vote_hist[max(c.values()) if c else 0] += 1
        top = c.most_common(1)[0][0] if c else ""
        maj.append(ok(i, top))
        w = {}
        for k, x in enumerate(v):
            if x: w[x] = w.get(x, 0) + 1.0/(k+1)
        wt = max(w, key=w.get) if w else ""
        wgt.append(ok(i, wt))
        pick_agree.append(next((k for k, x in enumerate(v) if x == top), 0))

    S = lambda a: sum(a)/n
    rank0_7 = sum(L7[i][0] for i in range(n))/n
    orc7 = sum(max(L7[i]) for i in range(n))/n
    tr14_oracle = sum(L14[i][next((k for k in range(8) if L7[i][k]), 0)] for i in range(n))/n
    tr14_agree = sum(L14[i][pick_agree[i]] for i in range(n))/n
    rank0_14 = sum(L14[i][0] for i in range(n))/n

    print(f"\n{'='*80}\nH16 -- GOLD-FREE SELECTION VIA SELF-CONSISTENCY, n={n}\n{'='*80}")
    print(f"  vote concentration (max agreeing chunks per query): "
          + " ".join(f"{k}:{vote_hist.get(k,0)}" for k in sorted(vote_hist)))
    print(f"\n  {'arm':<40}{'score':>9}{'gold-free':>11}")
    print("-"*80)
    for lab, v, gf in (("7B rank-0 chunk", rank0_7, "yes"),
                       ("7B MAJORITY answer (8 chunks)", S(maj), "yes"),
                       ("7B RANK-WEIGHTED majority", S(wgt), "yes"),
                       ("7B oracle pick", orc7, "NO"),
                       ("14B rank-0", rank0_14, "yes"),
                       ("14B on AGREEMENT-picked chunk", tr14_agree, "yes"),
                       ("14B on 7B ORACLE-picked chunk", tr14_oracle, "NO")):
        print(f"  {lab:<40}{v:>9.4f}{gf:>11}")
    print(f"\n  references: 7B RAG2 0.3292@912 | 14B RAG8 0.3083@3399 | 7B RAG8 0.3875@3399")
    best = max(S(maj), S(wgt), tr14_agree)
    print(f"\n{'='*80}\nVERDICT\n{'='*80}")
    if best >= 0.35:
        print(f"  WIN -- gold-free selection reaches {best:.4f}, beating 14B RAG8 (0.3083)")
        print(f"  and 7B RAG2 (0.3292). The cascade is DEPLOYABLE, not just an upper bound.")
    elif best > rank0_7:
        print(f"  WEAK -- {best:.4f} beats rank-0 ({rank0_7:.4f}) but misses the 0.35 bar.")
    else:
        print(f"  FAIL -- {best:.4f} <= rank-0. Agreement carries no selection signal;")
        print("  H15's stable target is real but NOT identifiable without gold.")
