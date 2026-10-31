"""
GATE before spending on H14 (execution traces).

H13 showed a 30pp oracle gap that surface features cannot touch. Two very different
worlds are consistent with that, and they imply opposite next steps:

  A) Containing the GOLD symbol strongly predicts utility.
     -> the signal IS in the content; retrieval/encoders can in principle find it;
        execution traces would be overkill. Build a better encoder.
  B) Containing the gold symbol barely predicts utility.
     -> having the right code in context does NOT determine whether the model
        answers. That caps EVERY retrieval improvement, and a new information
        source is required.

This is CPU-only, no GPU, no generation -- it reuses H12's labels.
"""
import json, re, modal
SEP = "\n\n---\n\n"
image = modal.Image.debian_slim(python_version="3.11")
app = modal.App("qcarve-h13b-gate")
data_vol = modal.Volume.from_name("qcarve-h7-data", create_if_missing=True)


@app.function(image=image, timeout=900, volumes={"/data": data_vol})
def gate(labels):
    items = json.load(open("/data/h7_items.json"))
    n = len(items)
    cells = {(0,0):0,(0,1):0,(1,0):0,(1,1):0}
    per_q = []
    for i, it in enumerate(items):
        ch = it["RAG8"].split(SEP); gold = it["gold"]
        gflags = []
        for k, c in enumerate(ch):
            has = int(any(re.search(rf"(?:def|class)\s+{re.escape(g)}\b", c) for g in gold))
            cells[(has, labels[i][k])] += 1
            gflags.append(has)
        per_q.append((gflags, labels[i]))
    return {"cells": {f"{a}{b}": v for (a,b), v in cells.items()},
            "per_q": per_q, "n": n}


@app.local_entrypoint()
def main():
    h12 = json.load(open("h12_results.json")); n = h12["n_items"]
    labels = [[0]*8 for _ in range(n)]
    for x in h12["records"]:
        if x["arm"] == "ORACLE" and len(x["subset"]) == 1:
            labels[x["i"]][x["subset"][0]] = x["hit"]
    r = gate.remote(labels)
    c = r["cells"]
    n00,n01,n10,n11 = c["00"],c["01"],c["10"],c["11"]
    tot = n00+n01+n10+n11
    p_hit_gold = n11/max(1,(n10+n11)); p_hit_nogold = n01/max(1,(n00+n01))
    print(f"\n{'='*74}\nGATE: does CONTAINING THE GOLD SYMBOL predict chunk utility?\n{'='*74}")
    print(f"  (query,chunk) pairs: {tot}")
    print(f"  chunks that DEFINE a gold symbol : {n10+n11} ({(n10+n11)/tot:.1%})\n")
    print(f"  P(model answers | chunk defines gold)     = {p_hit_gold:.4f}   (n={n10+n11})")
    print(f"  P(model answers | chunk does NOT)         = {p_hit_nogold:.4f}   (n={n00+n01})")
    print(f"  LIFT                                      = {(p_hit_gold-p_hit_nogold)*100:+.1f}pp")
    # how many solvable queries have NO gold-defining chunk at all?
    both = sum(1 for g,l in r["per_q"] if max(l)==1 and max(g)==0)
    solv = sum(1 for g,l in r["per_q"] if max(l)==1)
    print(f"\n  queries solved by SOME chunk            : {solv}/{n}")
    print(f"  ...of which NO chunk defines a gold symbol: {both} ({both/max(1,solv):.1%})")
    print(f"  -> the model answers correctly from code that does not contain the answer")
    print(f"\n{'='*74}\nVERDICT\n{'='*74}")
    if (p_hit_gold - p_hit_nogold) > 0.15:
        print("  WORLD A -- gold presence strongly predicts utility. The signal IS in the")
        print("  content. Build a better ENCODER; execution traces are not the bottleneck.")
    else:
        print("  WORLD B -- gold presence barely predicts utility. Having the right code in")
        print("  context does NOT determine whether the model answers. This CAPS every")
        print("  retrieval improvement and means a new information source is required.")
