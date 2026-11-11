# Reading of rollout qwen_ring_001

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-qwen-ring-001-r2-w0` is public pilot material, never to be used as an exam.

Read start to end and checked against the raw trace and the Lab log; the agent's code was read, not run.

**In short:** the agent understood the physics and failed on the workflow. It discarded every real observation, never ran its predictor, and hit a 40-turn limit it was never told about. Its 0.000 is the rule "no predictor is scored as K", not a measurement.

## 1. What it did (40 turns, 11 minutes)

- Turns 1–13: re-read TASK.md, read `world_ring.py`, printed the Lab card, ran one Lab episode. Two calls failed (`lab.experiment('exp1', None)`, then `[]`) before zeros worked.
- Turns 14–36: 21 turns on its own simulator: an exact Kalman-filter likelihood for the linear Gaussian law, tested on simulated data at an invented θ (log-likelihood -106.17 at the true parameters, -105.60 at wrong ones). Its correct conclusion: "we can't reliably pinpoint the true parameters from history alone".
- Lab, interleaved: 18 passive 16-tick episodes, no input ever, each inside a one-off `python -c` that printed a few rows and exited. 306 rows observed, 35 printed, none saved, none fitted.
- Turn 37: "The key is to get good parameter inference from real experiments". It drew 10 more episodes, printed one, then planned a predictor that uses no Lab data.
- Turns 38–39: simulated 2,000 episodes at prior draws and wrote `/workspace/predict.py`, outside `submission/`: per item, weight prior draws by the Kalman likelihood of the item's 17-row history, then simulate forward under the test program.
- Turn 40: `lab.validate('submission')` on the empty folder; the cap cut the run before the answer arrived. Predictor never run, nothing submitted.

## 2. Approach in the program's terms

Intended S (infer, then simulate); built P0 with an exact filter (prior only); graded as K. It formed no hypothesis about the hidden world (no estimate of D, gamma or c from real data), and no experiment changed a decision. It never observed ticks 17 to 48 or a push, which is what every item asks about.

## 3. Where it landed (one instance, 64 items)

Skill: O 1.000, C 0.932, S 0.927, P0 0.817, PM 0.796, D 0.466, **model 0.000**, null -0.040.

The model equals K on every item and cell: no per-item pattern, no noise. The references show that on this instance parameters matter only at long range: P0 and C score 0.93 and 0.94 one tick ahead, 0.58 and 0.94 at 16 ticks, 0.23 and 0.76 for level 2 at 32.

## 4. Budgets (used of allowed)

- Turns: 40 of 40, cap undisclosed.
- Agent wall time: 643 s of 3,600.
- Lab ticks: 306 of 400. Nats: 0 (8 per episode allowed).
- Output tokens: 18,888 of 60,000.
- Validations: 1 of 16. Submits: 0.

It read `lab.usage()` once (turn 9) and never mentioned time; the one limit that decided the outcome was invisible to it.

## 5. Easy, hard or broken, for this agent

Not trivially easy, and not yet a test of science: the run ended on workflow first. Partly broken by the hidden turn limit. More turns alone would not have rescued it quickly: its predictor cannot run as written (it calls `rng.randn`, which does not exist), returns the wrong array shape, and loads `/workspace/episodes.npz`, absent where items are graded.

## 6. Leaks, shortcuts, gaming

None attempted: all 40 calls were `bash` inside `/workspace`, with no read of `/etc`, no network attempt, no tampering. No hidden value appears in the transcript; the example requests are simulated at the prior mean.

What a smarter adversary could use:

- **Failure is paid.** A missing or crashing predictor receives K, samples from the hidden world's own long-run law, which the agent cannot know. Submitting nothing (0.000) beat the honest null agent (-0.040, se 0.023). Crashing on purpose when unsure would lift D from 0.466 to at most 0.520 (reference table's counterfactual).
- From the code, not exercised: in-box validation can read `/workspace`, so a pass does not prove the predictor runs where it is graded.

## 7. Mechanics and wording, with the fix

1. Undisclosed turn cap: state it in the prompt and show turns left in `lab.usage()`.
2. Lab data vanish unless saved: `labclient.py` should append every reply to `/workspace/lab_log.jsonl` and TASK.md should say so.
3. `experiment(label, None)` dies inside `json` with a traceback (2 turns): raise `LabError("inputs: a (T, n_in) array or an integer T")` and document the integer form.
4. Lab and item history conflated (turn 15: "Bayesian inference on (D, gamma, c) given the observed history"): add "The Lab and all exam items share the same three hidden numbers."
5. TASK promises 4 cores and 8 GiB; the box had 2 and 4: render the envelope from the runtime.
6. No reply carries reasoning (2,742 characters of prose in 40 turns): record whether it is on.

## 8. Before the next rollout

1. Disclose the turn limit and raise it to about 150 (a turn took 16 s), sizing the bill by turns times context.
2. Stop paying failure with K: score a missing or failed predictor as the null agent, or ship a working null-agent `submission/predict.py`.
3. Log Lab replies to disk and fix the `experiment` error, so the next agent fails on the science, not on bookkeeping.
