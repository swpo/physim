# qwen_ring_002: the first model rollout from a request (rehearsal of the round-4 pin)

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-qwen-ring-002` is public pilot material and is never to be used as an
exam. Its hidden parameters are printed below for that reason only.

Run on 11 Nov 2026 in the cloud container (Linux x86_64, 4 shared cores, Docker 29.9.2, verifiers 0.3.2.dev163)
by the integrator of port round 4, as the last of three jobs of the rehearsal of `../../vfport/RUNBOOK_MAC.md`
step 3 (`../../vfport/results/rehearsal_round4.json`). Every command was issued as ONE `sh -c` line copied from the
runbook of the pin `d9694f3e5b6c92a98c13fb36f02645f01f18728c` (sha256 of `PIN.sha256`
`9f1511add96b527d0ef208f81f5195162c4159740e898fefbb7dde6396d896e4`), from a fresh clone of that commit, with the
substitutions listed in the record. This folder is the publication folder that `tools/pack_rollout.py` made
(17 files, `MANIFEST.json`), copied unchanged; `RESULT.md` and `reference_noise.json` were added afterwards and
are not in the manifest. Evidence: run through vf-eval (the rollout, the reference table, the grading); read (the
transcript and the trace); the bootstrap below was computed afterwards from the per-item scores.

## What ran

| | |
|---|---|
| request | `../../vfport/rehearsal/round4_jobs/qwen-ring-002.json` (schema `rollout-job/v1`; kept there, never under a `requests/` folder) |
| config | `../configs/qwen_ring_002.toml` (= `config.toml` here): the defaults of the ring profile |
| model | `qwen/qwen3.6-35b-a3b` through Prime inference; reasoning not requested (`reasoning_effort = "default"`, nothing sent) |
| harness | verifiers' stock `bash` harness, preinstalled in image `physim2-ring:2` (no download in the box at set-up) |
| exam | profile `ring`, exam config `ring_r4`: 64 items, 256 samples per item, 400 laboratory ticks, a reset costs 17 ticks |
| instance | `pilot-qwen-ring-002`, commitment `05869e59...0203`; hidden D = 0.2367, gamma = 0.0951, c = -0.2650 |
| caps (disclosed in the task statement) | 150 turns, 60 minutes, 8,192 tokens per reply, context 200,000 tokens, spend 2 dollars; box 2 CPUs, 4 GiB, 512 processes, read-only root |
| spend stop | `cap_usd` 2.00; one worst-case call $0.0303; bound on the bill $2.0303 |

## Outcome

The agent stopped by itself (stop condition `agent_completed`: its 143rd reply had no tool call) after
**143 of 150 turns** and **38.6 of 60 minutes** (2,313 s agent phase; 1,705 s of it waiting for the model). It
**left a predictor**: `submission/predict.py` (4.2 KB) with the baseline's `pool.npz` beside it, graded from the
final collection (ruling E1: it never called `lab.submit`), in 64 fresh item boxes, no item failed, no fallback.
**Reward (skill on the K-to-O scale): 0.786.**

| policy | what it is | skill vs O | bootstrap se | the model minus this row (paired se) |
|---|---|---|---|---|
| O | oracle: the true simulator from the true hidden state | 1.000 | | |
| C | ridge trained on simulations at the true parameters | 0.896 | 0.012 | -0.111 (0.013) |
| S | scripted inference, then training on simulations | 0.868 | 0.015 | -0.083 (0.011) |
| **the model** | **Kalman filter at the prior-mean parameters, state sampled from a blended covariance** | **0.786** | **0.016** | |
| PM | ridge trained on simulations at the prior mean | 0.755 | 0.021 | +0.031 (0.011) |
| P0 | ridge trained on simulations at prior draws, no experiment | 0.737 | 0.023 | +0.049 (0.014) |
| D | fitted to the real episodes only, no simulator | 0.056 | 0.079 | +0.728 (0.076) |
| K | the long-run average of the hidden world | 0.000 | | |
| null | the baseline every box starts with (prior-predictive long-run law) | -0.026 | 0.013 | +0.811 (0.017) |

Reference policies: stage `reference` of the job (`tools/prove.py` by profile on the job's own instance, in
boxes with the model's caps; all graded, 0 failed items; `reference.json`). The model's score was recomputed
from `grades.json` and the reference's per-item scores: 0.7856, as graded. Noise: a bootstrap over the 64 items
of this one instance, 2,000 resamples, the same resamples for every row (`reference_noise.json`); it says how
well this instance separates the rows, nothing about other hidden worlds.

## What the agent did (five lines)

1. Turns 1 to 20: read TASK.md, the baseline, the public package and the laboratory's card and usage.
2. Turns 14 to 31: 11 free-running laboratory episodes of 17 observations at 34 ticks each (374 of 400 ticks, 0 nats, within 70 s); two later requests were refused for budget. It printed those episodes and never fitted anything to them.
3. Turns 23 to 34: read the world's source in its box and wrote down the linear-Gaussian state-space form (circulant A, block-sum observations, noise 0.3).
4. Turns 35 to 133: rewrote `submission/predict.py` 15 times (importance weighting over prior parameter pools with Kalman likelihoods, then spread calibration against simulated episodes at chosen parameters) and ran `python -m physim2.validate submission` 12 times; `lab.validate` never.
5. It settled on a Kalman filter at the prior-mean parameters with no parameter inference, deleted its 11 MB pool (turn 136), read the turns and seconds left from `lab.usage()` (turn 139: 11 turns and about 21 minutes), and ended with a summary.

Full text: `transcript.md`; raw record: `trace.redacted.jsonl`; the laboratory's replies: `lab_log.jsonl`.

## Usage and cost

| | |
|---|---|
| model calls | 143, all streamed, all with usage, none refused or cut; 0 reasoning tokens, no reasoning in any reply (the trace's `info.physim2.reasoning`) |
| billed input tokens | 7,280,288 (681,239 at the input price + 6,599,049 cache reads); the largest prompt 106,419 of the 200,000 allowed |
| output tokens | 74,233 (the longest reply 3,488 of 8,192) |
| price | $0.11 in, $1.01 out, $0.099 cache read per million tokens, read from `GET https://api.pinference.ai/api/v1/models` at run start (`model_entry.json`) |
| cost as counted | **$0.8050** (`usage.json`: per call the listed prices with the cache-read price, or the provider's own cost field where that was higher, on 65 of 143 calls); $0.8758 with all input at the full input price |
| against the bounds | 40 % of the bound on the bill ($2.0303 = `cap_usd` + one worst-case call), 14 % of the crude bound ($5.57 = 150 turns x a full 262,144-token window + replies); the spend stop never came near (`cap_usd` 2) |
| reconciliation | Prime's bill for this rollout was not read here; the runner on the Mac reconciles counted against billed (more than 10 % + $0.05 above the count means the count is wrong) |
| wall time | 17:57:31 to 18:41:12 UTC: 19 s set-up, 2,313 s agent, 273 s grading (64 item boxes, 4.1 s each) |

## What this rollout shows about the exam and the mechanics

- Ruling E1 with a real model: no submit, graded from what `submission/` held when the agent stopped.
- Rulings E4 and E5: the agent read `turns_left` and `seconds_left` from `lab.usage()` (turns 53, 124, 139); it never
  needed `lab_log.jsonl` (it did not use its real data at all).
- The 17-tick price of a reset (E13): the agent spent its laboratory in 11 short episodes in its first two
  minutes, before it had a plan for the data, and then could not afford an 18th observation run. The data was not
  the binding limit of its score; its choice not to infer the parameters was.
- Not trivially easy for this agent: it beat the prior-only rows (P0, PM) by 0.03 to 0.05 with a filter at the
  prior mean, and stayed 0.08 below the scripted inference S and 0.11 below C. The top two rows are ridge
  predictors, not the exact filter (ruling E16, not done), so how far below the best possible predictor 0.786 is
  remains unknown.
- Mechanics: no fault in the run. One fault of the report tool, found here and fixed after the first push
  (`tools/run_report.py` printed `"7_num_turns": null` for every saved trace; it now counts the sampled nodes,
  as verifiers does).

## Files

`status.json` (the job: request, stages, bounds, the trace's summary, the grade, the ledger rows), `grades.json`
(per item), `reference.json` (the reference table), `usage.json` (every model call with its tokens and counted
cost), `model_entry.json`, `lab_log.jsonl`, `transcript.md`, `trace.redacted.jsonl`, `submission/` and
`submission.json` (the graded copy and its manifest), `request.json`, `config.toml`, `resolved.toml`,
`key_scan.json` (clean: the credentials of the machine, generic credential shapes and the instance's hidden values;
no machine detail replaced), `MANIFEST.json` (sha256 of every packed file), `PILOT_NEVER_REUSE_AS_EXAM.txt`;
added: `RESULT.md`, `reference_noise.json`.
