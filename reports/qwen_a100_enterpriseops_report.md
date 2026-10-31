# Qwen3.5 Fine-Tuning for EnterpriseOps on One A100

**Recommendation.** Choose **Qwen3.5-9B, BF16 LoRA, rank 32, all 32 language blocks, microbatch 1, and an initial maximum training sequence of 16,384 tokens**. Keep Qwen3.5-4B as a short baseline and fallback. Test 32,768 tokens after the 16K implementation passes a real training update and memory measurement. This is the strongest starting configuration supported by the available evidence for an A100 80GB, four CPU cores, and 16GB host RAM; it is not a mathematically established global optimum.

The hardware can support a useful 9B LoRA experiment. A $35 GPU budget can fund a bounded training pilot, with $45–50 providing more room for evaluation or data work. Neither memory arithmetic nor published neighboring benchmarks establishes that the resulting model will reach 40–45% EnterpriseOps success. That remains an ambitious experimental target. A claim of top-five performance also requires a higher score than 45% against the current displayed competitors.

The analysis uses public source snapshots retrieved September 14–15, 2026, the quoted rental price, and read-only inspection of existing local experiment records. No A100 training, paid inference, or fresh EnterpriseOps task execution was performed for this report. The accompanying calculator reproduces resource and statistical scenarios; it does not predict accuracy.

**1. The benchmark and the target to beat.**

The relevant benchmark is **EnterpriseOps-Gym-AA**, Artificial Analysis's implementation of ServiceNow's EnterpriseOps-Gym. The live page confirms the previously cited frontier models. Its default displayed comparison includes the following results; this is a snapshot of selected chart entries, not a claim to have exhaustively ranked every selectable model.[^1]

| Displayed position | Model / setting | Whole-task success |
|---|---|---:|
| 1 | Claude Fable 5, max, with Opus 4.8 fallback | 51.12% |
| 2 | Gemini 3.7 Flash, medium | 50.40% |
| 3 | Gemini 3.5 Flash, high | 50.07% |
| 4 | DeepSeek V4 Pro 0813, max | 49.60% |
| 5 | Grok 4.6, high | 48.34% |

At least eleven displayed models exceed 45%. Therefore **40–45% could outperform some frontier models, but would not establish a current top-five position**. No verified EnterpriseOps-Gym-AA score for Qwen3.5-4B or Qwen3.5-9B was located. The older Qwen3 results in ServiceNow's repository are different checkpoints under another harness and cannot serve as these models' baseline scores.[^1][^3]

AA specifies **1,117 oracle-mode tasks, three repetitions per task, and up to 100 agent turns**. Each repetition starts from reset database state. All SQL outcome checks must pass for whole-task success. Three repetitions are averaged; this is not “keep the best of three.” Oracle mode supplies the relevant tools, not a correct action plan. AA explicitly distinguishes its harness and prompts from the paper's implementation.[^2]

This distinction changes the project objective. A 45% score on a custom holdout can be a useful result; it cannot be compared directly with 51.12% on a different set of tasks, tool definitions, context policies, and execution limits. A fair small-model result must specify the model **and** its agent interface.

**2. Published model comparison.**

Both the 4B and 9B are dense models with hybrid attention. For the otherwise unspecified MoE comparison, this report provisionally uses **Qwen3.5-35B-A3B**. It has roughly 35B total parameters and roughly 3B active per token. Its active count describes routing and arithmetic, not the amount of model weights that must reside in memory.

The following are Qwen's publisher-reported results, not measurements on EnterpriseOps or the proposed A100 setup. Dense-model values share one release table; MoE values come from its corresponding model card.[^4][^5]

| Benchmark | 4B | 9B | 35B-A3B MoE | 9B − 4B |
|---|---:|---:|---:|---:|
| BFCL v4 | 50.3 | 66.1 | 67.3 | +15.8 |
| τ²-Bench | 79.9 | 79.1 | 81.2 | −0.8 |
| VITA-Bench | 22.0 | 29.8 | 31.9 | +7.8 |
| DeepPlanning | 17.6 | 18.0 | 22.8 | +0.4 |
| IFEval | 89.8 | 91.5 | 91.9 | +1.7 |
| IFBench | 59.2 | 64.5 | 70.2 | +5.3 |
| MultiChallenge | 49.0 | 54.5 | 60.0 | +5.5 |
| AA-LCR | 57.0 | 63.0 | 58.5 | +6.0 |
| LongBench v2 | 50.0 | 55.2 | 59.0 | +5.2 |
| LiveCodeBench v6 | 55.8 | 65.6 | 74.6 | +9.8 |

The most relevant argument for 9B is stronger function calling and multi-step task performance while retaining substantial memory headroom. The exceptions matter: 4B wins τ²-Bench, the planning gain is small, and 9B beats the MoE on AA-LCR. There is no valid weighted average that turns these results into an EnterpriseOps prediction without a calibrated relationship to that benchmark. The τ² setup also includes particular airline-domain fixes, so its absolute score should not be treated as universal agent accuracy.[^4]

**Value judgment:** for one serious attempt at higher accuracy, 9B is worth its extra training cost. For testing data formatting, tool parsing, or many speculative data variants, 4B offers cheaper iterations. The MoE's BFCL improvement over 9B is only 1.2 points, although its planning advantage is larger. That evidence does not justify starting with a much tighter memory budget and more complicated expert kernels on this small host.

**3. What the earlier local experiment actually established.**

The saved “Research local Qwen fine-tuning” experiment records were inspected rather than treating the earlier conversation as a successful training result. A quantized Qwen3.5-4B configuration on the MacBook Air M4 with 16GiB memory completed a 6,144-token update/save/reload smoke. The 8,192-token attempt failed with a native Metal out-of-memory error before completing a microbatch. The successful 6K run peaked at 9.872GiB of MLX allocation, with substantial system memory pressure.[^6]

