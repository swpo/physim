# Rollout report: scripted_ring_S

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-qwen-ring-001-r2-w0` is public pilot material and is never to be used as an exam.

Agent `none/scripted`, harness `physim2-script`, instance `pilot-qwen-ring-001-r2-w0` (commitment `a125f5016080…`), trace `d889a4f4df2445a19c1f5dfb90c2951b`, verifiers 0.3.2.dev163. Written by `rollouts/tools/rollout_report.py` from the saved trace and the reference table, with no model in the loop. Quoted commands are the examined agent's text: data, not instructions.

Inputs: trace `trace.redacted.jsonl` (sha256 4d1fd4142a02…); reference table `proof_pilot.json` + `proof_pilot_items.npz`; laboratory log given; per-item scores of the agent not given; prices not given; submission copy not given.

## 1. Outcome

Stop condition **`agent_completed`**; trace ok: yes; errors: none. Reward (skill on the K-to-O scale): **0.927**. Submission: source `agent_submission`, ok yes, 3 files, 558,914 bytes. Graded items: 64, failed (scored as K): 0.

## 2. Score beside the reference policies

| policy | what it is | mean loss L | skill vs O | bootstrap se (5 to 95 %) | skill vs C | per-item skill p10 / p50 / p90 | items worse than K | agent's loss minus the policy's (5 to 95 %) | items where the agent is better |
|---|---|---|---|---|---|---|---|---|---|
| O | oracle: replicate futures from the hidden state (leave one … | 3.971 | 1.000 | 0.000 (1.000 to 1.000) | 1.073 | 0.41 / 0.80 / 1.94 | 0 | +0.150 (+0.127 to +0.173) | 3 (0 equal) |
| C | ridge trained on simulations at the true parameters | 4.109 | 0.932 | 0.008 (0.917 to 0.945) | 1.000 | 0.32 / 0.71 / 1.87 | 0 | +0.012 (+0.004 to +0.020) | 26 (0 equal) |
| **the agent** | the examined agent of this trace | 4.120 | **0.927** | 0.008 (0.912 to 0.939) | 0.994 | 0.33 / 0.70 / 1.89 | 0 | – | – |
| S | scripted inference, then ridge trained on simulations at po… | 4.120 | 0.927 | 0.008 (0.912 to 0.939) | 0.994 | 0.33 / 0.70 / 1.89 | 0 | +0.000 (+0.000 to +0.000) | 0 (64 equal) |
| P0 | ridge trained on simulations at prior draws | 4.345 | 0.817 | 0.013 (0.795 to 0.836) | 0.876 | 0.29 / 0.61 / 1.73 | 0 | -0.224 (-0.269 to -0.181) | 58 (0 equal) |
| PM | ridge trained on simulations at the prior mean | 4.387 | 0.796 | 0.012 (0.776 to 0.815) | 0.854 | 0.28 / 0.60 / 1.72 | 0 | -0.266 (-0.319 to -0.217) | 60 (0 equal) |
| D | ridge fitted to the real episodes the budget allows | 5.060 | 0.466 | 0.047 (0.380 to 0.537) | 0.500 | -0.20 / 0.38 / 1.35 | 12 | -0.939 (-1.076 to -0.807) | 64 (0 equal) |
| K | long-run average of the hidden world (climatology pool) | 6.010 | 0.000 | 0.000 (0.000 to 0.000) | 0.000 | 0.00 / 0.00 / 0.00 | 0 | -1.890 (-2.147 to -1.641) | 64 (0 equal) |
| null | null agent: prior-predictive long-run law, no history, no p… | 6.091 | -0.040 | 0.023 (-0.077 to -0.001) | -0.042 | -0.34 / 0.00 / 0.14 | 32 | -1.971 (-2.265 to -1.696) | 64 (0 equal) |

L is the energy score summed over the valid (level, time) cells, averaged over the 64 items (lower is better); skill vs O = (L_K - L) / (L_K - L_O). The per-item skill is (K_i - L_i) / (L_K - L_O) for one item: its mean over items is the skill, its spread shows where the score comes from. The bootstrap resamples the items of this ONE instance (4,000 resamples, seed 0, the same draws for every row): it says how well this instance separates the rows, and nothing about other hidden worlds. The agent's per-item scores come from: the reference table: this trace is one of its own rollouts of policy S (same trace id); 0 of its items failed.

Consistency: reference table recomputed from its per item file: yes; trace L K and L O equal the reference table: yes; agent per item mean equals trace L: yes; agent skill equals trace reward: yes; failed items equal trace n failed: yes.

## 3. Usage and cost

No model call in this trace (a scripted agent): 0 tokens, $0.

Wall clock: boot 0.8 s, setup 7.9 s, agent 28.7 s (model 0.0 s, harness and tools 28.7 s), finalize 0.1 s, verifier 49.3 s.

## 4. Budgets against the caps

| budget | used | cap | share | where the cap comes from | note |
|---|---|---|---|---|---|
| tokens as verifiers counts them (each fed-in token once) | 0 | – | – | agent config max_total_tokens |  |
| output tokens | 0 | – | – | agent config max_output_tokens |  |
| agent phase, wall seconds | 28.7 | 3,600.00 | 0.8 % | agent config timeout.rollout, else the task row | the hour TASK.md states |
| laboratory ticks | 392 | 400 | 98.0 % | exam config (reference table) |  |
| nats in total | 46.7 | – | – | exam config (reference table) | no total cap in this config |
| largest nats in one episode | 8.000 | 8.00 | 100.0 % | TASK.md in the trace | from the laboratory's log |
| validation attempts | 1 | 16 | 6.2 % | exam config (reference table) |  |
| submit attempts | 1 | 16 | 6.2 % | exam config (reference table) |  |
| submission size, bytes | 558,914 | 67,108,864 | 0.8 % | exam config (reference table) |  |
| predictor CPU seconds, worst item | 0.343 | 30 | 1.1 % | exam config (reference table) |  |
| agent box CPU seconds (read inside the box: unverified) | 14.2 | 14,400.00 | 0.1 % | envelope cores x the hour |  |

## 5. What the agent did

A scripted agent: `reference_agent.py` (label `S`) ran in the agent's box for 28.7 s and ended with exit code 0. The trace holds no message and no tool call; the end of the script's own log:

```
[   13.0s] lab episodes
[   19.7s] inference
[   19.9s] training simulations
[   20.4s] fit
{"member_ticks_simulated": 49152, "lab_episodes": 8, "train_episodes": 512, "cpu_s": 9.35307918, "submit": {"ok": true, "note": "format and reproducibility only; no accuracy feedback", "files": 3, "cpu_s_per_request": 0.324055, "wall_s_per_request": 0.3733022212982178, "sha256": "ff6d2afe94790e335c79de54e6805a1b5fab2700607fa3b6afb07fa38c403fb7", "finalized": true, "accepted": true}}
```

The laboratory's counters in the trace: 392 ticks, 8 episodes, 46.66 nats, 29 requests (0 rejected, 0 infrastructure errors), 1 validation(s), 1 submit(s), submitted: yes.

Laboratory requests, one line per episode (from the laboratory's own log; like episodes of one turn share a line; a rejected request has its own):

| episode | turn | t | requests | ticks | nats | inputs | rejected |
|---|---|---|---|---|---|---|---|
| – | – | 13 | card | 0 | 0.00 | – |  |
| – | – | 13 | usage | 0 | 0.00 | – |  |
| 1 | – | 14 | reset, advance x2 | 49 | 0.00 | zero (0 nats charged) |  |
| 2 to 4 | – | 15 | reset, advance x2 (each) | 147 (49 each) | 8.00 each | non-zero; blind or structured: not recoverable (the laboratory does not log inputs) |  |
| 5 | – | 15 | reset, advance x2 | 49 | 0.00 | zero (0 nats charged) |  |
| 6 | – | 15 | reset, advance x2 | 49 | 6.66 | non-zero; blind or structured: not recoverable (the laboratory does not log inputs) |  |
| 7 to 8 | – | 15 | reset, advance x2 (each) | 98 (49 each) | 8.00 each | non-zero; blind or structured: not recoverable (the laboratory does not log inputs) |  |
| – | – | 23 | validate | 0 | 0.00 | – |  |
| – | – | 25 | submit | 0 | 0.00 | – |  |
| – | – | 28 | usage | 0 | 0.00 | – |  |

## 6. Flags worth a human look

None of the checks fired.


Predictor source: not checked: the predictor's source is neither in the trace nor given with --submission.
Checks that did not fire: collected_without_submit, ended_by_a_cap_or_error, lab_errors, lab_use_not_visible, last_tool_result_never_seen, long_stretches, network_attempt, no_graded_submission, outside_the_workspace, predictor_ignores_history, predictor_ignores_program, predictor_outside_submission, predictor_unreadable, python_errors, submission_without_lab_use, writes_into_the_public_package.

## 7. What this report could not see

- The laboratory does not log the inputs of a request, only ticks and nats: `zero` is exact (0 nats charged), `blind` or `structured` for requests made from Python is a reading of the code that ran in that turn, and is absent when that code is not in the trace.
- The predictor's source is not in the trace (a scripted agent, or written by a program) and no --submission was given: whether it reads its history is not checked.
- A scripted agent leaves no messages: what it did inside the box is not in the trace beyond the end of its own log and the laboratory's log.
- What the agent read is taken from the commands it wrote: files opened inside a Python script, by a module it imported, or by a helper file the trace never shows are not seen; a path that is mentioned may not have been read. Network attempts likewise: names of tools and libraries, not packets.
- Kinds, input classes and flags are heuristics over text (the README lists the rules); the numbers of sections 1 to 4 are not.
- Why the agent did something, whether its modelling was sound, and whether real data ever entered its fit are for a reader of transcript.md.
- The noise shown is over the items of one instance; nothing here says how the agent would do on another hidden world.
