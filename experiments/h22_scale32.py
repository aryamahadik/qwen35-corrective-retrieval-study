"""
H22 --- Does the oracle gap survive at 32B? (the last flagged UNKNOWN)

WHY THIS IS THE RIGHT LAST EXPERIMENT
  H21 validated at 10-repo scale: oracle gap +14.2pp, transfer +6.7pp, kappa 0.678
  (8 non-degenerate repos, n=480). But every oracle/transfer number so far comes from
  7B and 14B, and H9 showed model scale CHANGES compression behaviour: 32B kept
  improving monotonically with more evidence (+3.8,+2.5,+2.9,+2.1,+1.7pp) and had not
  plateaued at 3,399 tokens, while achievable <=1pp compression went 1.32x/2.57x/1.00x
  across 7B/14B/32B -- non-monotone.

  If stronger models genuinely use long context better, "a small context suffices"
  should WEAKEN with scale. That is the live threat to the whole finding.

MEASURED, on the identical H21 corpus and gold
  32B RAG8, 32B singleton oracle, 32B rank-0
  TRANSFER: 32B evaluated on the chunk 7B's labels picked  (7B -> 32B, a 4.6x jump)
  Cohen's kappa 7B vs 32B

PRE-REGISTERED
  SURVIVES : 32B oracle gap >= +10pp AND transfer > RAG8.
  WEAKENS  : gap +5..10pp, or transfer <= RAG8 -> effect is scale-sensitive; restate
             the claim as holding at <=14B and unproven above.
  VANISHES : gap < +5pp -> the finding is an artifact of weak models and does not
             generalise to capable ones. This would substantially deflate the result.
  I expect WEAKENS. H9's evidence that 32B exploits long context better is direct and
  points against the premise. Stating that before the run.

COST: A100-80GB, 32B, 5013 generations => ~$1.
"""
import json, os, re, modal
SEP = "\n\n---\n\n"
MODEL = "Qwen/Qwen2.5-32B-Instruct"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h22-scale32")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)
TPL = ("You are a code maintainer. Below is a bug report and code from the repository.\n\n"
       "BUG REPORT:\n{q}\n\nCODE EVIDENCE:\n{e}\n\n"
       "Which single function or class must be modified to fix this bug?\n"
       "Answer with ONLY the name, nothing else.")


@app.function(image=llm_image, gpu="A100-80GB", timeout=7200,
              volumes={"/hf": hf_cache, "/data": data_vol})
def label32(model=MODEL):
    os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h21_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.95, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=24)
    pr, key = [], []
    for i, it in enumerate(items):
        for k, c in enumerate(it["chunks"]):
            pr.append(TPL.format(q=it["query"], e=c)); key.append((i, "S", k))
        pr.append(TPL.format(q=it["query"], e=SEP.join(it["chunks"]))); key.append((i, "R", 0))
    chat = [tok.apply_chat_template([{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True) for p in pr]
    print(f"[{model}] {len(chat)} generations")
    res = llm.generate(chat, sp)
    S = [[0]*8 for _ in range(n)]; R = [0]*n
    for (i, arm, k), r in zip(key, res):
        hit = int(any(re.search(rf"\b{re.escape(g)}\b", r.outputs[0].text)
                      for g in items[i]["gold"]))
        if arm == "R": R[i] = hit
        elif k < 8: S[i][k] = hit
    hf_cache.commit()
    return {"model": model, "n": n, "S": S, "R": R}


@app.local_entrypoint()
def main(out: str = "h22_results.json"):
    H = json.load(open("h21_results.json"))
    S7, P7 = H["r7"]["S"], H["r7"]["R"]
    pr = H["build"]["per_repo"]
    repos = []
    for rp, c in pr.items(): repos += [rp]*c
    SMALL = {"itsdangerous", "cachecontrol"}
    r = label32.remote(); json.dump(r, open(out, "w"), indent=2)
    S32, R32, n = r["S"], r["R"], r["n"]
    pick = [next((k for k in range(8) if S7[i][k]), 0) for i in range(n)]
    real = [i for i in range(n) if repos[i] not in SMALL]

    def blk(ix, S, R, lab):
        m = len(ix); f = lambda v: sum(v)/m
        rag = f([R[i] for i in ix]); orc = f([max(S[i]) for i in ix])
        rk0 = f([S[i][0] for i in ix]); tr = f([S[i][pick[i]] for i in ix])
        print(f"  {lab:<22}{m:>5}{rag:>9.4f}{rk0:>9.4f}{tr:>10.4f}{orc:>9.4f}"
              f"{(orc-rag)*100:>8.1f}p{(tr-rag)*100:>9.1f}p")
        return orc-rag, tr-rag
    print(f"\n{'='*92}\nH22 -- 32B ON THE H21 CORPUS (identical items and gold)\n{'='*92}")
    print(f"  {'set':<22}{'n':>5}{'RAG8':>9}{'rank0':>9}{'TRANSFER':>10}{'oracle':>9}"
          f"{'gap':>9}{'tr-RAG8':>10}")
    print("-"*92)
    blk(list(range(n)), S32, R32, "32B all 10 repos")
    g32, t32 = blk(real, S32, R32, "32B 8 real repos")
    f7 = [S7[i][k] for i in range(n) for k in range(8)]
    f32 = [S32[i][k] for i in range(n) for k in range(8)]
    N = len(f7); ag = sum(a == b for a, b in zip(f7, f32))/N
    p7, p32 = sum(f7)/N, sum(f32)/N; pe = p7*p32 + (1-p7)*(1-p32)
    print(f"\n  Cohen's kappa 7B vs 32B: {(ag-pe)/(1-pe):.4f}   (7B vs 14B was 0.6776)")
    print(f"\n  scale ladder, oracle gap on 8 real repos:")
    print(f"    7B  +14.2pp     14B (via transfer arm)     32B {g32*100:+.1f}pp")
    print(f"\n{'='*92}\nVERDICT\n{'='*92}")
    if g32*100 >= 10 and t32 > 0:
        print(f"  SURVIVES -- 32B oracle gap {g32*100:+.1f}pp, transfer {t32*100:+.1f}pp.")
        print("  The finding is NOT an artifact of weak models.")
    elif g32*100 >= 5:
        print(f"  WEAKENS -- gap {g32*100:+.1f}pp, transfer {t32*100:+.1f}pp at 32B.")
        print("  Restate: holds at <=14B, attenuates with capability.")
    else:
        print(f"  VANISHES -- gap {g32*100:+.1f}pp. The finding does not generalise to")
        print("  capable models and must be substantially deflated.")