That configuration trained only the last eight blocks at rank 8, with 2,654,208 trainable parameters. It was much smaller than the proposed all-block A100 adapter. The subsequent candidate A used 33 next-assistant examples from three workflows, containing only 1,598 distinct supervised tokens. It trained and reloaded successfully but achieved **0/3 training diagnostic tasks and 0/2 development tasks**. Candidate B remained pending in the inspected draft; no outcome is inferred.[^7]

Several failures involved repeated lookups, incorrect identifiers, incomplete sets used for decisions, or failure to act after retrieving relevant facts. These are not explained solely by insufficient context. The small and correlated task sample cannot establish the 4B model's general capability ceiling, but it does establish that successful optimization and lower token loss are insufficient evidence of better enterprise execution.

Moving to the A100 removes a major hardware constraint and permits a stronger model and broader adapters. It does not turn those 33 examples into an adequate eight-domain curriculum. The next meaningful investment is in complete, varied, independently verified workflow demonstrations and a fair evaluation interface.

**4. Architecture and exact weight accounting.**

The 4B and 9B each contain 32 language blocks: 24 Gated DeltaNet linear-attention blocks and eight full-attention blocks. Hidden widths are 2,560 and 4,096; MLP intermediate widths are 9,216 and 12,288. Both use a 248,320-token vocabulary and native maximum position count of 262,144. Consequently, 6K is not their architectural context ceiling.[^8][^9]

The exact tensor inventories were reconstructed from official checkpoint headers and reconciled against the published shard index. “Text-only” includes the language model and output head, and excludes the vision tower and multi-token prediction component. These are counts and storage arithmetic, not measured CUDA residency.[^10][^11][^12]

| Quantity | 4B | 9B | 35B-A3B |
|---|---:|---:|---:|
| Text parameters, including output head | 4,205,751,296 | 8,953,803,264 | 34,660,610,688 |
| Ideal text BF16 storage, decimal GB | 8.412 | 17.908 | 69.321 |
| Complete published tensor payload, decimal GB | 9.320 | 19.306 | 71.904 |
| Complete payload, GiB | 8.680 | 17.980 | 66.965 |

Use **GB = 10⁹ bytes** and **GiB = 2³⁰ bytes** throughout. A nominal “80GB” label must be checked with the actual GPU's reported capacity. To avoid benefiting from a unit ambiguity, the planning calculation below assumes only **80 billion bytes = 74.506GiB**. If the actual device reports about 80GiB, the additional capacity is extra headroom.

A few small dynamics tensors are stored in FP32. Preserving the published dense text dtypes adds only 7,680 bytes to the ideal 2N calculation, immaterial to the rounded tables. Framework conversions of norms, additional components, or duplicated weights must still be measured. Freezing vision or MTP does not remove their storage; they save memory only if the loader actually omits them.

**5. Exact LoRA parameter calculation.**

For a frozen matrix W of shape d_out × d_in, LoRA trains A and B such that W′ = W + (α/r)BA. Its trainable parameter count is:

`P_adapter = r × (d_in + d_out)`

The proposed target set covers 248 linear matrices across all language blocks. It includes full-attention q/k/v/o projections; GDN qkv, z, a, b, and output projections; and MLP gate/up/down projections. It excludes embeddings, the output head, vision, MTP, convolutions, norms, and dynamics vectors. The base remains frozen.[^13][^14]

Using hidden width H and MLP width I, the exact count for this unfused layout is:

`A(r) = r × [8(4H + 14,336) + 24(5H + 16,448) + 32 × 3(H + I)]`

For example, the gated full-attention query projection outputs 8,192 values, not merely H. The GDN projection dimensions also differ from ordinary Transformer attention. A parameter estimate based on a generic Llama layer would therefore be wrong.

| Adapter rank | 4B trainable parameters | 9B trainable parameters | 9B adapter training states at 16 bytes/parameter |
|---|---:|---:|---:|
| 16 | 32,464,896 | 43,278,336 | 0.645GiB |
| 32 | 64,929,792 | 86,556,672 | 1.290GiB |
| 64 | 129,859,584 | 173,113,344 | 2.580GiB |

Rank 32 trains approximately 1.54% of the 4B text model or 0.97% of the 9B text model. Increasing 9B from rank 32 to 64 adds just 1.290GiB to this static state budget. Rank is therefore not the principal memory constraint. Choose it based on held-out performance, not the assumption that a larger rank guarantees better results.

The 16-byte allowance can represent FP32 adapter parameters, gradients, and two FP32 Adam moments, or an equivalent mixed-precision layout with master weights. It is applied only to trainable adapters. Frozen base weights do not require Adam moments or full-sized parameter gradients. Applying a full-fine-tuning multiplier to all nine billion parameters would wrongly reject LoRA.

Actual module names must be inspected after loading: some backends fuse `in_proj_a` and `in_proj_b`, changing the adapter layout and count. A generic seven-module Llama list misses the 24 GDN attention blocks. Conversely, `all-linear` applied indiscriminately to the whole multimodal model may include unwanted components. In particular, unfreezing both `embed_tokens` and `lm_head` adds approximately 2.03 billion trainable parameters to 9B. The proposed recipe does neither.

**6. Training-memory feasibility at 16K and 32K.**

The relevant memory equation is:

`M_peak = frozen weights + adapter states + retained activations + live temporary tensors + runtime/workspaces`

