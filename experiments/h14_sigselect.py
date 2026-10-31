"""
H14 --- Can the MODEL select the culprit chunk from cheap SIGNATURES?

WHAT THE DATA SAYS
  P(answer | chunk defines the gold symbol) = 0.8190  vs 0.1957 otherwise (+62.3pp).
  The signal is in the content (WORLD A). But the gold symbol is named in the bug
  report only 20.4% of the time, so lexical/similarity features cannot find it --
  which is exactly why H13's utility model failed (defines_query_sym importance 0.039).

  The real task: infer WHICH function is buggy from a description that does not name
  it. That is inference, not retrieval mechanics -- an LLM's strength, an embedding's
  weakness.

ARCHITECTURE UNDER TEST
  stage 1  show only def/class SIGNATURES + first docstring line of each of the 8
           chunks (~400 tok total), ask the model to pick one
  stage 2  spend the budget on that ONE chunk (~496 tok)
  total    ~900 tok, MATCHED to RAG2 (912 tok, 0.3292)

  No stage-2 generation is needed: H12 already labeled every (query, chunk) singleton,
  so the selected chunk's outcome is a lookup. One generation per query.

CONTROLS
  - position control: distribution of chosen indices (is the model just picking #1?)
  - SHUFFLED presentation: chunks presented in a permuted order, so a positional
    habit cannot masquerade as selection skill. Same labels, permuted mapping.
  - rank-0 baseline 0.2750, RAG2 0.3292 @912 tok, ORACLE 0.5750 @496 tok.

PRE-REGISTERED
  WIN  : selection score > RAG2 (0.3292) at <=912 tok, and shuffled-order score is
         close to unshuffled (skill, not position bias).
  WEAK : beats rank-0 (0.2750) but not RAG2.
  FAIL : <= rank-0, or collapses under shuffling -> the model cannot infer the
         culprit from signatures either, and the 30pp oracle gap needs a new source.
  I expect WEAK-to-WIN. Signatures carry names and arg lists, which is most of what a
  maintainer uses; but 80% of reports never name the function, so this is genuinely hard.

COST: A10G, 7B, 240x2 short generations => ~$0.20.
"""
import json, re, modal
SEP = "\n\n---\n\n"
MODEL = "Qwen/Qwen2.5-7B-Instruct"
llm_image = (modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.6.6.post1", "transformers==4.48.3", "numpy==1.26.4")
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "VLLM_LOGGING_LEVEL": "WARNING"}))
app = modal.App("qcarve-h14-sigselect")
hf_cache = modal.Volume.from_name("qcarve-hf-cache", create_if_missing=True)
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


def signature_of(chunk, max_defs=6):
    """Cheap structural summary: def/class lines + first docstring line."""
    out, lines = [], chunk.split("\n")
    for i, l in enumerate(lines):
        m = re.match(r"\s*(?:async\s+)?(def|class)\s+([A-Za-z_]\w*)\s*(\([^)]*\))?", l)
        if m:
            sig = f"{m.group(1)} {m.group(2)}{(m.group(3) or '')[:90]}"
            doc = ""
            for j in range(i+1, min(i+4, len(lines))):
                s = lines[j].strip()
                if s.startswith(('"""', "'''")):
                    doc = s.strip('"\' ')[:70]; break
            out.append(sig + (f"  # {doc}" if doc else ""))
        if len(out) >= max_defs: break
    if not out:
        head = [l for l in lines if l.strip()][:2]
        out = ["(no definitions) " + " ".join(head)[:110]]
    return "\n".join(out)


@app.function(image=llm_image, gpu="A10G", timeout=3600,
              volumes={"/hf": hf_cache, "/data": data_vol})
