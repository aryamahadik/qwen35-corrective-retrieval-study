# Qwen3.5-9B vs frontier: what is actually achievable on $40

Status: **research memo, nothing executed, no GPU booked.**
Date: 2026-09-18. Every number below is either (a) computed from files in this
repo, or (b) carries a primary-source URL. Anything I could not establish is
labelled NOT FOUND / NOT MEASURED / INCONCLUSIVE.

---

## 0. The short answer

**The goal as stated — "beat GPT-5-mini *and* Claude Sonnet 4.6 on a specific
benchmark" — cannot be achieved, because the premise is false.**

GPT-5-mini and Claude Sonnet 4.6 are ~6 months apart (2025-08-07 vs 2026-02-17)
and are essentially **never co-evaluated on the same harness**. An exhaustive
inverted search (start from the models, enumerate every benchmark carrying both)
found exactly **two** publishers worldwide who score both: Artificial Analysis,
and Nanonets' IDP Leaderboard. Both are single-source, and each candidate fails
at least one other requirement. GPT-5-mini appears **zero times** in the
HTMLBench papers, the BFCL v4 Sonnet-4.6 row does not exist, LMArena has Sonnet
4.6 but not GPT-5-mini, Vals AI has Sonnet 4.6 but GPT-5-mini's page 404s,
HAL has neither, and Anthropic's own Sonnet 4.6 system card benchmarks against
GPT-5.2 and Gemini 3 Pro — GPT-5-mini is not in it.

Also worth knowing: as of today **both targets are legacy**. Artificial Analysis
marks GPT-5-mini "deprecated — we only continue benchmarking the default 10k
workload", and Anthropic's current lineup is Fable 5.1 / Opus 5 / Sonnet 5 /
Haiku 4.5. Beating them is a smaller claim in Sept 2026 than it was in Feb.

**But you are much closer to a real result than you think, on a different
claim.** The benchmark you already have vendored has a fully published ladder
where *your exact base model* is the subject.

---

## 1. The verified ladder (this is the good news)

HTMLBench-400, n = 400 items / 6,000 frozen weighted test cases.
Sources: arXiv:2608.30530 Table 1 (WebWorld) and arXiv:2605.26807 Table 4
(HTMLCure). Every row below was independently re-verified by fetching the raw
arXiv HTML and parsing the table cells — summarizers demonstrably mis-map these
columns, so snippet reads were rejected.

| Model | Size | Total /100 | TC pass % | Rend /10 | Visual /20 | Func /55 | Inter /10 | Code /5 |
|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B **(your base)** | 9B | **42.9** | 35.1 | 8.9 | 9.1 | 19.9 | 0.9 | 4.0 |
| WebWorld-9B-Raw (control) | 9B | 44.5 | 34.1 | 9.5 | 9.1 | 20.3 | 0.7 | 4.9 |
| Qwen3.5-27B | 27B | 45.5 | 38.4 | | | | | |
| Gemini-3.1-Pro | — | 45.4 | 37.0 | | | | | |
| **Claude-Sonnet-4.6** | — | **46.6** | 37.2 | 9.4 | 11.1 | 21.1 | 1.0 | 3.9 |
| WebWorld-4B | 4B | 46.7 | 39.3 | | | | | |
| Qwen3.6-27B | 27B | 47.1 | | | | | | |
| Claude-Opus-4.6 / 4.7 | — | 47.5 / 47.8 | 39.3 / 39.8 | | | | | |
| HTMLCure-9B-Refined | 9B | 48.5 | 42.1 | 9.2 | 10.2 | 23.9 | 1.1 | 4.1 |
| DeepSeek-V3.2 | 685B-A37B | 48.8 | | | | | | |
| GPT-5.4 | — | 49.2 | 42.7 | 8.8 | 11.0 | 24.2 | 1.0 | 4.2 |
| **WebWorld-9B** | 9B | **49.3** | 40.6 | 9.5 | 8.0 | 26.1 | 0.6 | 5.1 |
| Kimi-K2.6 | 1T-A32B | 49.8 | 43.7 | | | | | |
| HTMLCure-27B-Refined | 27B | 50.6 | 45.2 | 9.1 | 10.7 | 25.6 | 1.1 | 4.3 |
| WebWorld-27B | 27B | **52.7** | 43.2 | 9.5 | 8.9 | 28.0 | 0.6 | 5.7 |

**GPT-5-mini: NOT FOUND.** Zero occurrences in either paper.

So a fine-tuned Qwen3.5-9B beating Claude Sonnet 4.6 on HTMLBench is not
speculative — it is *published*. That is the encouraging part.

### What it cost them

Verified from arXiv:2608.30530: **full-parameter** SFT (no LoRA), 32,800
certified transitions, 3 epochs, seq 16,384, effective batch 128, LR 2e-5,
**64 × H100 ≈ 384 H100-card-hours**. Your budget is ~13 A100-hours.
That is a **~60× compute gap** before accounting for A100-vs-H100.

---