LoRA sharply reduces optimizer state; it does not eliminate activation gradients. Gradient checkpointing reduces retained activations by recomputing parts of the forward pass during backward. A useful explicit reference layout saves one BF16 residual stream at each of 32 block boundaries:

`M_boundaries = 2 bytes × 32 layers × microbatch × sequence_length × hidden_width`

This is an accounting term for that checkpoint layout, **not the entire activation allocation or a universal lower bound for every possible implementation**. Other checkpoint schemes can save different tensors or offload them. With microbatch 1 and rank 32:

| Model | Sequence | Frozen text + adapter states | Assumed boundary activations | Subtotal: explicitly not peak VRAM |
|---|---:|---:|---:|---:|
| 4B | 16,384 | 8.80GiB | 2.50GiB | 11.30GiB |
| 4B | 32,768 | 8.80GiB | 5.00GiB | 13.80GiB |
| 9B | 16,384 | 17.97GiB | 4.00GiB | 21.97GiB |
| 9B | 32,768 | 17.97GiB | 8.00GiB | 25.97GiB |

Now reserve 6GiB for runtime/workspaces and an additional 8GiB of safety headroom. Even if the entire published checkpoint stays resident, the remaining allowance for other live tensors is:

| Model | 16K allowance | 32K allowance |
|---|---:|---:|
| 4B | 48.36GiB | 45.86GiB |
| 9B | 37.24GiB | 33.24GiB |

For 9B at 32K, the explicit conditional fit statement is:

`25.97 + 1.30 + 6 + 8 + M_other_live ≤ 74.51 GiB`

`Therefore M_other_live must be ≤ 33.24 GiB.`

The 6GiB runtime reserve is a planning assumption, not a guaranteed bound; extra workspace beyond it consumes the remaining allowance. This makes the uncertainty visible rather than inventing a precise peak-memory number. Efficient kernels make both 9B lengths credible, with 16K the more conservative starting point. Actual peak allocation and reserved CUDA memory must be checked through backward, optimizer update, and checkpoint save.

Unsloth documents Qwen3.5 BF16 LoRA support and indicative memory figures of 10GB for 4B, 22GB for 9B, and 74GB for 35B-A3B. These corroborate feasibility but are **not certified 16K/32K measurements**; the worked example starts at 2K. Its current guide favors BF16 over four-bit training for this model family because of quantization differences.[^15]

Three implementation details can dominate the result:

| Allocation at microbatch 1 | 16K | 32K | Consequence |
|---|---:|---:|---|
| Full vocabulary logits in BF16 | 7.58GiB | 15.16GiB | Use fused/chunked linear cross-entropy |
| Full vocabulary logits in FP32 | 15.16GiB | 30.31GiB | Avoid a full logits cast and its duplicates |
| One naive 16-head BF16 attention score matrix | 8GiB | 32GiB | Use FlashAttention or verified memory-efficient SDPA |

Those attention figures are for one score tensor, before probabilities, gradients, or another layer. Merely installing a fast-attention package does not establish that the model selected its fast path. The GDN blocks also need supported fast linear-attention/convolution kernels; reference fallbacks can consume substantially more memory and time.[^16][^17]

**7. Other configurations and edge cases.**

| Configuration | Feasibility on this machine | Decision |
|---|---|---|
| 4B BF16 LoRA, rank 16–64, 16K | Strong candidate with ample headroom | Fast control or fallback |
| 4B BF16 LoRA, rank 32, 32K | Strong candidate with efficient kernels | Useful if long inputs dominate |
| 9B BF16 LoRA, rank 32, 16K | Strong candidate | Recommended first real run |
| 9B BF16 LoRA, rank 32, 32K | Credible conditional fit | Profile before committing time |
| 9B BF16 LoRA, rank 64 | Small extra static cost | Try only after evidence of underfitting |
| 4B/9B four-bit QLoRA | Smaller frozen weights; activations remain | Fallback, not the first choice here |
| 35B-A3B BF16 LoRA | Some optimized short-context setups fit | Too little comfortable long-context margin |
| 35B-A3B QLoRA | Potentially much smaller weight storage | Extra quantization/kernel uncertainty; defer |
| 4B full-parameter tuning | Conditional on optimizer and context | Possible, but lower priority than 9B LoRA |
| 9B conventional full Adam tuning | States alone exceed capacity | Outside this single-card recipe |

Four-bit storage is not exactly “N/2 bytes” in a real quantized model: scales, metadata, unquantized components, and dequantization buffers add memory. QLoRA's original work establishes substantial savings and good results on its evaluated models, not lossless quantization for every Qwen3.5 task.[^18] With enough BF16 headroom, quantizing the 9B before measuring a problem introduces an unnecessary experimental variable.

The MoE needs all experts resident unless it offloads them. An A3B name does not make it a three-billion-parameter memory footprint. Its complete checkpoint consumes 66.97GiB before adapter states and activations. Expert offload would collide with the 16GB host-RAM limit and add transfer overhead. Its routed execution may be efficient with suitable kernels, but active parameters alone do not determine measured tokens per second.

For full 4B tuning, optimizer precision changes the conclusion. The following are **text-only static states**, before activations and workspaces:

| State layout allowance | 4B | 9B |
|---|---:|---:|
| 12 bytes/parameter | 47.00GiB | 100.07GiB |
| 16 bytes/parameter | 62.67GiB | 133.42GiB |
| 18 bytes/parameter | 70.50GiB | 150.10GiB |

A 12-byte layout can correspond to BF16 weights/gradients and FP32 moments without an FP32 master copy; other mixed-precision optimizers use more. An optimized or lower-state optimizer can make full 4B tuning feasible, but it is a different numerical and implementation choice. The 16-byte case plus 32K boundary checkpoints already reaches 67.67GiB, leaving little room for live tensors under the conservative capacity assumption.

