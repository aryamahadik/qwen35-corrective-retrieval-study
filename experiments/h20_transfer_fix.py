"""
H20 --- Does H15's TRANSFER result survive corrected gold?

WHY THIS IS MANDATORY, NOT OPTIONAL
  H19 just showed the funcname-gold defect was NOT common-mode: under AST gold the
  oracle fell 10.0pp while RAG8 fell only 5.4pp, cutting H12's headline from +18.7pp
  to +14.2pp. Hub names gave best-of-8 eight chances to score a spurious hit.

  H15's transfer number is the load-bearing claim of the whole programme -- the only
  result that beat a matched RAG baseline (14B on 7B's picked chunk: 0.4000 @496 tok
  vs 0.3083 @3399, +9.2pp at 6.85x fewer tokens). It used the SAME defective labels,
  and it is ALSO a best-of-style selection, so it is exposed to the same inflation.
  Guessing at the correction is not acceptable; this measures it.

METHOD
  Relabel all 1920 singletons + 240 RAG8 prompts with 14B, scoring against gold_ast
  (from /data/h19_items.json). Recompute, under corrected labels:
    - 14B rank-0, 14B own oracle, 14B RAG8
    - TRANSFER: 14B evaluated on the chunk 7B's corrected labels picked
    - Cohen's kappa between 7B and 14B corrected labels

PRE-REGISTERED
  HOLDS    : transfer still beats 14B RAG8 by >= 5pp  -> claim stands, restated.
  WEAKENED : beats RAG8 by 0..5pp                      -> restate, much smaller.
  RETRACTED: transfer <= 14B RAG8                      -> the one positive result of
             the programme does not survive clean labels and must be withdrawn.
  Given H19, I expect WEAKENED. Stating that before the run.

COST: A100-40GB, 14B, ~2160 generations => ~$0.40.
"""
import json, os, re, modal
SEP = "\n\n---\n\n"
MODEL = "Qwen/Qwen2.5-14B-Instruct"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h20-transferfix")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A100-40GB", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def relabel(model=MODEL):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h19_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    prompts, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["RAG8"].split(SEP)):
            prompts.append(TPL.format(q=it["query"], e=c)); key.append((i, "S", k))
        prompts.append(TPL.format(q=it["query"], e=it["RAG8"])); key.append((i, "R", 0))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in prompts]
    print(f"[plan] {len(chat)} generations with {model}")
    res = llm.generate(chat, sp)
    S = [[0]*8 for _ in range(n)]; R = [0]*n
    for (i, arm, k), r in zip(key, res):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in items[i]["gold_ast"]))
        if arm == "R":
            R[i] = hit
        else:
            S[i][k] = hit
    hf_cache.commit()
    return {"model": model, "n": n, "S14": S, "R14": R}


@app.local_entrypoint()
def main(out: str = "h20_results.json"):
    h19 = json.load(open("h19_results.json"))
    S7, R7 = h19["S"], h19["R"]                 # 7B under CORRECTED gold
    r = relabel.remote(); json.dump(r, open(out, "w"), indent=2)
    S14, R14, n = r["S14"], r["R14"], r["n"]

    f7 = [S7[i][k] for i in range(n) for k in range(8)]
    f14 = [S14[i][k] for i in range(n) for k in range(8)]
    N = len(f7); agree = sum(a == b for a, b in zip(f7, f14))/N
    p7, p14 = sum(f7)/N, sum(f14)/N
    pe = p7*p14 + (1-p7)*(1-p14)
    kappa = (agree - pe)/(1-pe) if pe < 1 else 0.0

    pick = [next((k for k in range(8) if S7[i][k]), 0) for i in range(n)]
    Sm = lambda v: sum(v)/n
    rank0 = Sm([S14[i][0] for i in range(n)])
    transfer = Sm([S14[i][pick[i]] for i in range(n)])
    oracle14 = Sm([max(S14[i]) for i in range(n)])
    rag8 = Sm(R14)

    print(f"\n{'='*78}\nH20 -- TRANSFER UNDER CORRECTED GOLD, 14B, n={n}\n{'='*78}")
    print(f"  Cohen's kappa 7B vs 14B (corrected): {kappa:.4f}   (was 0.6693 on old gold)")
    print(f"\n  {'arm':<38}{'score':>9}{'tokens':>9}")
    print("-"*78)
    for lab, v, t in (("14B RAG8 (full retrieval)", rag8, 3399),
                      ("14B rank-0 chunk", rank0, 496),
                      ("14B on 7B's picked chunk (TRANSFER)", transfer, 496),
                      ("14B own oracle", oracle14, 496)):
        print(f"  {lab:<38}{v:>9.4f}{t:>9}")
    d = (transfer - rag8)*100
    print(f"\n  TRANSFER vs RAG8: {d:+.1f}pp at {3399/496:.2f}x fewer tokens")
    print(f"  (old-gold values were: transfer 0.4000, RAG8 0.3083, +9.2pp)")
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if d >= 5:
        print(f"  HOLDS -- transfer still beats matched RAG8 by {d:+.1f}pp at 6.85x fewer")
        print("  tokens under corrected labels. The programme's one positive result stands.")
    elif d > 0:
        print(f"  WEAKENED -- transfer beats RAG8 by only {d:+.1f}pp. Restate at this value;")
        print("  the effect is real but much smaller than reported.")
    else:
        print(f"  RETRACTED -- transfer {d:+.1f}pp vs RAG8 under clean labels. The one")
        print("  positive result of the programme does NOT survive and is withdrawn.")
