"""
H24 --- THE NULL MODEL: how much of "retrieval performance" is just the model's PRIOR?

WHY THIS CONTROL IS OVERDUE
  H23 refuted grounding in the opposite direction: P(correct | answer IS in chunk)
  = 0.1517 vs 0.2098 when it is NOT. Answers the model produces WITHOUT support from
  the chunk are MORE often right than ones read off the page.

  That has an implication I never tested: if the model can name the culprit without
  using the evidence, it may be able to name it with NO evidence at all. These repos
  (flask, requests, urllib3, jinja...) are famous open-source projects almost certainly
  in pretraining. The model may simply KNOW that `save_session` lives in the session
  module.

  If a zero-evidence baseline scores near RAG8, then most of what I have been
  measuring is PRIOR, not retrieval, and every gap in this programme is inflated.
  This is the single most important missing control in the whole session.

ARMS
  NULL_NOCTX   bug report only, no code evidence at all
  NULL_REPO    bug report + repository name only ("This is a bug in flask.")
  RAG8         full evidence (reference, from H23)

PRE-REGISTERED
  CLEAN   : null <= 0.10  -> evidence is doing the work; all prior results stand.
  INFLATED: null 0.10-0.20 -> a meaningful share of every score is prior; gaps should
            be restated relative to the null floor, not zero.
  SEVERE  : null > 0.20 (i.e. ~= rank-0's 0.2729) -> retrieval is contributing far less
            than reported and the corpus is contaminated by pretraining memorisation.
  I expect INFLATED, possibly SEVERE. H23's -5.8pp finding is hard to explain any
  other way. Stating this before the run.

  NOTE: a high null does NOT invalidate the ORACLE gap (oracle and RAG8 share the same
  prior), but it does mean absolute accuracies overstate retrieval's contribution, and
  it would explain why gold-free selection keeps failing -- the model is not reading
  the chunk in the first place.

COST: A10G 7B, ~1100 generations => ~$0.10.
"""
import json, os, re, modal
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h24-null")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)

NOCTX = ("You are a code maintainer. A bug has been reported.\n\nBUG REPORT:\n{q}\n\n"
         "Which single function or class must be modified to fix this bug?\n"
         "Answer with ONLY the name, nothing else.")
REPOCTX = ("You are a maintainer of the open-source Python project `{r}`.\n\n"
           "BUG REPORT:\n{q}\n\n"
           "Which single function or class in `{r}` must be modified to fix this bug?\n"
           "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A10G", timeout=3600,
              volumes={"/hf": hf_cache, "/data": data_vol})
def run(model="Qwen/Qwen2.5-7B-Instruct"):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key = [], []
    for i, it in enumerate(items):
        pr.append(NOCTX.format(q=it["query"])); key.append((i, "NOCTX"))
        pr.append(REPOCTX.format(q=it["query"], r=it["repo"])); key.append((i, "REPO"))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in pr]
    print(f"[plan] {len(chat)} zero-evidence generations")
    res = llm.generate(chat, sp)
    out = {"NOCTX": [0]*n, "REPO": [0]*n}
    for (i, arm), r in zip(key, res):
        out[arm][i] = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                              for g in items[i]["gold"]))
    hf_cache.commit()
    return {"model": model, "n": n, **out}


@app.local_entrypoint()
def main(out: str = "h24_results.json"):
    r = run.remote(); json.dump(r, open(out, "w"), indent=2)
    H = json.load(open("h21_results.json")); H23 = json.load(open("h23_results.json"))
    pr = H["build"]["per_repo"]; repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    n = r["n"]; real = [i for i in range(n) if repos[i] not in SMALL]
    f = lambda v: sum(v[i] for i in real)/len(real)
    S7 = H["r7"]["S"]; P7 = H["r7"]["R"]
    nc, rp_ = f(r["NOCTX"]), f(r["REPO"])
    rag8 = f(P7); rk0 = f([S7[i][0] for i in range(n)])
    orc = sum(max(S7[i]) for i in real)/len(real)
    print(f"\n{'='*76}\nH24 -- NULL MODEL, 7B, 8 real repos (n={len(real)})\n{'='*76}")
    print(f"  {'arm':<34}{'score':>9}{'evidence tokens':>18}")
    print("-"*76)
    for lab, v, t in (("NULL: bug report only", nc, 0),
                      ("NULL: + repo name", rp_, 0),
                      ("rank-0 chunk", rk0, 496),
                      ("RAG8 (full)", rag8, 3399),
                      ("ORACLE (upper bound)", orc, 496)):
        print(f"  {lab:<34}{v:>9.4f}{t:>18}")
    best_null = max(nc, rp_)
    print(f"\n  evidence contribution (RAG8 - null): {(rag8-best_null)*100:+.1f}pp")
    print(f"  oracle gain ABOVE the null floor    : {(orc-best_null)*100:+.1f}pp")
    print(f"  share of RAG8 explained by prior    : {best_null/rag8:.1%}")
    print(f"\n{'='*76}\nVERDICT\n{'='*76}")
    if best_null <= 0.10:
        print(f"  CLEAN -- null {best_null:.4f}. Evidence is doing the work; results stand.")
    elif best_null <= 0.20:
        print(f"  INFLATED -- null {best_null:.4f}. {best_null/rag8:.0%} of RAG8's score is")
        print("  prior, not retrieval. Restate absolute numbers relative to this floor.")
    else:
        print(f"  SEVERE -- null {best_null:.4f}, at or above rank-0 ({rk0:.4f}).")
        print("  These repos are memorised from pretraining. Retrieval contributes far")
        print("  less than reported, and that explains why gold-free selection keeps")
        print("  failing: the model is barely reading the chunk at all.")