There is no theorem that updating all 4B parameters produces a better model than adapting a stronger 9B base. Research reports both LoRA shortcomings in extensive domain learning and near-full-tuning performance in well-configured post-training settings. These are task-dependent results, not a universal ranking.[^19][^20] For a small workflow dataset and a tight experiment budget, 9B LoRA is the more defensible first allocation.

**8. Host RAM, software, and storage.**

The 9B text weights alone occupy approximately 17.91 decimal GB, exceeding the quoted 16GB host RAM. A naive load-into-CPU-then-transfer workflow can therefore fail even when most VRAM is free. Use meta initialization and sharded, memory-efficient direct GPU loading in the selected training framework, with explicit BF16 dtype. Confirm that the loader did not retain a full CPU copy or dispatch layers to CPU. The existence of a low-memory loading option does not prove its exact peak on this host.[^21]

Tokenize and validate the training corpus before renting the expensive GPU where possible. Use disk-backed token arrays, dynamic padding, and zero to two loader workers rather than many processes duplicating the dataset. Start with packing disabled: independent sequences must reset GDN/convolution state as well as enforce attention boundaries. Historical library bugs make blind packing particularly risky for this architecture.[^22]

Keep training and evaluation as separate phases. A100 VRAM does not increase host RAM. Do not concurrently assume space for the trainer, a second inference copy, every domain's database server, large tokenization jobs, and many rollouts. Start evaluation at concurrency one and measure RAM/CPU before increasing it; Hybrid tasks may require multiple relevant domain servers. No official minimum establishes that all eight can be run concurrently on this configuration.

Save adapters and the exact tokenizer/template/configuration. Avoid routine full-model merging on a 16GB CPU host: a merge or conversion can need additional model-sized buffers. Budget disk for weights, software caches, dataset files, checkpoints, and container images; 60–100GB free is a reasonable provisioning allowance for the dense-model project, not a verified minimum. Four cores can also make first-run kernel compilation slow, so preparation time belongs in the cost calculation.

**9. Context and reasoning-token accounting.**

For each generation call, the actual bound is:

`context ≥ system/policy + tool schemas + current task + retained history/tool results + generated reasoning + generated answer/tool calls`

“Thinking” and “reasoning tokens” refer to the same generated reasoning budget here; they should not be counted twice. They are also not free space beyond the context window. Thinking should be explicitly controlled through the correct chat template and deployment settings.[^23]

An illustrative 16K allocation is 3,000 tokens of policy/tools, 6,500 of task/recent evidence, 2,200 of retained state, 3,000 of generated reasoning, and 800 of answer/tool calls: 15,500 tokens, with 884 remaining. These are proposed limits, not measured EnterpriseOps averages. Reject or restructure oversize examples rather than silently truncating the instruction, tool result, or target.

The original repository advertises roughly 89K average context per task without adequately defining whether this is cumulative processing or peak simultaneous input. It does not establish that every task needs an 89K window, and it does not establish that every task fits 32K.[^3] Record per-call peak input, output, and total tokens, plus overflow frequency and cumulative tokens. Repeated prompts can make cumulative work much larger than the largest individual context.

Training at a 16K maximum does not change a native 262K architecture into a 16K architecture. Longer inference may work, but quality and memory must be evaluated. Train on complete decision windows preserving required dependencies; use 32K selectively when measurement shows necessary information would otherwise be lost. Retain retrieval identifiers and query scope in compact memory, including whether a result is complete or filtered. Compact representations must be applied fairly when comparing systems.

**10. Training time and the $35–50 budget.**

The quoted prices are internally inconsistent: a $2.50/hour GPU cannot produce a $0.27/hour total. This report therefore calculates three interpretations. If “0.02 cents” is literal, it is $0.0002; if it means two cents, it is $0.02. No cloud provider was identified, so the rental price is an input rather than an independently verified quotation.

| Total credits | $2.50/hour | $2.52/hour | $2.77/hour |
|---|---:|---:|---:|
| $35 | 14.00h | 13.89h | 12.64h |
| $45 | 18.00h | 17.86h | 16.25h |
| $50 | 20.00h | 19.84h | 18.05h |

These are rental hours before any separately charged teacher API, storage, or other fixed cost. Additional $10–15 buys about 3.61–5.42 hours at $2.77/hour. The general equation is:

`H_train = (budget − external_costs)/hourly_rate − setup_hours − baseline_hours − evaluation_hours − export_hours`

`training_cost = processed_token_exposures / measured_tokens_per_second / 3600 × hourly_rate`

Count **all processed tokens**, including prompts, padding actually computed, and repeated epochs. Assistant-only loss reduces supervised target positions; it does not eliminate the forward/backward cost of context needed to predict those positions. Track both processed-token throughput and supervised-token throughput.

A coarse compute proxy helps check orders of magnitude. For frozen dense weights with input gradients and checkpoint recomputation, the dominant matrix term is approximately 6N FLOP per token: 2N forward, 2N backward through inputs, and 2N recomputation. A conservative full-attention term adds approximately `16 × 8 × S × 4096` FLOP per token. This ignores or approximates embeddings, GDN internals, adapters, loss kernels, and data movement; it is not a measured timing model.

| Model | 16K proxy | 32K proxy |
|---|---:|---:|
| 4B | 33.82 GFLOP/token | 42.41 GFLOP/token |
| 9B | 62.31 GFLOP/token | 70.90 GFLOP/token |