## 2. Why the obvious plan fails — the arithmetic

### 2a. The dominant lever is quality, and it was deliberately withheld

The paper's own Table 4, at a **fixed 5,000 examples**, HTMLBench total by
minimum certified depth:

| min depth | ≥1 | ≥2 | ≥3 | ≥5 | ≥8 |
|---|---|---|---|---|---|
| Total /100 | 43.4 | 45.2 | 46.8 | **48.8** | 48.5 |

Read that carefully:

- **5,000 uniform-certified rows → 43.4.** Base is 42.9. The gain is **+0.5**.
- **5,000 depth≥5 rows → 48.8.** The gain is **+5.9**.
- Depth filtering is worth **+5.4 points at identical data budget** — more than
  the entire 5k→32.8k data-quantity effect (+5.9 over a 6.6× increase).

**The public WebWorld-SFT-10k release is exactly the 43.4 composition:** uniform
random over the certified pool, seed 20260901. Verified locally from
`webworld_clean_sft_v1/data/raw/upstream_MANIFEST.json`.

And the depth signal is **not recoverable**. I parsed the raw 400 MB file: every
row has exactly **one** top-level key, `conversations`, holding exactly two turns
keyed `{from, value}`. No id, no seed, no depth, no score, no certificate. The
MANIFEST lists `depth_ge1/2/3/5/8_equal5k` and "internal trajectory records with
certificate metadata" under **`not_released`**. They withheld precisely the thing
that produces the result.

### 2b. Format mismatch — you would not be reproducing the method