def select(labels, model=MODEL):
    import os; os.environ["HF_HOME"] = "/hf"
    from vllm import LLM, SamplingParams
    items = json.load(open("/data/h7_items.json")); n = len(items)
    llm = LLM(model=model, gpu_memory_utilization=0.92, max_model_len=8192,
              enable_prefix_caching=True, disable_log_stats=True)
    tok = llm.get_tokenizer(); sp = SamplingParams(temperature=0.0, max_tokens=8)

    TPL = ("A bug has been reported in a Python repository.\n\nBUG REPORT:\n{q}\n\n"
           "Below are {k} candidate code locations, summarised by their definitions.\n\n{s}\n\n"
           "Which candidate most likely contains the function or class that must be "
           "modified to fix this bug?\nAnswer with ONLY the candidate number.")

    # deterministic permutation per query (no RNG: index arithmetic)
    perm_of = lambda i: [(j * 3 + i) % 8 for j in range(8)]

    out = {}
    for mode in ("ordered", "shuffled"):
        prompts, ntoks, maps = [], [], []
        for i, it in enumerate(items):
            ch = it["RAG8"].split(SEP)
            order = list(range(8)) if mode == "ordered" else perm_of(i)
            s = "\n\n".join(f"[{p+1}]\n{signature_of(ch[c])}" for p, c in enumerate(order))
            body = TPL.format(q=it["query"], k=8, s=s)
            prompts.append(tok.apply_chat_template([{"role": "user", "content": body}],
                                                   tokenize=False, add_generation_prompt=True))
            ntoks.append(len(tok(body)["input_ids"])); maps.append(order)
        res = llm.generate(prompts, sp)
        recs = []
        for i, (r, nt, order) in enumerate(zip(res, ntoks, maps)):
            m = re.search(r"\d+", r.outputs[0].text)
            pos = int(m.group(0)) - 1 if m else 0
            pos = pos if 0 <= pos < 8 else 0
            chosen = order[pos]
            recs.append({"i": i, "pos": pos, "chunk": chosen, "hit": labels[i][chunk_ix(chosen)],
                         "sig_tok": nt, "repo": items[i]["repo"]})
        out[mode] = recs
        print(f"  {mode:<9} selection score = {sum(x['hit'] for x in recs)/n:.4f}  "
              f"sig prompt tok = {sum(x['sig_tok'] for x in recs)/n:.0f}")
    hf_cache.commit()
    return {"model": model, "modes": out, "n": n}


def chunk_ix(c):
    return c


@app.local_entrypoint()
def main(out: str = "h14_results.json"):
    h12 = json.load(open("h12_results.json")); n = h12["n_items"]
    labels = [[0]*8 for _ in range(n)]
    for x in h12["records"]:
        if x["arm"] == "ORACLE" and len(x["subset"]) == 1:
            labels[x["i"]][x["subset"][0]] = x["hit"]
    r = select.remote(labels); json.dump(r, open(out, "w"), indent=2)

    ORACLE, RANK0, RAG2, RAG8 = 0.5750, 0.2750, 0.3292, 0.3875
    print(f"\n{'='*78}\nH14 -- SIGNATURE-BASED LLM SELECTION\n{'='*78}")
    sc = {}
    for mode, recs in r["modes"].items():
        s = sum(x["hit"] for x in recs)/n
        st = sum(x["sig_tok"] for x in recs)/n
        sc[mode] = s
        from collections import Counter
        c = Counter(x["pos"] for x in recs)
        print(f"  {mode:<9} score={s:.4f}  total tok ~= {st:.0f}+496 = {st+496:.0f}")
        print(f"            chosen position histogram: "
              + " ".join(f"{k+1}:{c.get(k,0)}" for k in range(8)))
    print(f"\n  reference:  rank-0 {RANK0:.4f} @496 | RAG2 {RAG2:.4f} @912 | "
          f"RAG8 {RAG8:.4f} @3399 | ORACLE {ORACLE:.4f} @496")
    best = max(sc.values()); drop = abs(sc["ordered"] - sc["shuffled"])
    print(f"\n{'='*78}\nVERDICT\n{'='*78}")
    print(f"  ordered-vs-shuffled gap = {drop*100:.1f}pp "
          f"({'position bias suspected' if drop > 0.05 else 'stable under permutation'})")
    if best > RAG2 and drop <= 0.05:
        print(f"  WIN -- {best:.4f} beats RAG2 ({RAG2:.4f}) at a matched ~900 tok budget,")
        print(f"  and survives permutation. Closes {(best-RANK0)/(ORACLE-RANK0)*100:.0f}% "
              f"of the rank-0 -> oracle gap.")
    elif best > RANK0:
        print(f"  WEAK -- {best:.4f} beats rank-0 ({RANK0:.4f}) but not RAG2 ({RAG2:.4f}).")
        print(f"  Closes {(best-RANK0)/(ORACLE-RANK0)*100:.0f}% of the rank-0 -> oracle gap.")
    else:
        print(f"  FAIL -- {best:.4f} <= rank-0. The model cannot infer the culprit from")
        print("  signatures. The 30pp oracle gap needs an information source beyond text.")