NVIDIA specifies 312 TFLOPS of dense BF16 Tensor Core peak for A100; the larger advertised sparse figure does not apply to ordinary dense model training.[^24] At an assumed 10% effective utilization, the 9B proxy gives about 501 tokens/second at 16K and 440 at 32K. These are scenarios. Kernel fallbacks, host stalls, padding, thermal behavior, and recompilation can make actual throughput much worse. Measure a warmed-up sequence of real updates before extrapolating.

At the conservative $2.77/hour rate:

| Total processed token exposures | At 250 tokens/s | At 500 tokens/s | At 1,000 tokens/s |
|---|---:|---:|---:|
| 2 million | 2.22h / $6.16 | 1.11h / $3.08 | 0.56h / $1.54 |
| 8 million | 8.89h / $24.62 | 4.44h / $12.31 | 2.22h / $6.16 |
| 16 million | 17.78h / $49.24 | 8.89h / $24.62 | 4.44h / $12.31 |

For example, 1,000 decision examples averaging 4,000 total tokens, trained for two epochs, consume 8 million token exposures—not 32 million merely because the configured maximum is 16K. Conversely, padding each example to 16K would change that calculation. Two epochs are not intrinsically optimal; task validation should select the checkpoint.

The same simplified model makes 9B about 1.84 times the arithmetic per token at 16K, or 1.67 times at 32K, compared with 4B. Actual wall-time ratios can differ. The value case for 9B is its stronger starting behavior, not a claim that its score per dollar is already measured.

**11. A concrete first-run configuration and spending plan.**

| Setting | Initial choice |
|---|---|
| Checkpoint | Qwen/Qwen3.5-9B, post-trained, pinned revision |
| Frozen base | BF16; omit vision/MTP where supported |
| Adaptation | LoRA in all 32 language blocks; explicit targets from Section 5 |
| Rank / alpha | 32 / 32, standard α/r scaling |
| Dropout / bias | 0 / none |
| Optimizer | AdamW on adapters only; FP32 adapter-state accounting |
| Learning rate | Start 1e-4; 5e-5 is a single follow-up alternative if validation warrants |
| Sequence maximum | 16,384; dynamically pad shorter complete examples |
| Microbatch / accumulation | 1 / 8; adjust to preserve a reasonable effective token batch |
| Loss | Assistant/tool-call target tokens; correct token-weighted normalization |
| Memory controls | Gradient checkpointing; fused/chunked CE; memory-efficient attention and GDN kernels |
| Cache / packing | Training use_cache=False; packing disabled initially |
| Schedule | Small warmup, approximately 3%; validate during 1–2 initial passes |
| Save | Adapter, tokenizer/template, configuration, data/split hashes |

These hyperparameters are a starting experiment, not a proven optimal setting. If microbatch lengths vary, normalize accumulation by the total supervised tokens in the accumulation window rather than giving arbitrarily short and long targets identical weight. Confirm that at least one nonzero adapter update occurs and reload the saved checkpoint before accepting the training implementation.

Prepare the data and compatible environment first. During the paid preflight, measure several actual 16K examples through full backward and optimizer update, then one 32K stress case with realistic supervision. Inspect process RSS and CUDA allocated/reserved peaks, verify intended module coverage, and confirm that fast kernels are used. If 32K is stable, use it only where data length or failure analysis warrants the extra work.

With verified training data already available, a practical $35 pilot at $2.77/hour is:

| Phase | Time allowance | Cost |
|---|---:|---:|
| Loading, compilation, memory/throughput preflight | 1h | $2.77 |
| Short matched 4B/9B baseline comparison | 1h | $2.77 |
| Main 9B training allocation | 7h | $19.39 |
| Held-out evaluation and checkpoint selection | 2.5h | $6.93 |
| Adapter export and reload | 0.5h | $1.39 |
| **Total rental** | **12h** | **$33.24** |
| **Remaining contingency** | — | **$1.76** |

The phase times are spending caps, not assertions that a fixed number of tasks will finish. At 500 processed tokens/second, seven training hours buy 12.6 million token exposures; at 250, they buy 6.3 million. Adjust the dataset/epoch count after profiling. If setup or evaluation runs longer, reduce training allocation instead of silently exceeding the budget.

At $50, prioritize better demonstrations and a larger paired evaluation before a rank sweep or many extra epochs. More credits cannot rescue a wrong tool parser, contaminated split, or incorrect reward function. If clean data do not yet exist, the all-in $35 plan must be smaller than the training-only plan above.

**12. Data, evaluation cost, and reproducibility barriers.**

The live public Hugging Face oracle files were downloaded and counted: Calendar 61, CSM 103, Drive 64, Email 67, HR 102, Hybrid 88, ITSM 103, and Teams 61—**649 tasks**. The files contain prompts, tool selections, configuration, and verifiers, but no ready-made gold action trajectories or training/evaluation partition. Domain names are dataset splits, not a train/test separation. Dataset prose and benchmark descriptions contain different larger counts.[^25]

This does not establish that AA's 1,117-task evaluation is wrong. It establishes that the publicly retrieved 649-task artifact cannot automatically reproduce its manifest. Before a leaderboard claim, obtain the exact task manifest, dataset/backend versions, prompts, scoring protocol, and allowed context handling. If unavailable, run competitors and the candidate on the same frozen custom holdout and label the result accordingly.

The public scorer also needs care. At the inspected repository revision, verifier results are keyed by verifier name; duplicate names overwrite earlier entries. Across the retrieved files, 543 of 3,496 verifier entries share keys that would be overwritten, affecting 101 tasks. Some duplicate checks may be equivalent. The issue tracker reports a subset with non-equivalent lost checks. This audit does **not** establish that AA's separate implementation has the bug.[^26][^27]

