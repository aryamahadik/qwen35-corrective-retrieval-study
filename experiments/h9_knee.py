"""
H9 --- WHERE IS THE KNEE ON THE CHUNK CURVE?

H8 showed the accuracy-vs-evidence slope FLATTENS 10x from 7B to 14B: RAG3 costs
4.6pp at 7B but only 0.4pp at 14B, at 2.57x fewer tokens. Two points cannot locate
a knee. Everything below 1,324 tokens is unmeasured, and that is exactly the region
the 4x target lives in.

HYPOTHESIS
  H9: plain RAG@k is flat down to some k*, and 1/rho(k*) locates the true achievable
      token reduction at <=1pp -- WITHOUT any Q-CARVE machinery.

WHY THIS MATTERS EVEN THOUGH IT HELPS THE BASELINE
  If the baseline itself reaches 4x by retrieving less, the breakthrough region is
  reachable but there is NO ARCHITECTURE TO SELL. That is decision-relevant and it is
  the scientifically correct thing to measure. Reporting it is the point.

METHOD -- zero new retrieval. The stored RAG8 evidence is chunks joined by a
separator; slicing it yields exact RAG@1..8 arms. FAST3 carried along unchanged as
the architecture's arm. Both model scales, so the verdict is not scale-specific.

PRE-REGISTERED
  For each arm: Delta = acc(RAG8) - acc(arm). Achievable reduction = max tokens x
  over arms with Delta <= 1.0pp. Compare to target 4.00x.
  If FAST3 is not on the frontier, the architecture is dominated by plain RAG.

COST: A100-40GB, two models, ~25 min => ~$1.00.
"""
import json, re, modal

SEP = "\n\n---\n\n"
MODELS = ["Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-14B-Instruct"]
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h9-knee")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


@app.function(image=llm_image, gpu="A100-40GB", timeout=5400,
              volumes={"/hf": hf_cache, "/data": data_vol})
def sweep(model):
    import os; os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h7_items.json"))

    # integrity check: slicing must reproduce the original chunk count
    bad = sum(1 for it in items if len(it["RAG8"].split(SEP)) != 8)
    print(f"[integrity] items whose RAG8 does not split into exactly 8: {bad}/{len(items)}")

    arms = {}
    for k in (1, 2, 3, 4, 6, 8):
        arms[f"RAG{k}"] = [SEP.join(it["RAG8"].split(SEP)[:k]) for it in items]
    arms["FAST3"] = [it["FAST3"] for it in items]

    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=False, disable_log_stats=True)
    tok = llm.get_tokenizer()
    sp = SamplingParams(temperature=0.0, max_tokens=24)
    TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
           "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
           "Which single function or class must be modified to fix this bug?\n"
           "Answer with ONLY the name, nothing else.")

    out = {}
    for arm, evs in arms.items():
        prompts, ntoks = [], []
        for it, ev in zip(items, evs):
            if len(tok(TPL.format(q=it["query"], e=ev))["input_ids"]) > 7800:
                ev = tok.decode(tok(ev)["input_ids"][:7400])
            p = TPL.format(q=it["query"], e=ev)
            prompts.append(tok.apply_chat_template([{"role": "user", "content": p}],
                                                   tokenize=False, add_generation_prompt=True))
            ntoks.append(len(tok(p)["input_ids"]))
        res = llm.generate(prompts, sp)
        recs = [{"repo": it["repo"], "hit": int(any(re.search(rf"\b{re.escape(g)}\b",
                 r.outputs[0].text) for g in it["gold"])), "n_tok": nt}
                for it, r, nt in zip(items, res, ntoks)]
        out[arm] = recs
        print(f"  {arm:<7} acc={sum(x['hit'] for x in recs)/len(recs):.4f}  "
              f"tok={sum(x['n_tok'] for x in recs)/len(recs):.0f}")
    hf_cache.commit()
    return {"model": model, "arms": out, "split_integrity_failures": bad}


@app.local_entrypoint()
def main(out: str = "h9_results.json"):
    allr = list(sweep.map(MODELS))
    json.dump(allr, open(out, "w"), indent=2)
    for r in allr:
        A = r["arms"]; n = len(A["RAG8"])
        acc = lambda a: sum(x["hit"] for x in A[a]) / n
        tkn = lambda a: sum(x["n_tok"] for x in A[a]) / n
        base, bt = acc("RAG8"), tkn("RAG8")
        print(f"\n{'='*80}\n{r['model']}   n={n}   "
              f"(split integrity failures: {r['split_integrity_failures']})\n{'='*80}")
        print(f"{'arm':<8}{'accuracy':>10}{'mean tok':>10}{'tokens x':>10}{'Delta pp':>11}{'':>4}")
        print("-"*80)
        ok = []
        for a in ("RAG1","RAG2","RAG3","RAG4","RAG6","RAG8","FAST3"):
            d = (base - acc(a)) * 100; x = bt / tkn(a)
            flag = "  <= 1pp" if d <= 1.0 else ""
            if d <= 1.0: ok.append((x, a, d))
            print(f"{a:<8}{acc(a):>10.4f}{tkn(a):>10.0f}{x:>9.2f}x{d:>10.1f}pp{flag}")
        if ok:
            x, a, d = max(ok)
            print(f"\n  BEST at <=1pp quality loss: {a} -> {x:.2f}x fewer tokens ({d:.2f}pp)")
            print(f"  target 4.00x -> {'ACHIEVED' if x >= 4 else 'MISSED'}"
                  f"    2x stretch -> {'ACHIEVED' if x >= 2 else 'MISSED'}")
            fd = (base - acc("FAST3")) * 100
            print(f"  FAST3 (the architecture): {bt/tkn('FAST3'):.2f}x at {fd:.1f}pp -> "
                  + ("ON the frontier" if fd <= 1.0 else "DOMINATED by plain RAG"))
        else:
            print("\n  No arm holds <=1pp.")
