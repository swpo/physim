# Reading of rollout astra_ring_001

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-astra-ring-001-w0` is public pilot material, never to be used as an exam.

Read start to end; checked against the raw trace and per-item scores.

**In short:** the agent solved the exam as a textbook exercise in six minutes, without a real experiment. Its 0.964 overstates its prediction: an estimated 0.05 to 0.08 comes from how it spaced its 32 samples.

## 1. What it did (14 replies, 359 s)

- Replies 1–2: read `world_ring.py`; plan before any data: "estimate the three parameters from independent episodes, then use the public linear-Gaussian law to sample futures".
- Reply 3: 10 passive episodes of 20 observations (200 ticks), saved to disk.
- Reply 4: exact Kalman-filter likelihood, fitted; a Fisher-information table over episode lengths.
- Reply 5: on that table, 200 bare resets. "Is this related to gaming? I'm allowed to use the reset because it provides valid initial observations".
- Reply 6: posterior: D 0.129 (true 0.166), gamma 0.067 (0.062), c 0.254 (0.272). Also: "ensuring some intersample repulsion".
- Replies 7–12: predictor: posterior reweighted by the item's history, exact predictive law under the test program, 32 scrambled Sobol points. Checks: formulas against direct Gaussian conditioning (zero input only); sampling schemes scored (independent 0.5519, Sobol 0.5432).
- Replies 13–14: Lab `validate`, `submit`.

It never ran the public simulator, applied an input, or compared a prediction with real data.

## 2. Approach in the program's terms

S with the simulator replaced by algebra: exact likelihood instead of simulated summaries, exact predictive law instead of a trained ridge. Its hypothesis is the posterior; the truth lies inside it (D at 1.9 sd). It was never tested on held-out data. Experiments changed one decision: the first 200 ticks led to the reset design.

## 3. Where it landed (one instance, 64 items)

Skill: O 1.000, **model 0.964** (se 0.010), C 0.888, S 0.883, P0 0.791, PM 0.787, D 0.037, null -0.043. Better than C on 60 of 64 items, in every program class.

By horizon: 7–8% above the oracle's loss at 1–2 ticks (O knows the hidden state), equal at 8, 1.2–1.7% below it at 16 and 32 (up to 6.7 se), which independent samples cannot do. My check: Sobol draws from the true law score 2.1–2.5% below independent ones. Without that gain the model sits near 0.89–0.92 (estimate): about level with C. Its D estimate was three times further off than S's: the margin is not better inference.

## 4. Budgets (used of allowed)

Lab ticks 400 of 400; nats 0 (8 per episode); replies 14 of 22; tokens 20,917 of 70,000; wall 359 s of 3,600. Only the tick budget visibly shaped behaviour; it never mentioned its told limits.

## 5. Easy, hard or broken, for this agent

Trivially easy, on a partly broken scale. No failed command, no rejected Lab request, no revised plan: the law is linear and Gaussian, so the answer is closed-form. This instance fails the program's own acceptance bars: knowing the parameters is worth 11% of the K-to-C gap (bar: 15%), and the script S closes 95% of that (bar: 70%).

## 6. Leaks, shortcuts, gaming

No leak: all 14 calls stayed in `/workspace`; no network attempt, no tampering, no hidden value in the transcript.

For an adversary:

- **Sample spacing beats the oracle**, by up to 1/(m-1) of the score: 3% at 32 samples.
- **Resets are cheap snapshots:** each start comes from the stationary law, which depends on the parameters.
- Unread, but in the box: the grader's scoring code and the designers' closed-form library (`_vendor/vw1/vw/lingauss.py`).

## 7. Mechanics and wording, with the fix

Nothing cost this agent a turn. For the next one:

1. TASK.md §4 does not say whether a sample is paired with itself; the agent assumed so ("includes the diagonal"). Fix: "over pairs of different samples, scored as independent draws".
2. Counters hidden: add replies and tokens left to `lab.usage()`.
3. TASK.md says 4 cores, 8 GiB; the box had 2 and 4: render from the runtime.
4. Reasoning is encrypted in 4 of 14 replies, summarised elsewhere: request summaries everywhere.

## 8. Before the next rollout

1. Fix the top of the scale: ask for 256 samples (Sobol gain 0.3%) and add reference rows: the exact filter at the true parameters and at the prior.
2. Retire the ring for strong models: use a world without a closed-form answer that passes the acceptance bars, and price a reset like a history (17 ticks).
3. Show the counters and size caps by money billed: this run cost $2.48 of a $19 bound.

## 9. The two agents side by side

Both saw the same physics: Qwen also wrote an exact Kalman likelihood. Astra saved its Lab data, fitted them within two replies, ran and checked its predictor, and submitted; Qwen spent 21 turns on simulated data, saved nothing and never ran its predictor. The scores differ by 0.96, far beyond noise (item se 0.01–0.02; the same scripts shift 0.03–0.04 between instances), but Qwen's 0.000 is a rule, not a measurement. The exam separated them on workflow, not science. For the lead's question: the ring is trivially easy for a strong agent and tests bookkeeping in a weak one; neither rollout shows interesting modelling yet.