Score every required check by stable index/identity and verify completeness. Do not turn an empty set of evaluated checks into an accidental success, and do not silently remove context failures or model errors from the denominator. Pin corrected evaluation code and rerun matched baselines if its semantics differ from prior results. Report both strict task success and secondary diagnostic verifier results.

Training should use independent workflow instances or a split frozen before teacher generation. Keep related task variants, database lineages, and alternative tool modes together. Training on public task instances and evaluating on those same instances does not establish held-out performance. Synthetic tasks should vary policy constraints and action dependencies, not merely replace names in test solutions.

A reasonable curriculum teaches complete lookups, identifier resolution, multi-record conditions, reversible/irreversible state transitions, policy checking, verification after mutation, and stopping after completion. Include recovery demonstrations and permitted “cannot complete” outcomes. The existing 33 snippets are useful diagnostics, but not a substitute for broad coverage. A first data target of roughly 150–300 independently verified workflows, yielding many more decision windows, is an experiment-design recommendation—not a mathematical minimum for 40% success.

Frontier help costs money or consumes separately supplied resources. The live AA chart reports Gemini 3.7 Flash medium averaging about 4,173 generated tokens and $0.05881 per task, versus about 9,762 generated tokens for Fable 5. This includes reasoning in the generated total; fewer tokens do not imply weaker task performance.[^1] At that Flash average, 200 attempts cost about $11.76; one 1,117-task pass costs $65.69, and three cost $197.08. New synthetic tasks, caching, and providers may change those amounts. If only half the teacher attempts yield verified usable demonstrations, the expected attempts per accepted demonstration double under that simplified assumption.

Self-hosted evaluation also has a cost. Let R be attempts, P the average uncached prefill tokens per attempt, O generated tokens, p prefill throughput, g aggregate decode throughput, and t tool/reset seconds:

`evaluation_hours ≈ R × (P/p + O/g + t) / 3600`

This is an additive planning model. Concurrent execution can overlap tool waits, prefill, and decoding, so aggregate throughput and overhead must ultimately be measured together; the formula is not an exact wall-time prediction for a batched server.

For 1,117 × 3 attempts at 4,000 output tokens each, generation alone is 13.404 million tokens. At an assumed aggregate 100 tokens/second, that is 37.23 hours or $93.08 at $2.50/hour, before prefill and tools. At 500 aggregate tokens/second it is 7.45 hours, but achieving that batching rate on four cores and 16GB host RAM is not established. Training throughput is not a substitute for decode throughput.

Thus $35 can fund a useful pilot. It cannot honestly be represented as a guaranteed budget for creating the whole dataset, training, exhaustively tuning, and reproducing several complete frontier evaluations.

**13. What mathematics says about accuracy—and what it cannot say.**

The desired score is an expectation over previously unseen tasks and model outputs. It depends on the pretrained model, data quality and distribution, optimization, tool interface, context retention, environment correctness, and evaluation protocol. N parameters, r adapter rank, GPU FLOPs, and dollars do not specify that expectation. No defensible numerical probability of reaching 40% or beating four domains can be derived from the supplied hardware alone.

A simple model illustrates why improving execution reliability could nevertheless have substantial value. If a task needs k essential decisions, each independently correct with probability q, then:

`P(task success) = q^k; therefore q = target_success^(1/k)`

| Assumed essential decisions | q for 40% task success | q for 45% | q for 51.12% |
|---|---:|---:|---:|
| 10 | 91.24% | 92.33% | 93.51% |
| 20 | 95.52% | 96.09% | 96.70% |
| 30 | 96.99% | 97.37% | 97.79% |

Real decisions are correlated and tasks have different difficulties, so this is an illustration, not a forecast. It explains why fewer unnecessary steps, better identifiers, and correct state tracking can matter greatly. It does not let BFCL's 66.1% become a per-step q, nor does it turn average verifier success into full-task success by assuming independence.

The original EnterpriseOps paper supplies relevant encouraging evidence: older small Qwen executors improved markedly when supplied strong plans, and human-plan ablations produced 14–35-point gains. However, supplying a test-time oracle plan is a different experiment from teaching planning through LoRA. The result motivates learning compact planning and state-aware execution; it does not justify adding 14–35 points to an unmeasured Qwen3.5 baseline.[^28]

Other work demonstrates that specialized LoRA models can outperform larger general models on particular datasets, and that agent-trajectory training can improve generalization. Those papers use different models, data, benchmarks, and budgets. They establish that the direction is plausible, not that this particular run will succeed.[^29][^30]

**14. Four-domain wins and a valid decision rule.**

An overall 40% target says nothing about which domains are won. For reference, the current raw domain percentages for two named comparators are below; these are success rates, not the leaderboard heatmap's normalized color values.[^1]

| Domain | Fable 5 with fallback | Grok 4.6 high |
|---|---:|---:|
| CSM | 53.23% | 55.38% |
| HR | 50.00% | 45.65% |
| ITSM | 48.07% | 44.20% |
| Email | 58.65% | 57.69% |
| Calendar | 50.96% | 45.19% |
| Teams | 52.00% | 48.00% |
| Drive | 62.86% | 54.29% |
| Hybrid | 39.87% | 39.87% |

Beating Fable at 40% in four domains would not follow: only its Hybrid score is below 40%. Likewise, four-domain superiority over one named competitor is different from beating the best model in each domain. Choose the comparator and domain claim explicitly.

Use an initial stratified baseline across all eight domains to locate the candidate's actual strengths. Then predeclare four target domains before the final test. Calendar, Teams, Email, and Drive are reasonable initial hypotheses for a workflow curriculum, but their higher existing frontier scores can make them harder to beat. Do not select domains solely because their benchmark average is low or because a few observed tasks were easy. Keep a mixed-domain adapter initially; eight separate adapters would fragment the small dataset and experiment budget.

