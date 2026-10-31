"""
H15 --- Is "which chunk works" a STABLE property of the evidence, or one model's noise?

WHY THIS NOW
  Five mechanisms recover ~none of H12's 30pp oracle gap: embeddings, cross-encoder
  relevance, learned utility features, LLM inference over signatures, rank order.
  Before proposing a sixth selector, test whether there is a stable target to select.

  H12's labels come from ONE model at temperature 0. Deterministic is not the same as
  learnable: the map (query, chunk) -> hit could be that model's idiosyncrasy. If so,
  best-of-8 harvests per-model noise and NO selector could ever capture it.

THE TEST
  Relabel the identical 1920 (query, chunk) singletons with a DIFFERENT model (14B),
  then evaluate 7B's ORACLE CHOICE under 14B's labels.

    transfer ~= oracle_14B   -> the winning chunk is a property of the EVIDENCE.
                               The gap is real and learnable; we lack the features.
    transfer ~= rank0_14B    -> the winning chunk is model-specific NOISE.
                               H12's headroom is largely illusory and must be restated.

  Also reported: per-pair agreement and Cohen's kappa between 7B and 14B labels, and
  the ceiling a perfect 7B-trained selector could reach on 14B.

PRE-REGISTERED
  STABLE   : transfer >= rank0_14B + 0.5*(oracle_14B - rank0_14B)
  NOISE    : transfer <= rank0_14B + 0.2*(oracle_14B - rank0_14B)
  PARTIAL  : in between.
  I expect PARTIAL leaning NOISE. Per-chunk hit rate is 0.2333 while independent
  best-of-8 would give 0.882 vs the observed 0.575, so outcomes are strongly
  correlated within a query -- consistent with "some queries are hard" plus a large
  idiosyncratic component. Stating this before the run.

COST: A100-40GB, 14B, 1920 short generations => ~$0.40.
"""
import json, re, modal
SEP = "\n\n---\n\n"
MODEL = "Qwen/Qwen2.5-14B-Instruct"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h15-transfer")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A100-40GB", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def relabel(model=MODEL):
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
    print(f"[plan] {len(prompts)} singleton relabels with {model}")
    res = llm.generate(prompts, sp)
    lab = [[0]*8 for _ in range(n)]
    for (i, k), r in zip(key, res):
        lab[i][k] = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                            for g in items[i]["gold"]))
    hf_cache.commit()
    return {"model": model, "labels": lab, "n": n}


@app.local_entrypoint()
def main(out: str = "h15_results.json"):
    h12 = json.load(open("h12_results.json")); n = h12["n_items"]
    L7 = [[0]*8 for _ in range(n)]
    for x in h12["records"]:
        if x["arm"] == "ORACLE" and len(x["subset"]) == 1:
            L7[x["i"]][x["subset"][0]] = x["hit"]
    r = relabel.remote(); json.dump(r, open(out, "w"), indent=2)
    L14 = r["labels"]

    flat7 = [L7[i][k] for i in range(n) for k in range(8)]
    flat14 = [L14[i][k] for i in range(n) for k in range(8)]
    N = len(flat7)
    agree = sum(a == b for a, b in zip(flat7, flat14)) / N
    p7, p14 = sum(flat7)/N, sum(flat14)/N
    pe = p7*p14 + (1-p7)*(1-p14)
    kappa = (agree - pe) / (1 - pe) if pe < 1 else 0.0
    both = sum(1 for a, b in zip(flat7, flat14) if a and b)

    rank0_14 = sum(L14[i][0] for i in range(n)) / n
    oracle_14 = sum(max(L14[i]) for i in range(n)) / n
    oracle_7 = sum(max(L7[i]) for i in range(n)) / n
    # 7B's oracle choice, evaluated on 14B
    pick = [next((k for k in range(8) if L7[i][k]), 0) for i in range(n)]
    transfer = sum(L14[i][pick[i]] for i in range(n)) / n

    print(f"\n{'='*78}\nH15 -- LABEL TRANSFER 7B -> 14B, n={N} (query,chunk) pairs\n{'='*78}")
    print(f"  per-chunk hit rate     7B {p7:.4f}   14B {p14:.4f}")
    print(f"  raw agreement          {agree:.4f}")
    print(f"  Cohen's kappa          {kappa:.4f}   "
          f"({'slight' if kappa<0.2 else 'fair' if kappa<0.4 else 'moderate' if kappa<0.6 else 'substantial'})")
    print(f"  pairs BOTH models solve {both} / {sum(flat7)} of 7B's successes "
          f"({both/max(1,sum(flat7)):.1%})")
    print(f"\n  14B rank-0 baseline    {rank0_14:.4f}")
    print(f"  14B TRANSFER (7B pick) {transfer:.4f}")
    print(f"  14B own oracle         {oracle_14:.4f}    (7B oracle was {oracle_7:.4f})")
    span = oracle_14 - rank0_14
    frac = (transfer - rank0_14) / span if span > 0 else 0.0
    print(f"\n  transfer closes {frac*100:.0f}% of 14B's own rank-0 -> oracle gap")
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    if frac >= 0.5:
        print("  STABLE -- the winning chunk is a property of the EVIDENCE, not the model.")
        print("  H12's headroom is real and learnable; we simply lack the right features.")
    elif frac <= 0.2:
        print("  NOISE -- the winning chunk does NOT transfer across models. Best-of-8")
        print("  largely harvests per-model idiosyncrasy. NO selector could capture it,")
        print("  and H12's 30pp headroom must be restated as mostly illusory.")
    else:
        print(f"  PARTIAL -- {frac*100:.0f}% transfers. Some stable signal, a large")
        print("  idiosyncratic component. Any selector is capped well below the oracle.")
