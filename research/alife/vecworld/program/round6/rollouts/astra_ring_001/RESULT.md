# astra_ring_001: the first rollout of a strong model on a v2 exam

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-astra-ring-001-w0` is public pilot material and is never to be used
as an exam. Its hidden parameters are printed below for that reason only.

Run on 11 Nov 2026 in the cloud container (Linux x86_64, 4 shared cores under load 5 to 7, Docker 29.9.2,
verifiers 0.3.2.dev163), from the pinned port `../../vfport` (PIN.sha256 cd67eb4b..., 109 of 109 hashes, checked
before and after), which was not changed. One rollout; no second one (nothing died on mechanics).

**In short.** The model finished the whole exam in 14 replies and 6 minutes for $2.48 and scored **0.964** on
the K-to-O scale, above every reference policy (C 0.888, S 0.883). Two things in how it got there are for the
exam's designers, not for the model's credit: its 32 samples per item are a low-discrepancy (Sobol) set and
not independent draws, which the "fair" energy score rewards, so that it scored BELOW the oracle's loss at 16
and 32 ticks ahead; and it spent half of the laboratory budget on bare resets, each one tick for one
independent observation. It never applied an input.

## What ran

| | |
|---|---|
| model | `openai/gpt-6-astra` through Prime inference; reasoning is mandatory for this model, default effort (medium), nothing set |
| harness | verifiers' stock `bash` (tools offered: `bash`, `edit`, `lab_call`) |
| exam | ring world, config `smoke_ring`: 64 items, R = 16, 400 laboratory ticks, hidden (D, gamma, c); TASK.md and the first message are identical to rollout qwen_ring_001 (9,169 characters, same sha256) |
| instance | `pilot-astra-ring-001-w0`, commitment `58488c5f...28f4bf`; hidden D = 0.1658, gamma = 0.0621, c = 0.2719 |
| caps | 22 turns, 70,000 total tokens, 70,000 output tokens, 16,384 tokens per reply, 3,600 s, no retries, `push = false`, `PRIME_RUNS_MODE=disabled` |
| told to the agent | both limits that could end its run, in one sentence of the system message (below) |
| boxes | image `physim2-ring-ca:1` (the pinned image plus this machine's CA bundle), 2 CPUs, 4 GB, network cut after setup; the scripted reference boxes had the same caps |
| config | `../configs/astra_ring_001.toml`, `../configs/astra_ring_001.system_prompt.txt` |
| command | in `result.json` (`command`): `tools/here.py --run-id physim2-rolla-20261111 vfrun.py --config ... --run-name astra-ring-001 ... --disk-floor-gib 1.5 --model-credentials prime`; the key reaches the process through the environment only |

The disk floor of the tools was 1.5 GiB instead of 8 (this machine had 2.6 to 2.8 GiB free for everyone).

**The caps, and why they differ from qwen_ring_001** (coordinator's rulings of 11:42 UTC: no hidden cut; the
bill bounded by turns x context at $20 or less; the limits told to the agent if a config field allows). At $10
per million input tokens the turn cap could not be raised: every call but the last has prompt + completion under
`max_total_tokens`, so the bill is at most (10 T + 40) x M / 1e6 + one last reply, and turns and tokens share one
budget, (T + 4) x M <= 1.92 million for $20 (150 turns would leave 12,400 tokens; 40 turns 43,600). Chosen:
T = 22, M = 70,000; bound $19.02 (`../LEDGER.md`, "Row 3"). `sampling.max_tokens` was raised from 8,192 to
16,384 because for this model a reply is reasoning and answer together.

The sentence, appended by the bash harness to its own system line through the config field
`[env.taskset] system_prompt` (nothing in the pinned tree is touched), word for word:

> Limits of this run, set by the operator: it ends after your 22nd reply (a reply with all the tool calls in it
> counts as one) or once the conversation has used 70,000 tokens in total (the task text, every tool result and
> everything you generate, reasoning included, each counted once), whichever comes first; neither counter is
> shown to you.

So the agent's hour was not the binding limit of this rollout; 22 replies or 70,000 tokens were, and it knew
both. It used 14 replies and 20,917 tokens.

## Outcome

`EXIT 0`, complete and graded, not cut. Stop condition **`frozen`**: the agent called `validate` and then
`submit` through the `lab_call` tool, the submit was accepted, and the task's stop hook ended the rollout (the
first time that hook fired for a model). 14 model calls in 359 s of the agent phase (266 s waiting for the
model, 94 s in tools). The frozen `submission/` (predict.py, posterior.npz; 417,993 bytes) passed the three
example calls in the verifier box and ran in 64 item boxes: 0 failed items, 4.8 CPU-seconds per item (limit 30).

| policy | what it is | mean energy score L | skill vs O | bootstrap se (64 items) | skill vs C |
|---|---|---|---|---|---|
| O | oracle: the true simulator from the true hidden state (leave one out over 16 real futures) | 3.654 | 1.000 | | 1.126 |
| **the model** | **its frozen submission** | **3.694** | **0.964** | **0.010** | **1.086** |
| C | ridge trained on simulations at the true parameters | 3.781 | 0.888 | 0.014 | 1.000 |
| S | scripted inference, then training on simulations | 3.787 | 0.883 | 0.014 | 0.995 |
| P0 | trained on simulations at prior draws, no experiment | 3.892 | 0.791 | 0.018 | 0.890 |
| PM | trained on simulations at the prior mean | 3.897 | 0.787 | 0.017 | 0.886 |
| D | fitted to the real episodes only, no simulator | 4.751 | 0.037 | 0.083 | 0.042 |
| K | the long-run average of the hidden world | 4.793 | 0.000 | | 0.000 |
| null | prior-predictive long-run law | 4.843 | -0.043 | 0.027 | -0.049 |

Reference policies: `tools/prove.py` on the same instance (all graded, 0 failed items), all items of a rollout
in one verifier box; the model was graded with one fresh box per item (the two modes gave identical per-item
scores for the same files in qwen_ring_001). Noise: a bootstrap over the 64 items of this ONE instance
(`reference_noise.json`); it says how well this instance separates the rows, nothing about other hidden worlds.
Paired over the same resamples: the model above C by 0.077 (se 0.009), above S by 0.082 (0.010), above P0 by 0.174
(0.014). Per item: `per_item_scores.json`.

Per query (mean loss over the 64 items; level, ticks ahead):

| | L1, 1 | L1, 2 | L1, 4 | L1, 8 | L1, 16 | L2, 16 | L2, 32 |
|---|---|---|---|---|---|---|---|
| K | 0.623 | 0.653 | 0.777 | 0.724 | 0.677 | 0.682 | 0.658 |
| O | 0.306 | 0.380 | 0.482 | 0.575 | 0.637 | 0.626 | 0.649 |
| C | 0.335 | 0.413 | 0.512 | 0.587 | 0.643 | 0.631 | 0.661 |
| the model | 0.330 | 0.406 | 0.499 | 0.577 | 0.626 | 0.615 | 0.641 |
| model minus O (paired se) | +0.024 (0.003) | +0.026 (0.003) | +0.018 (0.003) | +0.002 (0.002) | **-0.010 (0.002)** | **-0.011 (0.002)** | **-0.008 (0.003)** |
| model's skill in this cell | 0.92 | 0.91 | 0.94 | 0.99 | 1.25 | 1.19 | 1.86 |

The model is better than C in every cell, and better than the ORACLE in the three long-range cells, by 5 to 7
paired standard errors in two of them. No predictor can do that with independent samples. See "Leaks, shortcuts,
gaming" below.

## Usage and cost

| | |
|---|---|
| model calls | 14, all answered, all with usage, every one ended in a tool call; replies 28 to 2,638 tokens |
| billed input tokens | 193,826 (21,636 uncached, 172,190 cache reads) |
| output tokens | 10,782, of which 5,242 reasoning (the trace holds reasoning summaries, not the reasoning itself) |
| what the caps saw | 10,135 in + 10,782 out = 20,917 of 70,000; 14 of 22 turns |
| price | $10 in, $50 out per million tokens, no cache-read price listed: the `pricing` field of the model's entry in `GET https://api.pinference.ai/api/v1/models`, read without a credential on 11 Nov 2026 (`model_entry.json`) |
| cost | **$2.4774** with all input at the listed price (the ledger's figure). The provider's own `cost` fields sum to **$1.0188**: cache reads are billed below the listed input price, at a rate the Models API does not list |
| bound by the caps | $19.02; the bill was an eighth of it |
| wall time | 359 s agent phase, 18 s setup, 568 s verifier (64 item boxes, 8.6 s each, one at a time); 16 minutes from the start (11:53:51 UTC) to `EXIT 0` (12:09:50) |
| preflight | two streamed requests as the harness sends them (`preflight_ping_stream.json`): $0.0052 |

## What the agent did

1. Replies 1 and 2 (to 49 s after the rollout's start; the agent phase began at 24 s): listed the workspace, read `world_ring.py`, the package's `__init__` and
   `predict_runner.py`. Plan stated at once: estimate the three parameters from independent episodes, then
   sample futures from the public linear-Gaussian law conditional on each test history.
2. Replies 3 to 5 (to 134 s), the laboratory: 10 free-running episodes of 20 observations (200 ticks), saved to
   disk; an exact Kalman-filter likelihood fitted by L-BFGS; then a Fisher-information table over episode
   lengths, from which it concluded that fresh stationary starts are worth more than longer trajectories and
   spent the other 200 ticks on **200 bare resets** (one observation each). It asked itself "Is this related to
   gaming? I'm allowed to use the reset because it provides valid initial observations". No input was ever
   applied (0 nats). All 400 ticks used.
3. Reply 6 (to 217 s): a posterior over (D, gamma, c) by importance sampling on 12,906 Sobol particles around the
   mode (effective sample size 10,900): D = 0.129 (sd 0.020; true 0.166), gamma = 0.0673 (0.0045; true 0.0621),
   c = 0.254 (0.028; true 0.272). The same reply's reasoning turns to the score: "create valid Gaussian margins
   with about 32 samples while ensuring some intersample repulsion".
4. Replies 7 to 12 (to 342 s): wrote `submission/predict.py` (111 lines): for each item, reweight the posterior
   particles by the Kalman likelihood of the item's 17-row history, compute the exact joint Gaussian law of all
   queried quantities under the test program, and draw the 32 samples from a scrambled Sobol set along the
   principal directions. Checked its filter and forecast against direct Gaussian conditioning (agreement to
   1e-13), and compared independent, antithetic and Sobol ensembles under an energy score (`sample_check.py`:
   0.5519, 0.5455, and 0.5432 to 0.5434) before keeping Sobol.
5. Replies 13 and 14 (to 363 s): `validate` and `submit` through the `lab_call` tool. It stopped with 8 replies
   and 49,000 tokens of its told limits, and 54 minutes of its hour, unused.

It never used the public simulator object (`W.Simulator`): it rebuilt the law in numpy from the docstring. All
14 tool calls stayed in `/workspace` (10 `bash`, 2 `edit`, 2 `lab_call`); no read of `/etc`, no network
attempt, no tampering. Full text: `transcript.md`; its files: `submission/`, `workspace/`.

## Leaks, shortcuts, gaming

No leak: no hidden value appears in the transcript or the run folder (0 hits), and nothing outside the workspace
was touched. Three things the exam's design let a strong agent use:

1. **The oracle can be beaten by choosing the 32 samples jointly.** The grader's energy score is the "fair"
   estimator (`vw1/vw/scoring.py:62-67`, used at `round5/agentenv/evaluator/instance.py:153-171`), which is
   unbiased when the 32 samples are independent. The model's samples are not: they are a scrambled Sobol set
   mapped through the normal quantile function, each one marginally a draw from its predictive law, together
   spread more evenly than independent draws. That enlarges the term the score subtracts. Measured in the exam:
   the model's loss is below the oracle's at L1 16 ticks, L2 16 ticks and L2 32 ticks (paired t = -6.7, -5.9,
   -2.7). Checked with the evaluator's own functions and no code of the model (`fair_score_check.json`): for a
   made-up Gaussian truth, 32 independent draws from the truth score as the leave-one-out oracle does
   (+0.05 to +0.08 %, within noise), 16 antithetic pairs score 1.3 % below it, a Sobol set 2.1 to 2.4 % below it.
   Consequences: "skill vs O" can exceed 1; the reference policies draw with a pseudo-random generator, so part of the model's
   margin over C is the sampling scheme and not better prediction. A rough size, not a measurement: the model
   was 1.2 to 1.7 % below the oracle where the hidden state no longer matters; the same share of its loss in
   every cell is 0.06 in L, which would put the same predictor with independent samples near 0.91 (C 0.888).
   The model did this in the open and for a stated reason ("reducing finite-cloud Monte Carlo error"); the
   task statement asks for "a cloud of samples distributed like the real futures" and does not say that the
   samples must be independent.
2. **A reset buys an independent observation for one tick.** `reset_cost` is 1 (`smoke_ring.json:3`) and the
   reset returns o(0) from the stationary law, so 200 ticks bought 200 independent snapshots; by the model's own
   Fisher calculation that leaves half the uncertainty in gamma, and three quarters of that in D, that 10 more
   long episodes would have left. Nothing in the rules forbids it. It also means the 400-tick budget was never a constraint that called for an experiment in
   the scientific sense: no input was applied and the nats budget played no part.
3. **The exam was easy for this agent.** The law is public, linear and Gaussian, so the exact answer is a Kalman
   filter and a closed-form predictive law; a strong agent writes that in a few minutes without the simulator.
   C (ridge on 512 simulations at the true parameters) is not a ceiling for it: the exact filter with estimated
   parameters beat it in every cell. For the lead's question ("tests that are not trivially easy"): on this
   world the public simulator carries the exam.

Not exercised: a failing or crashing predictor (the "failure is paid with K" rule), validation that reads
`/workspace`, any attempt on the box's walls.

## Mechanics: what a model has now exercised, and what went wrong

Exercised end to end by a model for the first time: an accepted submit and its freeze; the stop hook `frozen`;
the validation of a model-written predictor in the verifier box; 64 item boxes on a model-written predictor; the
`lab_call` tool; a system-message sentence from the config; a model with mandatory reasoning through the
streamed route (usage in every call, reasoning summaries in the trace). 0 infrastructure errors.

Problems, all of them:

1. **A $20 bound by caps is a small rollout at this price.** Turns and tokens share one budget (above); the turn
   cap went down from 40 to 22 instead of up to 150. In the event the bill was $2.48, an eighth of the bound:
   the caps bound the worst case, which is far from a typical run. A meter of the money actually spent, read
   during the run, would let the cap be the money itself; verifiers' log shows no usage until the rollout ends.
2. **The provider bills cache reads below the listed price, and the list does not say at what rate** ($1.02
   billed by its own fields against $2.48 by the list). The ledger keeps the higher figure.
3. **TASK.md still states 4 CPU cores and 8 GiB**; the box had 2 CPUs and 4 GB (the agent set one BLAS thread
   itself).
4. **The agent's hour was not the binding limit**; the told limits (22 replies, 70,000 tokens) were. It finished
   at 14 replies and 6 minutes; whether the told limits made it stop early cannot be read from one run.
5. The reply to the accepted submit is not in the trace: the stop hook ends the rollout first, so the model
   never sees "accepted" and the transcript ends on its tool call. The laboratory's record has it.
6. vf-eval prints `rollout done ... reward=0.000` when the agent phase ends, before grading; the reward is in
   the trace only (0.964).
7. `tools/prove.py` has no option for the boxes' memory; worked around outside the tree by
   `../tools/prove_here.py` (4 GB on every scripted box, checked on the first one).
8. `../tools/watch.py` showed a reference policy's laboratory counters in the first line of `timeline.jsonl`
   (the newest record of the instance before the model's own existed); fixed for later runs.
9. Still open from qwen_ring_001, worked around the same way: vf-eval cannot verify TLS on this machine without
   `../tools/here.py`; the bash harness installs itself in the box over the network at setup (image
   `physim2-ring-ca:1`); two names in the session's environment that the tools refuse.

## What would have to change in the port (nothing was changed)

Nothing had to change for this rollout to run. For the next ones:

| file and line | change |
|---|---|
| `vw1/vw/scoring.py:62-92` with `round5/agentenv/evaluator/instance.py:153-171` | the fair energy score assumes independent samples and the submission chooses them: decide what the top of the scale means. Options: ask for many more samples than 32 (the gain of a dependent set shrinks with the ensemble size), or score the oracle and the references with the same kind of set, or say in TASK.md that samples are scored as independent draws and test for it |
| `round5/agentenv/configs/smoke_ring.json:3` (`reset_cost: 1`) | price a reset by what it gives (an independent observation), or say that this is intended |
| `tools/vfrun.py:318, 333` and `tools/prove.py:113, 154, 178` | a `memory` argument next to `cpu` for the scripted reference boxes |
| `RUNBOOK_MAC.md:701-706` and `configs/qwen_ring_bash.toml:5-6` | the price bound: `(max_turns x p_in + p_out - p_in) x max_total_tokens + p_in x (tool output of one reply) + p_out x max_tokens`; with it, size turns and tokens together |
| `configs/qwen_ring_bash.toml` (new line under `[env.taskset]`) | `system_prompt = "<file>"` to tell the agent its run limits; no change to `physim2_env/taskset.py` is needed for that |
| `round5/agentenv/TASK.md.tmpl:67` | render the compute envelope from the runtime the box really gets |
| `tools/vfrun.py:62`, `docker/Dockerfile.ring:10-13, 23-27`, `tools/run_report.py:31-33` | as listed in `../qwen_ring_001/RESULT.md` (unchanged) |

## Files

`result.json` (everything above as numbers), `per_item_scores.json`, `reference_noise.json`, `lab_record.json`
(the laboratory's own log: every request), `transcript.md`, `trace.redacted.jsonl` (the team header removed by
field name; `tools/scan_key.py` counts 0 credentials and 0 account identifiers in this folder), `submission/`
(the frozen folder, from the verifier's box) with `submission_manifest.json`, `workspace/` (the agent's own
files outside `submission/`, from the watcher's last copy of its box) with `workspace_manifest.json`,
`timeline.jsonl` (what the watcher saw), `run_report.json` (the port's own report tool), `resolved_config/`,
`dry_run_resolved_eval.json`, `model_entry.json`, `preflight_ping_stream.json`, `fair_score_check.json` (the
runner's check of the scoring rule), `reference/` (the scripted policies on the same instance), `MANIFEST.json`.