For a diagnostic result of 45 successes in 100 independent tasks, the 95% Wilson interval is approximately **35.6–54.8%**. At 90/200 it is **38.3–51.9%**. At 503/1,117 it is approximately **42.1–48.0%**. These describe sampling uncertainty under a simple independent-task model, not proof of generalization across shared task families.

Use paired task outcomes for model comparisons, with a task/family-level bootstrap or an appropriate paired test. Cluster the three repetitions by task rather than counting them as 3,351 independent task types. Predeclare the comparator and target domains, and specify how simultaneous domain claims or multiple testing will be handled. A high point estimate on a small chosen subset is not sufficient evidence of a frontier win.

The practical decision sequence is:

1. Validate data formatting, model loading, adapter coverage, kernels, and the scorer on small fixtures and real examples.
2. Run matched untuned 4B and 9B diagnostic baselines under the intended deployment interface. Retain failure categories and context overflow counts.
3. Train the chosen 9B adapter on independent, verified examples, using a capped token budget and intermediate development checks.
4. Promote only if held-out strict task success improves with no material regression in policy/state integrity. Loss reduction alone does not qualify.
5. Expand to a larger frozen evaluation and matched frontier baselines before making a public superiority claim. If the exact AA manifest is unavailable, state that the experiment is a custom EnterpriseOps evaluation.

If 9B fails to improve, inspect whether it actually learned complete training workflows, whether the train/deployment template matches, whether masks are correct, and whether errors come from the model or the interface. A small learning-rate or rank comparison follows that diagnosis; it does not precede it.

**15. The role of frontier assistance and iterative improvement.**

Frontier models can propose independent task instances, draft concise action plans, inspect failures, and produce candidate demonstrations. The environment and independent checks must validate the resulting state and unintended changes. Accepting self-written rewards or reusing final-test feedback as training material can create the appearance of improvement without a better model.

For the first budget, use supervised LoRA with verified demonstrations and checkpoint selection. Online long-horizon RL adds rollout generation, sparse whole-task rewards, environment resets, and substantial evaluation expense; it is not the most economical first move. The availability of LoRA RL implementations does not make its end-to-end compute cost equal to SFT.

Record the model revision, dataset provenance, teacher costs, prompt/template, adapter targets, random seeds, task manifest, context policy, and scored outcomes for each iteration. Use observable plans, experiment logs, and results as the documentation of the improvement process. A frontier-assisted sequence of training experiments is a useful foundation for automation; demonstrating autonomous recursive improvement would require separate evidence that the automated loop repeatedly improves on unseen evaluations within fixed resource limits.

**16. Reproducible calculations and final decision.**

The accompanying `qwen_a100_calculator.py` uses only Python's standard library. It reports rank/context memory tables, optimizer-state alternatives, price scenarios, token-throughput sensitivity, a coarse FLOP proxy, evaluation generation costs, and statistical illustrations. It makes no network calls and starts no training. `qwen_a100_scenarios.json` contains its default output.

To recompute an 8-million-token 9B training scenario at an assumed 500 tokens/second and $2.77/hour:

```bash
python3 qwen_a100_calculator.py --model 9B --context 16384 --rank 32 --tokens 8000000 --tps 500 --hourly 2.77 --budget 35 --nontrain-hours 4
```

Replace throughput with a measured sustained value from the actual machine; set `--external-cost` for teacher/API charges and `--capacity-gib` from the device's reported capacity. The memory result deliberately leaves actual peak unset. The important output is how much room remains for unmeasured live allocations, not an invented precise total.

**The recommended purchase of compute is a 9B BF16 LoRA pilot at 16K, with a measured path to 32K.** The mathematical resource analysis and related benchmark evidence justify that experiment. They do not establish a 40–45% score or a probability of beating frontier models. The most promising route to those targets is better complete-workflow data, correct state/tool handling, and matched held-out evaluation—not full 4B tuning or a MoE selected solely by its active parameter count.

**Sources and evidence notes**

