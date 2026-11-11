# First model rollouts of the v2 exam (round 6)

PILOT_NEVER_REUSE_AS_EXAM: every instance named here is public pilot material and is never to be used as an exam.

Two models took the ring exam on 11 Nov 2026, one rollout each, in the coordinator's cloud container, from the
environment pinned at commit 08bd5a66 (`../vfport`). The ring is the small smoke-test world: a linear Gaussian law
with three hidden numbers, 64 exam items, a Lab budget of 400 ticks. Each rollout has its own folder with the
runner's `RESULT.md`, an independent `READING.md`, the full `transcript.md` and the reference table of scripted
policies on the same instance. Spend is in `LEDGER.md` and `ledger.json`: $2.59 for both, at the listed prices.

| | cheap model (`qwen_ring_001`) | strong model (`astra_ring_001`) |
|---|---|---|
| limits | 40 replies, not told to the agent | 22 replies and 70,000 tokens, told to the agent |
| replies used, agent time | 40 of 40, 11 minutes | 14 of 22, 6 minutes |
| Lab use | 18 passive episodes, printed, never saved or fitted | 10 passive episodes, then 200 bare resets; fitted |
| predictor | written outside `submission/`, never run | exact filter over a fitted posterior, validated, submitted |
| score (oracle = 1, climatology = 0) | 0.000 by rule (nothing submitted) | 0.964 (item bootstrap error 0.010) |
| scripted policies on the same instance | C 0.932, S 0.927, P0 0.817, D 0.466, null -0.040 | C 0.888, S 0.883, P0 0.791, D 0.037, null -0.043 |
| cost at the listed prices | $0.10 | $2.48 (the provider's own cost fields sum to $1.02) |

C trains at the true hidden numbers, S infers them by a script and then simulates, P0 simulates the public prior
without any experiment, D fits the Lab data alone, null uses the public prior only. One instance and 64 items each:
the errors say nothing about other hidden worlds, and the same scripts move by 0.03 to 0.04 between instances.

## What the two rollouts show

1. The ring exam is trivially easy for a strong agent. The law is linear and Gaussian, so the answer has a closed
   form: the agent wrote the exact likelihood, fitted it to Lab data and sampled from the exact predictive law. It
   never ran the public simulator, never applied an input and revised no plan.
2. The cheap model saw the same physics (it also wrote an exact likelihood) and failed on workflow: it kept no Lab
   data, spent 21 replies on simulated data, never ran its predictor and was cut by a limit it had not been told.
   Its 0.000 is a rule, not a measurement.
3. So this exam separated the two agents on bookkeeping, not on science, and neither rollout shows interesting
   modelling. That is the expected verdict on a smoke-test world, and the instance also fails the program's own
   acceptance bars (knowing the hidden numbers is worth 11% of the gap between climatology and C; the bar is 15%).
4. No leak and no tampering in either transcript.

## Faults of the exam that the rollouts exposed

- A hidden reply limit decided the first rollout.
- An empty submission was scored as climatology (0.000), which beats the honest null policy (-0.040): failing was
  paid.
- The score can be raised without better prediction. With 32 samples per item, samples chosen jointly (a scrambled
  Sobol set) score 2.1 to 2.5% better than independent draws from the same law, so the oracle row can be beaten.
  The reading estimates that 0.05 to 0.08 of the strong model's 0.964 comes from this (an estimate, not measured);
  without it the agent sits about level with C.
- A bare reset of the Lab bought one independent observation for one tick; the strong model spent half its budget
  on 200 of them.
- The library's token limits do not bound the bill: only replies times context does. The first rollout billed
  758,132 input tokens where the limit had counted 18,759.
- The stock harness installed packages inside the box at set-up; the task statement named a larger machine than
  the box had; Lab replies were lost unless the agent saved them.

Each of these is being fixed in the next pinned version of the environment (`../vfport`, round 4; the rulings are
in `../../roadmap/DECISIONS.md`).

## What follows for the program

The lead's direction asks for tests that are "not trivially easy for the agents" and for rollouts that show
"interesting modeling". The ring cannot give either; it stays as the mechanics check. The next rollouts need a
world without a closed-form answer that passes the acceptance bars: the candidates are the round-6 exam designs
(`../dials`) and the worlds the world cards single out (`../cards`). Those rollouts run on the lead's Mac by
request files once the new pinned version has passed its audits and the Mac session's review.

`tools/rollout_report.py` turns a saved trace and a reference table into the tables above without a model in the
loop (42 checks; its numbers equal the first runner's files).