The paper's training unit is the 6-tuple transition `(q, o_t, c_t, r_t, x_{t+1},
e_t)` — prompt, observation, critique, contract, repaired HTML, certificate. The
public rows are the 2-tuple `(q, x_final)`. The matched-budget raw-HTML control
(`WebWorld-9B-Raw`) scores **44.5**, and on the deterministic TC pass rate it
scores **34.1 — below the 35.1 base**.

### 2c. Most published configurations of this recipe make the model *worse*

TC pass %, 9B: base **35.1**. Published ablations at 20k rows: no-certificate
31.0, no-preserve 31.9, VLM-only 33.4, score-gate 34.0. **Four of five are below
base.** Only the full certificate rule at 32,800 rows reaches 40.6. Even
depth≥5 at 5k reaches only 36.1 — still short of Sonnet's 37.2.

### 2d. Your corpus, measured

Computed by joining `static_rows.jsonl` × render shards × contamination
decisions × duplicate groups:

| gate | rows |
|---|---|
| upstream | 10,000 |
| − static quarantine | −1,092 |
| − render FAIL | −50 |
| − benchmark leak (LEAK_VARIANT) | −112 |
| − never rendered (**shard 1 of 4 is incomplete**) | −219 |
| − duplicate-group collapse | −108 |
| **surviving** | **8,419** (87.9 M tokens, mean 10,441) |
| of which ≤16,384 tok | 7,311 (66.6 M) |
| of which **English** and ≤16,384 tok | **3,871** (36.4 M, mean 9,408) |

Note: **3,871 English rows is below the paper's 5,000-example anchor that scored
43.4.** Train Chinese too and 44.6 % of your gradient serves a split you are not
evaluating.

### 2e. Projection

Log-linear fit through the paper's own two depth≥1 points (5,000→43.4,
32,800→49.3; slope 3.14 pts per ln-unit):

| your N (uniform certified) | projected total |
|---|---|
| 3,871 (EN only) | **42.6** |
| 8,419 (all languages) | **45.0** |
| needed to pass Sonnet 4.6 | **46.6** |

And that fit is the *optimistic* attribution — it credits the entire +5.9 to
size, when the two endpoints also differ in depth composition, contamination and
recipe. Correcting for LoRA-instead-of-full-FT, <1 epoch instead of 3, flattened
pairs instead of trajectories, and decontamination, the honest central estimate
is **42.5 – 44.5: a wash with the base model, with real downside risk.**

### 2f. You cannot measure the dimension where the gap lives

Decompose Sonnet 4.6's +3.7 lead over base Qwen3.5-9B:

| dimension | base | Sonnet 4.6 | gap |
|---|---|---|---|
| visual_design /20 (**VLM-judged**) | 9.1 | 11.1 | **+2.0 (54 % of the gap)** |
| functionality /55 (deterministic) | 19.9 | 21.1 | +1.2 |
| rendering /10 | 8.9 | 9.4 | +0.5 |
| interaction /10 | 0.9 | 1.0 | +0.1 |
| code_quality /5 | 4.0 | 3.9 | −0.1 |

**The judge VLM is never named** — not in either paper, not in any config
(`evaluator.model` is the placeholder `${HTMLEVAL_MODEL}`). So 46.6 is not
reproducible at all. And `fast` mode is *not* the deterministic 80: with
`vlm_scores={}` the shipped `composite_score` hardcodes visual_design to 8/25 →
a flat 6/20, capping a perfect page at 86/100. **A fast-mode total printed next
to 46.6 is a category error.**

Meanwhile, look at where WebWorld's +6.4 actually landed: functionality
19.9→26.1, code 4.0→5.1, rendering 8.9→9.5 — and **visual_design fell 9.1→8.0**.

> SFT on this data buys exactly the dimension you can measure for free, and
> costs you the dimension the frontier model wins on.

---

## 3. Two real findings already sitting in this repo (free, CPU-only)

Both independently verified by me against the vendored files.

### 3a. HTMLBench's frozen scoring pool is not model-blind

`benchmark/tc_selection_20260430_6000.json` carries
`target_sft_model: "qwen3.5-27b-html-sft-128card-0414_final_correct"` and
per-test-case pass rates for the SFT / non-SFT / target model groups. The shipped
`benchmark/en` test cases are **set-identical** to that frozen pool (I checked:
6,000 ∩ 6,000, zero symmetric difference).

`scripts/analysis/rescore_drop_cov_tc_rend_0430.py` shows how it was built:

- `is_sft_unfavorable()` **deletes** discriminative test cases where non-SFT
  models beat SFT models by ≥25 pp and the target SFT model fails.
- `sft_contrast_keep_reason()` **adds** cases specifically because SFT models
  pass more often.
- `hard_anchor_sort_key()` prefers hard anchors "less adverse to SFT".

Keep-reason composition by scored weight: normal_discriminative 40.7 %,
hard_anchor 36.5 %, easy_anchor 13.3 %, **pro-SFT contrast buckets 9.47 %**.

Measured consequence:

| pool | SFT group | non-SFT group | gap |
|---|---|---|---|
| full frozen 6,000 | 0.4160 | 0.3938 | **+2.22 pp** |
| minus the 591 pro-SFT cases (9.47 % of weight) | 0.4052 | 0.4086 | **−0.34 pp** |

**The entire class-level SFT advantage on this benchmark is manufactured by the
test-case selection.** Neither paper discloses this. The repo has 0 stars, 0
forks, 0 issues and 2 citations, both from the same authors — nobody has checked.

Two more structural facts from the same file: 36.5 % of the functionality budget
is `hard_anchor` cases where the target model passed **zero** (1,961 of 2,151
have a pool-wide pass rate of exactly 0.0), and 13.3 % is `easy_anchor` where
everyone scores ~1.0. Only ~40 % of the 55-point functionality budget is live.

### 3b. 27.7 % of the "deterministic" score is a pixel diff

`assert_screenshot_changed` appears 1,662 times across 1,628 test cases —
**27.1 % of count, 27.7 % of scored weight, touching 372 of 400 items** — on
animated/timed pages. Run-to-run variance is never reported in either paper;
`--seed` defaults to 0 (disabled) and browser/probe timing is unseeded. **Nobody
has ever published HTMLBench's test–retest reliability.** You can measure it for
$0 on your Mac by running the evaluator three times over identical response
files.

### 3c. The dataset contradicts its own paper

`upstream_MANIFEST.json` (local, verified): the 32,800-row training corpus
contained **2,000 HTMLBench-seeded + 800 MiniAppBench-seeded rows** (8.54 %),
removed only before the public 10k sample. arXiv:2608.30530 Appendix A.1 asserts
"No HTMLBench-400 item ID, prompt string, rendered DOM, or screenshot enters the
data-construction pipeline… the intersection is empty." **One of the two is
wrong.** Every published number in the table above is a contaminated-regime
number; no decontaminated retrain exists, so the effect is UNQUANTIFIED.

---

## 4. Budget and runtime reality

### Throughput is NOT MEASURED — this is the biggest unknown

There is **no published tokens/sec for LoRA SFT of any 8–10B model on a single
A100-80GB at 8k–16k**, and none at all for Qwen3.5-9B on any GPU. Estimates:

- FLOPs model (6N + hybrid attention; only 8 of 32 layers are full attention, so
  8k→32k costs ~+14 % FLOPs/token): 312 TFLOPS × 35–45 % MFU → **1,850–2,800 tok/s**.
- Pessimistic anchor derived from the paper's own 64×H100 full-FT run: ~740 tok/s
  per H100 — but that is distributed full-parameter training, not single-GPU LoRA.

**3–4× uncertainty, and it decides whether anything fits.** Measure it first.

| plan (EN ≤16k, 3,871 rows, 36.4 M tok) | @800 t/s | @1,200 t/s | @2,000 t/s | @2,400 t/s |
|---|---|---|---|---|
| 1 epoch | $35.6 | $23.7 | $14.2 | $11.9 |
| 2 epochs | $71.2 | $47.5 | $28.5 | $23.7 |

Modal, verified from `config/modal.json` and modal.com/pricing:
A100-80GB $2.4984/h GPU-only, **$2.8149/h all-in** with 4 cores + 16 GiB.
H100 SXM $3.95/h — ~1.9–2.2× the throughput at 1.58× the price, so **H100 is
~1.2–1.4× better $/token for training.** RunPod Community A100 is $1.19–1.39/h
(≈2× the hours) but you would port the Modal-volume checkpoint code and take
preemption risk; only worth it if you commit to multi-epoch runs.

One more thing to check: Modal Starter reportedly includes **$30/month free
compute**. If that applies to your workspace your real budget may be ~$65, not
$34. Confirm before planning.

### Runtime landmines (all verified, all cheap to hit)

1. **`fla` + `causal_conv1d` are mandatory, not optional.** Unsloth PR #10280
   measures **877 tok/s with them, 418 without** (2.1×), and peak memory
   14.02 → 17.08 GiB. Unsloth's own `check_fast_path()` is "advisory and cannot
   break a load" — it degrades **silently**.
   **CORRECTION (2026-09-19):** that 877/418 measurement was taken on a DGX Spark
   GB10 (sm_121a) at seq 512, **not an A100** — it bounds the penalty ratio, not
   the absolute speed. Worse: **FlashQLA**, the fast Gated-DeltaNet kernel Qwen
   ships and `fla` adopted in 2026-07, declares support for **SM90/SM100/SM103/
   SM120/SM121 only — Ampere (sm80) is not supported**, and vLLM's own Qwen3.6-27B
   recipe page lists H100/H200/L40S/B200/GB10/GB300 and **no A100**. So on an A100
   you get `fla`'s Triton GDN path: slower than FlashQLA, but not the 418 tok/s
   pure-PyTorch floor. Absolute A100 throughput remains NOT MEASURED.
2. **Sequence packing silently corrupts the model** — *already disarmed in this
   repo:* `config/training.json` sets `"packing": false`, and with
   `per_device_train_batch_size: 1` there is no padding waste to recover, so
   keeping it off costs ~0. Note that HTMLCure's own appendix says **they trained
   with packing at seq 32,768 on Qwen3.5** — i.e. the published numbers came off
   the path that issue #46851 says miscomputes. That is a reason to distrust their
   recipe, not to copy it. Detail: `transformers` Qwen3_5 only
   honours an explicit `cu_seq_lens_q`; the pure-PyTorch
   `torch_chunk_gated_delta_rule` ignores `cu_seqlens` entirely, so GatedDeltaNet
   recurrent state leaks across document boundaries with no error. Issue #46851
   is open; the fix PR #46859 was **closed unmerged**. → **Disable packing** unless
   you can prove the fast path is active.
3. **Fused cross-entropy is a hard requirement.** vocab 248,320 untied × 16,384
   seq = **7.58 GiB** of bf16 logits before the fp32 upcast and gradient. Liger
   FLCE covers this class (PR #1123, #1150) but convergence was tested on H200 only.
4. **The released 9B is `Qwen3_5ForConditionalGeneration`** — a VLM with a
   27-layer vision tower, not a text-only causal LM. Code written against
   `AutoModelForCausalLM` will not do what you expect.
5. `head_dim=256` falls outside the flash-attention fast paths (Unsloth #11102,
   open) — the 8 full-attention layers drop to SDPA.
6. **vLLM on A100/sm80 runs the least-exercised GDN backend.** FlashInfer and
   CuteDSL are gated to SM90/SM10x/SM12x; sm80 falls through to Triton with no
   raise. Do **not** enable MTP self-speculation (`mtp_num_hidden_layers: 1`) —
   vLLM #34948 (CUDA illegal memory access in the GDN kernel) is still open.
   The LoRA `expand_packed_lora` crash is #47639, **fixed** by #47640 (2026-08-19).
7. ~~89.2 % of training targets load external CDN assets — inline them~~
   **RETRACTED 2026-09-19. Do not inline.** Two independent reasons:
   (a) HTMLBench's own docs state external resources "are not penalized by
   themselves. They only matter if they cause real rendering or runtime
   failures", so CDN use costs nothing on the metric; and
   (b) I measured the cost of inlining against the manifest — the corpus goes
   from **92.6 M to 1,182 M tokens (12.8×)**, mean row 10,391 → 132,724, rows
   fitting 16 k collapse from 7,760 to 2,648, and the worst single row gains
   **1.9 M tokens** from a 5.9 MB library. It would also teach the model to emit
   megabyte-long inlined bundles.
   Hermetic rendering is already handled without touching the HTML: the render
   runs under `network_policy = exact_url_content_addressed_cache_then_abort_unknown`,
   which serves every dependency from `audit/cache/` and blocks anything unknown.
8. `config/modal.json` records `cloud_runtime_tested: false`, `runs/` and
   `checkpoints/` are empty. Nothing in this stack has ever touched a GPU.

### 4a. Render-harness defect found and fixed (2026-09-19)

`scripts/render_audit.py` aborted the whole shard whenever the **browser
process** died, because the recovery path at the old line 480 —
`context, page = await new_context_page()` inside an `except asyncio.TimeoutError`
block — was unguarded. A dead browser turned a per-row fault into a shard-wide
abort. This is the direct cause of the 219 unrendered rows: shard 1 stopped at
the contiguous tail (source_index 9069 onward), and those rows are *smaller*
than average (p50 27.9 k chars vs 32.7 k, max 4 deps vs 14), so it was browser
exhaustion, not a pathological input.

Second defect: on abort no summary was written, but the rows file remained and
looked plausible, so `merge_render_audits.py` proceeded with 8,689 of 8,908 rows
with nothing marking the gap — a missing measurement recorded as nothing (§87).
Third: `processed` reset to 0 on resume with a 100-row flush, so a crash could
discard up to 99 completed renders.

Fix (157 lines, backup at `scripts/render_audit.py.pre-fix-bak`):
`ensure_browser()` relaunches a dead browser under a lock and aborts loudly if
the version changes mid-run; `recover_context()` returns `None` instead of
raising, so an unrecoverable row becomes `FAIL_BROWSER_UNAVAILABLE` and the run
continues; context rebuilding moved to the top of the loop where it is guarded;
flush every 25 rows; and the summary now carries `completeness`, `expected_rows`,
`missing_rows`, `aborted` and `browser_relaunches`, returning exit code 1 on
anything short of COMPLETE.

Note the fix changes `render_script_sha256`, hence `run_fingerprint`, so the
existing 8,689 rows cannot be resumed against — one clean full pass is required.
That was already necessary and is the right outcome.

### 4b. Phase 1 executed — dataset is ready (2026-09-19)

Render moved to Modal CPU (`webworld_clean_sft_v1/modal_render.py`, 24 containers,
no GPU). Result: **8,908 / 8,908 rows rendered, 24/24 shards COMPLETE, one shared
`run_fingerprint`, zero duplicates, zero uncovered.** 11 failures (0.12 %) against
50 on the partial macOS run — watchdog timeouts fell from 38 to 3, because a
dedicated container is not competing with a desktop. One container was preempted
mid-run and restarted; the coverage gate proved it cost nothing.

`finalize_release.py` initially refused with "render evidence browser binary
identity is stale": it re-hashes the browser named in the evidence, which assumes
render and finalize share a machine. With a distributed render that check is
*impossible*, not failing. Rather than delete it, a second branch was added —
`modal_render.py::attest` re-opens the same content-addressed image
(`im-768V2R7uzquRnQ7QW8VTSn`) and re-hashes its own browser; finalize accepts that
only when it matches the evidence on executable path, sha256 and version, records
`browser_verification.mode = "REMOTE_IMAGE_ATTESTED"` in the manifest, and appends
an explicit limitation saying the binary was not re-hashed on this host. A local
render still takes the stronger `LOCAL_REHASH` path unchanged.

`verify_release.py` → **PASS, 0 critical findings, token counts replayed.**

| payload | rows | tokens |
|---|---:|---:|
| `train_16k.jsonl` | **6,271** | **56.2 M** (3,337 en / 2,930 zh) |
| `train_32k_addendum.jsonl` | 756 | — |
| `train_offline_16k.jsonl` | 697 | 4.6 M |
| `validation_16k.jsonl` | 695 | — |
| admitted / source | 7,808 / 10,000 | |

Top quarantine reasons: unresolved_outbound_request 819, render_pass_with_blocked_requests
796, remote_media_license_unverified 564, embedded_verifier_marker 551, benchmark_leak 137.

Qwen3.5-4B training cost on `train_16k` (2,700–5,400 tok/s assumed, $2.8149/h all-in):

| slice | ×1 | ×2 | ×3 |
|---|---|---|---|
| all languages, 56.2 M tok | $8–16 | $16–33 | $24–49 |
| **English only, 30.9 M tok** | $4–9 | **$9–18** | **$13–27** |

So on the 4B the paper's actual 3-epoch recipe is reachable on English-only —
which it never was on the 9B.

### 4c. Phase 2 step 1 — throughput MEASURED (2026-09-19)

No published tokens/sec exists for Qwen3.5 training on any GPU. These are ours,
Qwen3.5-4B, LoRA on 248 matrices, bf16, gradient checkpointing on, real rows
(mean 9,374 tokens, range 1,967-16,201), Modal A100-80GB at $2.8149/h all-in.

| config | rank | batch | bucketed | tok/s | peak GiB | pad waste |
|---|---|---|---|---|---|---|
| baseline, UNFUSED loss | 256 | 1 | - | 943.6 | 68.73 | 0 % |
| H100, same config | 256 | 1 | - | 1,220.9 | 68.78 | 0 % |
| fused loss | 256 | 1 | no | 566 | 19.1 | 0 % |
| fused loss | 256 | 4 | no | 598 | 42.6 | 31 % |
| fused loss | 256 | 8 | no | 727 | 71.5 | 37 % |
| **fused loss** | **256** | **8** | **yes** | **1,133** | **41.3** | **2 %** |
| fused loss | 64 | 8 | yes | 1,024 | 36.6 | 2 % |
| fused loss | 64 | 16 | yes | OOM | | |

Four defects found, each of which would have wasted a paid run:

1. **CUDA mismatch.** PyPI `torch==2.10.0` is built against CUDA 13.0; the repo's
   base image is 12.8 and `causal-conv1d` compiles CUDA extensions. Fixed by
   installing torch from the cu128 index, which is what `config/training.json`
   pinned all along (`torch 2.10.0+cu128`).
2. **PEP 517 build isolation.** pip built `causal-conv1d` against its own torch
   pulled fresh from PyPI, ignoring the installed cu128 build. `--no-build-isolation`
   is load-bearing here, not a convenience.
3. **Triton miscompiles on Hopper.** torch 2.10 pins `triton==3.6.0`; `fla` refuses
   to run it on Hopper because ">= 3.4.0 and < 3.7.1 produces incorrect results for
   gated chunk_bwd_dqkwg". It raises rather than silently returning wrong gradients.
   Pinned `triton==3.7.1`.
4. **Liger never applied anything.** `apply_liger_kernel_to_qwen3_5` is
   all-or-nothing and patches rope first; there is no Qwen3_5 rope kernel, so the
   call raised `NotImplementedError: liger_rotary_pos_emb is not available for
   Qwen3_5 models` and rms_norm, swiglu and fused_linear_cross_entropy were never
   reached. The 943.6 baseline therefore ran with HuggingFace's stock loss
   materialising 9,200 x 248,320 logits and upcasting them to fp32 — 21+ GiB of
   its 68.73 GiB peak. Applying each component separately with `rope=False` fixes
   all four and drops peak memory to 19.1 GiB.

Two findings that were not expected:

- **Fused cross-entropy costs ~40 % throughput at batch 1** (943.6 -> 566) in
  exchange for ~50 GiB. It only pays for itself because the freed memory permits
  bucketed batching.
- **Padding, not batch size, was the bottleneck.** Naive batching pads every row to
  the batch maximum; at batch 8 that wasted 37 % of every step. Length-bucketing at
  the same batch size gave **+56 % throughput and -42 % memory simultaneously**
  (727 -> 1,133 tok/s, 71.5 -> 41.3 GiB). Batch size alone moved 566 -> 727 across
  an 8x increase.
- **H100 is worse value.** 1,220.9 vs 943.6 tok/s is 1.29x for 1.52x the price:
  $0.972 vs $0.827 per M tokens. Its MFU was *lower* (3 % vs 7 %).
- **Lower rank did not help.** r=64 ran slower than r=256 (1,024 vs 1,133) and its
  memory saving did not buy a larger batch, because bucketed batches of the longest
  rows (16 x ~16k tokens) OOM regardless. Batching must be token-budgeted, not
  row-counted.

Best measured: **1,133 tok/s = $0.690 per M tokens.** One epoch on the 30.9 M-token
English split therefore costs **$21.32**. The hard floor for affordability was
1,421 tok/s and the comfortable target 1,600; we reached 1.20x of baseline where
1.7x was needed.

### Base-model choice: stay, with a numeric fallback

Surveyed 2026-09-19. **There is no better small model.** Qwen ships exactly four
Qwen3.6 repos (27B, 35B-A3B) and Qwen3.8 also bottoms out at 27B — the smallest
dense Qwen in any of the three generations is Qwen3.5-9B/4B. Every "Qwen3.6-9B"
on HuggingFace is a community 16-layer prune of a 27B merge that self-labels
"do not rely on this model". And Qwen3.6-27B's own config declares
`architectures: ["Qwen3_5ForConditionalGeneration"]` — same class, same 3:1 GDN
hybrid, same head_dim 256, same 248,320 vocab. **Zero landmine relief.**

**No model ≤15B other than Qwen3.5-4B and Qwen3.5-9B has any published
HTMLBench-400 score.** Switching trades a measured anchor for an unmeasured one.
Non-Qwen options considered and rejected: `gemma-4-12B-it` (Apache-2.0, softmax
attention so packing is safe — but head_dim still 256 and vocab 262,144 gives
**8.00 GiB** of logits, worse than Qwen's 7.58); `granite-4.2-8b` (perfect plain
architecture, best algorithmic coding in the sweep — but granite-4.1-8b ranks
**124th of 128** on WebDev Arena, so algorithmic coding does not transfer to
frontend); `Qwen3-8B` (clean architecture, but a 2025-04 pretrain and no anchor);
`Tesslate/OmniCoder-9B` (a real Qwen3.5-9B LoRA SFT, but zero HTML/UI evals and
the MTP head stripped — 9,409,813,744 params vs 9,653,100,528).

**Break-even: 1,473 tok/s.** $26.45 of GPU budget = 9.40 A100-h; two 400-item
arms ≈ 2.0 h and the probe ≈ 0.5 h, leaving 6.86 h for 36.4 M tokens. The FLOPs
model predicts 1,850–2,800 tok/s, so it probably fits.

**Pre-registered fallback rule:** if the probe measures **< 1,473 tok/s, fall
back to Qwen3.5-4B — do not cut the corpus.** The 4B keeps a published anchor
(41.7 / **35.4 TC — higher than the 9B's 35.1**), keeps the data–model match,
costs 2.25× less per token, and its fine-tuned ceiling (WebWorld-4B, 46.7 /
**39.3 TC**) still clears Sonnet 4.6. The risk is fragility: the 4B's raw-SFT
control collapsed **35.4 → 26.8 TC (−8.6)** where the 9B's only fell −1.0.

### Statistical power

n = 400. For a 0–100 per-item score with SD ≈ 24:

- Unpaired vs a published constant: SE = 1.20 → you need an observed
  **≥ 48.9** to clear 46.6 at p<0.05. Honouring the published number's own SE:
  **≥ 49.9** — at or above WebWorld-9B's contaminated 49.3.
- **Paired** (both arms through your harness, ρ≈0.6): SE_diff ≈ 1.07, so a
  **+2.5** delta is detectable.
- On the item-level TC pass rate, n=400 paired gives SE ≈ 0.75 pp,
  MDE ≈ 2.1 pp at 80 % power.
- McNemar, discordant pairs: n=30 needs a 21/9 split; n=100 needs 61/39.

**The unpaired comparison against a published number is not winnable. A paired
comparison is.**

---

## 5. What I recommend

Stop chasing the frontier total. Ship the three things that are actually yours.
Expected total spend **≈ $22–30**, with eval free on your Mac.

**Claim 1 — the paired delta (headline).** Base vs LoRA Qwen3.5-9B, all 400 EN
items, one vLLM session with `--enable-lora`, identical seeds/decoding/prompt,
same pinned Chromium. Metric = **weighted TC pass rate** — no VLM anywhere in it.
Report on the full frozen pool *and* on the bias-stripped pool (minus the 591
pro-SFT cases). Clustered bootstrap over items primary, McNemar secondary.

**Claim 2 — the benchmark audit (lands regardless of the model result).** §3a and
§3b above. The selection-bias number is already computed; the reliability run is
CPU-only and free. No published paper has done either.

**Claim 3 — the frontier check, honestly scoped (optional).** Pre-registered
150-item stratified subsample via the Batch API: Sonnet 4.6 ≈ $11, GPT-5-mini
≈ $1.50. Say "150 of 400" in every sentence that quotes it. Do **not**
pre-commit to winning. (All 400 items through Sonnet 4.6 costs **$60 standard /
$30 batched** — 1.8× your whole budget — because responses are whole HTML
documents at ~9k tokens each.)

### Order of operations

1. **Free, today:** `scripts/render_audit.py` has been patched (see
   §4a below) — re-render all 8,908 rows in one clean pass, then
   `finalize_release.py` + `verify_release.py`. Every cost estimate depends on
   the true counts. Drop — do not truncate — the 1,108 rows over 16k; training
   on documents with no `</html>` is actively harmful on a render-scored
   benchmark. **Do not inline the CDN dependencies** (see landmine 7).
2. **Free, today:** run the evaluator 3× over identical response files and
   publish the test–retest SD. This is Claim 2 and it costs nothing.
3. **~$1.50:** validate imports on CPU, then one ~20-minute A10G/L4 run that
   hard-asserts 248 target matrices, confirms `fla`/`causal_conv1d` are on the
   fast path, completes 10 steps with decreasing loss, and — most important —
   **measures tokens/sec**. Do not debug at $3.95/h.
4. **Pre-register in a git commit** before generating anything: metric, primary
   subset, language mix, test, subsample size, stopping rule.
5. **~$2–3 — GENERATE THE BASE ARM FIRST, AND GATE ON IT.** Before spending a
   training dollar, generate and score all 400 EN items with the *unmodified*
   Qwen3.5-9B. Pre-register a clustered-bootstrap acceptance band around the
   published 42.9 total / 35.1 TC pass in a git commit **before looking**. If your
   base arm lands outside it, your harness disagrees with the paper's and a paired
   delta computed on it is worthless — stop and fix the harness. This is the only
   external check that your evaluator is correct, and 27.7 % of the scored weight
   is unseeded pixel-diff, so it matters more here than usual.
6. **~$10–14:** train. EN-only, ≤16k, 3,871 rows, 1 epoch, LoRA rank 256
   all-linear at 10× the full-FT LR (2e-4 vs 2e-5 — the rank-32 config currently
   in `config/training.json` is under-powered for SFT), packing **off**, fused CE on.
7. **~$2–3:** generate the tuned arm, same session, same settings.
8. **Optional $12.50:** the 150-item frontier subsample.

### Calibrated probabilities

| claim | P(success) |
|---|---|
| beat Sonnet 4.6 on the 100-pt total, defensibly | **~5 %** |
| beat Sonnet 4.6 on deterministic TC pass %, paired and defensible | **~15–20 %** |
| positive, significant **base → tuned** paired delta | **~60 %** |
| ship something true, novel and worth posting | **~70 %** |

### Hard rules

- Never print a `fast`-mode total beside 42.9 / 46.6 / 49.3.
- Best-of-n is legitimate **only** if the selector never reads
  `score.test_pass_rate`. `metrics.py` ships `pass_at_k()` and `is_pass()` that
  read exactly that — using them is selecting on the answer key. Restrict the
  selector to `render_data` page-health signals. Publish token- and
  dollar-matched curves; never show bo-n against n=1 unlabelled.
- Do **not** distill from GPT-5-mini or Claude outputs. OpenAI Business Terms and
  Anthropic Commercial Terms D.4 both bar using Output to train competing models.
  Publishing a *comparison* is fine; both providers' terms contain no restriction
  on that. WebWorld-SFT-10k is Apache-2.0 and is clean for this purpose.
- A null result must be publishable as-is. If the plan only works when the LoRA
  wins, it is the plan I just talked you out of, wearing a disguise.

---

## 6. Paths considered and rejected

- **olmOCR-Bench.** The one candidate with both target models. **Rejected.** The
  numbers (GPT-5-mini 69.9, Sonnet 4.6 73.9, Qwen3.5-9B 77.2) are real but come
  from Nanonets' IDP Leaderboard, **not** AI2's official board — which contains
  none of those three models. The "85.9 top score" is a column mis-read (it is
  Nanonets OCR-3's three-benchmark composite; its olmOCR score is 87.4). The
  leaderboard operator also ships the #1 model, and its Overall arithmetic does
  not close. Fatally: **the base model already beats both**, so the fine-tune has
  a null counterfactual; and on the same operator's composite Sonnet 4.6 (80.7)
  **beats** Qwen3.5-9B (76.7). Training cost is 4–45× the budget, olmOCR's own
  paper found LoRA worse than full FT on this exact data, and the only real
  headroom (Old Scans) needs the vision tower, which the LoRA config does not
  target. Adversarial P(success): **2 %**.
- **EnterpriseOps-Gym.** Already dead here: `qwen35-harness-v21-pilot-v1/summary.json`
  shows base 0/8 and adapter 0/8 verifier checks on n=1, McNemar p=1.0. No public
  trajectory corpus exists — only task specifications. Needs a live multi-service
  environment for both collection *and* evaluation. **Abandon.**
- **MiniAppBench.** 400 of 500 test rows have `reference: ""` (verified in your
  own lockbox); only 100 validation items are self-scorable. The judge is an
  agentic Gemini-3-Pro + Playwright harness — expensive and stochastic. No
  GPT-5-mini, no Sonnet 4.6 on its leaderboard. GitHub has no LICENSE file.
- **IFBench** (n=300, AA: GPT-5-mini 75.44 vs Sonnet 4.6 41.16). Both models
  present, train set `allenai/IF_multi_constraints_upto5` is 95k rows ODC-BY.
  But n=300 gives ±2.9 pp binomial SE, and AA's Sonnet row is the
  *non-reasoning* variant — the 34-point gap may vanish with thinking enabled.
- **SWE-bench / BFCL / BIRD / Spider 2.0 / DABstep / MMTU / KernelBench /
  miniF2F.** All fail on the co-published-baseline requirement, or are saturated,
  or need infrastructure far beyond the budget. SWE-bench additionally restricts
  submissions to academic institutions since 2025-11-18.
- **Waiting for a WebWorld checkpoint.** None exists. `Qwen/WebWorld-8B/14B/32B`
  is a **name collision** — a different org, different sizes, dated six months
  before the paper. Evaluating those would attribute numbers falsely.

---

## 7. Open questions I could not resolve

- **Tokens/sec for this architecture on A100.** NOT MEASURED, anywhere, by
  anyone. Every published figure is B200, H200, DGX Spark or MI355X. 3–4× spread.
  Resolve with the $1.50 probe before committing anything.
- **How much of WebWorld-9B's 49.3 is the 8.54 % benchmark-seeded rows.**
  UNQUANTIFIED. The `raw_equal32800` baseline and every ablation are
  `not_released`, and no decontaminated retrain exists. Any number here would be
  invented.
- **The identity of the visual_design judge VLM.** NOT FOUND. Makes 46.6
  unreproducible by anyone.
- **HTMLBench run-to-run variance.** NOT MEASURED by the authors. You can be the
  first — for free.
- **Whether a render/richness-based quality filter recovers any of the depth
  signal.** UNVALIDATED and unvalidatable: there is no depth label in any public
  artifact to check a proxy against. A residualised richness score does separate
  the corpus cleanly (at matched HTML length, the top tercile has 2.3× the event
  listeners, 10× the ARIA attributes, 5× the localStorage use), but whether that
  correlates with certificate depth is a **hypothesis, not a measurement.**
- **Your actual remaining budget**, and whether Modal Starter's $30/month credit
  applies. `qwen35-corrective-collection-v1/budget_reservations.jsonl` shows
  $4.20 reserved of the $10 API bucket; `qwen35-harness-v21-budget-reservations.jsonl`
  shows $1.25 GPU. I assumed ~$34 remains.