[^1]: Artificial Analysis. [EnterpriseOps-Gym-AA live evaluation page](https://artificialanalysis.ai/evaluations/enterprise-ops-gym-aa). Accessed September 14–15, 2026. Raw public chart properties supplied selected model scores, domain success rates, and token/cost averages. Default chart selections are not an exhaustive ranking of all selectable models.
[^2]: Artificial Analysis. [Intelligence benchmarking methodology: EnterpriseOps-Gym-AA](https://artificialanalysis.ai/methodology/intelligence-benchmarking#enterprise-ops-gym-aa). Accessed September 14–15, 2026. Task count, repetitions, oracle tools, harness and scoring protocol.
[^3]: ServiceNow. [EnterpriseOps-Gym repository](https://github.com/ServiceNow/EnterpriseOps-Gym). Inspected revision `271f2c357f763376997dfd16807fcde2474ae41b`. Original leaderboard, environment instructions, and context-length description.
[^4]: Qwen. [Qwen3.5-9B model card](https://huggingface.co/Qwen/Qwen3.5-9B). Accessed September 14–15, 2026. Shared dense model benchmark table and evaluation notes. The corresponding [4B card](https://huggingface.co/Qwen/Qwen3.5-4B) was also checked.
[^5]: Qwen. [Qwen3.5-35B-A3B model card](https://huggingface.co/Qwen/Qwen3.5-35B-A3B). Accessed September 14–15, 2026. MoE identity and publisher benchmarks.
[^6]: Local experiment record, “Native-limit local training smoke,” `ECHO Architecture/RSI/hardware_smoke/native_limits/REPORT.md`, September 13–14, 2026. Read-only inspection of a private local source; no public URL. Establishes only the recorded Mac smoke results.
[^7]: Local experiment record, “Local Qwen fine-tuning pilot — draft,” `ECHO Architecture/RSI/pilot_v1/REPORT_DRAFT.md`, plus `runtime_6k/context_v3/qwen_probe_v1/REPORT.md`. Read-only snapshot September 14–15, 2026; private local sources, no public URL. Candidate B remained pending in the inspected draft.
[^8]: Qwen. [Qwen3.5-4B configuration](https://huggingface.co/Qwen/Qwen3.5-4B/blob/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/config.json). Pinned configuration and layer dimensions.
[^9]: Qwen. [Qwen3.5-9B configuration](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/config.json). Pinned configuration and layer dimensions.
[^10]: Qwen. [Qwen3.5-4B checkpoint index](https://huggingface.co/Qwen/Qwen3.5-4B/blob/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/model.safetensors.index.json). Tensor headers in its referenced shards were summed for component counts and bytes.
[^11]: Qwen. [Qwen3.5-9B checkpoint index](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/model.safetensors.index.json). Tensor headers in its referenced shards were summed for component counts and bytes.
[^12]: Qwen. [Qwen3.5-35B-A3B checkpoint index](https://huggingface.co/Qwen/Qwen3.5-35B-A3B/blob/59d61f3ce65a6d9863b86d2e96597125219dc754/model.safetensors.index.json). Tensor inventory and resident weight accounting.
[^13]: Hu et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685), 2021. Adapter factorization and parameter-efficient training.
[^14]: Hugging Face. [PEFT LoRA reference](https://huggingface.co/docs/peft/en/package_reference/lora). Accessed September 14–15, 2026. Target selection, rank, and adapter configuration.
[^15]: Unsloth. [Qwen3.5 fine-tuning guide](https://unsloth.ai/docs/models/qwen3.5/fine-tune). Accessed September 14–15, 2026. Supported configurations, framework memory claims, BF16 recommendation and example sequence length. These are implementation-provider claims, not new A100 measurements.
[^16]: Hugging Face. [Transformers Qwen3.5 documentation](https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_5). Accessed September 14–15, 2026. Hybrid architecture, text-only classes and fast-kernel/fallback behavior.
[^17]: Hugging Face. [TRL: Reducing memory usage](https://huggingface.co/docs/trl/main/en/reducing_memory_usage). Accessed September 14–15, 2026. Memory-saving training mechanisms. Specific peak values in this report are independently calculated scenarios.
[^18]: Dettmers et al. [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314), 2023. Quantized adapter training and its evaluated results.
[^19]: Biderman et al. [LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673), 2024. Empirical comparisons in programming and mathematics; results are not EnterpriseOps predictions.
[^20]: Thinking Machines Lab. [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/), September 29, 2025. Effects of target layers, rank and optimization in supervised and reinforcement learning settings.
[^21]: Hugging Face. [Instantiate a big model](https://huggingface.co/docs/transformers/main/en/big_models). Accessed September 14–15, 2026. Meta initialization, checkpoint sharding and dtype-aware loading; inference dispatch examples require care when adapting to training.
[^22]: Hugging Face Transformers. [Issue 46093](https://github.com/huggingface/transformers/issues/46093); ModelScope MS-SWIFT. [Issue 9618](https://github.com/modelscope/ms-swift/issues/9618). Primary implementation reports on packed-sequence handling in hybrid attention. The installed training path must be checked rather than assuming every version is affected.
[^23]: Qwen. [Qwen3.5-9B chat template](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/chat_template.jinja). Accessed September 14–15, 2026. Explicit thinking/template behavior.
[^24]: NVIDIA. [A100 product specifications](https://www.nvidia.com/en-us/data-center/a100/), accessed September 14–15, 2026. Dense BF16 peak arithmetic; manufacturer peak is not application throughput.
[^25]: ServiceNow-AI. [EnterpriseOps-Gym dataset](https://huggingface.co/datasets/ServiceNow-AI/EnterpriseOps-Gym). Eight public oracle parquet files downloaded and counted September 14–15, 2026; 649 rows in that retrieved snapshot. Task counts and schema were independently audited, not inferred from prose descriptions.
[^26]: ServiceNow EnterpriseOps-Gym. [Duplicate verifier name issue 23](https://github.com/ServiceNow/EnterpriseOps-Gym/issues/23), opened August 11, 2026. Reported semantic consequences; distinct from the independent duplicate-key count.
[^27]: ServiceNow. [Pinned benchmark executor source](https://github.com/ServiceNow/EnterpriseOps-Gym/blob/271f2c357f763376997dfd16807fcde2474ae41b/benchmark/executor.py). Inspected name-keyed verifier result behavior. No inference is made about AA's separate implementation.
[^28]: EnterpriseOps-Gym authors. [EnterpriseOps-Gym: Environments and Evaluations for Stateful Agentic Planning and Tool Use in Enterprise Settings](https://arxiv.org/html/2603.13594v1), 2026, especially Section 4.4. Planning ablations and small-model execution evidence.
[^29]: Predibase researchers. [LoRA Land: 310 Fine-tuned LLMs that Rival GPT-4, A Technical Report](https://arxiv.org/abs/2405.00732), 2024. Evidence for task specialization on other datasets, not a forecast for enterprise operations.
[^30]: Zeng et al. [AgentTuning: Enabling Generalized Agent Abilities for LLMs](https://arxiv.org/abs/2310.12823), 2023. Agent-trajectory instruction tuning and evaluation on different agent tasks.
