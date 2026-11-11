# Round 6, study foundryexam: an exam pilot where the hidden law is a network's weights

**Question.** Round 5 found that with a correct public simulator and a few hidden parameters, a policy with no
hypothesis and no experiment (P0: train on simulations of the public prior) takes nearly all the skill. Does that
still hold when the hidden part is the 250 numbers of the level-0 network itself, and the public simulator is the
family, not the world?

**Answer.** Less than before, and how much less depends on three dials that this pilot measured.
- On the foundry's transport automaton, observed in the block view, P0 takes 0.863 [0.835, 0.889] of the skill of a
  net trained at the true weights (C) when the exam's prior is the screened prior, and 0.868 [0.840, 0.899] when it is
  a 30% neighbourhood of a public world. With a 10% neighbourhood it takes 0.958, as in round 5.
- The remaining tenth is not reserved for science. P0 fine-tuned on Lab episodes, with no hypothesis, closes 33% of
  the gap at 32 episodes and 71% at 512. The science share sigma is 0.12 at 8 Lab episodes and 0.04 at 512, below the
  0.15 bar at every budget when all horizons are pooled.
- The horizon is the strongest dial. At 16 ticks alone, P0 takes 0.66 [0.58, 0.74] of C, and sigma is 0.33 [0.26,
  0.42] at 8 Lab episodes, 0.25 [0.20, 0.32] at 32 and 0.11 at 512 (screened prior). This breakdown was first made
  after job 003 and then repeated on new items in job 004.
- A scripted inference of the world from Lab statistics (amortised S) adds nothing: rho is 0.01 to 0.05.
- C is a lower bound: it still gains from more true-weight data (section "What C is worth"), so P0's shares are upper
  bounds and the sigmas lower bounds.

**PILOT ONLY.** Every hidden world here is a public function of public seeds and its weights are written to public
outputs (`origin/gpu-jobs:jobs/<job>/out/full/<arm>/worlds.json`). These worlds, Labs and items must never be
reused as an exam.

Every number below is in `results/summary.json` with its source (job, file, key). Design, criteria and thresholds:
`DESIGN.md`, committed before the first GPU request; its sections 5b, 5c and 5d record what was changed later and
what had been seen by then.

## What is public, hidden and told

Public: the family (`../../round5/foundry/tnca.py`: law, noise, wind channel, initial distribution), the prior over
its 250 numbers, the screen, the block view, the item format, the program mix, the nats caps, the scoring rule.
Hidden: the weights of the hidden world, the noise secret, the items' futures. The agent has the family's simulator,
a Lab on the hidden world (exam-shaped episodes in the block view, 200 nats per episode on average, caps 100 per
tick and 400 per episode) and items: 17 observed frames, a public 16-tick wind program, queries at 1, 2, 4, 8, 16
ticks.

| arm | the exam's prior | hidden | hidden worlds | prior worlds of P0 |
|---|---|---|---|---|
| P | the screened prior: round 5's candidates that are still active at the exam's burn-in (300 ticks) | 240 weights + 10 scalars | 16 | 210 |
| N30 | 30% weight neighbourhoods of three public centre worlds (draws 3078, 1672, 7567) | 240 weights | 12 | 128, 83, 128 |
| N10 | 10% neighbourhoods of the same centres | 240 weights | 12 | 128 each |

Gate at the exam's burn-in: 226 of 416 pool worlds pass (171 of the 323 enriched candidates of prior seed 2027, from
which the 16 hidden worlds are drawn); 457 of 816 neighbours at 30%, 709 of 816 at 10%. A 30% change of the weights
stops the activity of nearly half the neighbours of a shortlisted world.

Reference policies, one net family (periodic conv net on the block grid, noise inputs, fair energy score): K
climatology; O the simulator from the hidden state; C trained at the true weights; P0 trained on simulations of the
prior worlds, reading each item's own history; P0s the same from the last two frames; S(N) amortised inference from N
Lab episodes; FT(N) P0 fine-tuned on N Lab episodes; D(N) a net on N Lab episodes alone; Dr(N) a local ridge on N Lab
episodes; plug-in simulators from the hidden state with wrong weights or without the test program.

## What ran

| job | state | card | pod-hours billed | billed | what |
|---|---|---|---|---|---|
| r6-foundryexam-001 | rejected by the runner's validation (notes over 4,000 characters) | - | 0 | $0 | - |
| r6-foundryexam-002 | cancelled by the runner when 003 arrived | A100 40GB | 0.96 | $1.92 | one dispatch per training step: 70 ms per step of two nets, 3.5 times the round-5 basis; nothing of it enters the results |
| r6-foundryexam-003 | done, exit 0 | A100 40GB | 1.07 | $2.13 | first full pass, three arms (C on 1,536 episodes; 24-32 prior worlds in the N arms) |
| r6-foundryexam-004 | done, exit 0 | A100 40GB | 2.17 | $4.33 | the table below: C on 4,096 episodes with 8,000 steps, 83-128 prior worlds in the N arms, new seeds, items and Labs |
| r6-foundryexam-005 | see "What C is worth" | A100 40GB | | | arm P again with a third reference net on 16,384 episodes |

Job 004: 80.9 million member-ticks of the 64 x 64 automaton (float64) in 2.05 h on an A100-SXM4-40GB (lambdalabs,
$1.99/h), jax 0.12.0.1; 40 hidden worlds, each with a Lab of 512 episodes, 32 items x 12 replicate futures and 96
climatology runs; 724 trained nets (float32). No part failed or was skipped in 003 or 004. Each job passed the
runner's code review (`results/job/review_*.md`) and a presmoke at full shapes.

## Results (job 004; pooled skill, climatology 0, oracle 1; ± world-clustered SE with a training seed drawn per resample)

| policy | arm P | arm N30 | arm N10 |
|---|---|---|---|
| O: simulator from the hidden state | 1 | 1 | 1 |
| C: net at the true weights, 4,096 episodes | 0.768 ± 0.028 | 0.851 ± 0.024 | 0.817 ± 0.017 |
| P0 fine-tuned on the same true-weight episodes | 0.754 ± 0.029 | 0.836 ± 0.025 | 0.814 ± 0.017 |
| C on 1,024 episodes only | 0.734 ± 0.029 | 0.828 ± 0.027 | 0.786 ± 0.019 |
| FT(512): P0 fine-tuned on 512 Lab episodes | 0.737 ± 0.030 | 0.818 ± 0.026 | 0.800 ± 0.018 |
| FT(128) / FT(32) / FT(8) | 0.717 / 0.697 / 0.673 | 0.798 / 0.778 / 0.747 | 0.787 / 0.783 / 0.782 |
| D(512): net on 512 Lab episodes alone | 0.710 ± 0.029 | 0.797 ± 0.029 | 0.753 ± 0.021 |
| D(128) / D(32) / D(8) | 0.653 / 0.575 / 0.479 | 0.720 / 0.618 / 0.501 | 0.683 / 0.576 / 0.438 |
| Dr(512) / Dr(8): local ridge on Lab episodes | 0.665 / 0.637 | 0.656 / 0.629 | 0.657 / 0.630 |
| S(512) / S(8) / S(0): amortised inference | 0.665 / 0.664 / 0.658 | 0.742 / 0.742 / 0.739 | 0.784 / 0.783 / 0.780 |
| P0: prior simulations, own history | 0.663 ± 0.034 | 0.739 ± 0.027 | 0.783 ± 0.018 |
| P0s: prior simulations, last two frames | 0.646 ± 0.036 | 0.676 ± 0.034 | 0.728 ± 0.020 |
| P0 on 64 / 16 prior worlds | 0.628 / 0.522 | - | - |
| persistence | 0.216 ± 0.090 | 0.143 ± 0.127 | 0.083 ± 0.067 |

The ± on a level is mostly world-to-world spread of the level; the paired gaps below are much tighter.

| quantity (90% interval) | arm P | arm N30 | arm N10 |
|---|---|---|---|
| share of C's skill with no hypothesis and no experiment | 0.863 [0.835, 0.889] | 0.868 [0.840, 0.899] | 0.958 [0.949, 0.966] |
| median over hidden worlds | 0.858 | 0.870 | 0.959 |
| criterion 2 (trivially easy at 0.95 or more, not at 0.85 or less) | undecided | undecided | undecided, 0.949 at the lower end |
| sigma with no Lab | 0.137 [0.111, 0.165] | 0.132 [0.101, 0.160] | 0.042 [0.034, 0.051] |
| sigma at 8 / 32 / 128 Lab episodes | 0.123 / 0.092 / 0.067 | 0.122 / 0.086 / 0.062 | 0.042 / 0.041 / 0.036 |
| sigma at 512 (the declared null: best of D, FT, Dr at 512, P0, S(0)) | 0.040 [0.031, 0.050] | 0.039 [0.028, 0.050] | 0.021 [0.016, 0.025] |
| verdict against the 0.15 bar | fail (null FT(512)) | fail | fail |
| rho of amortised S at 8 / 512 Lab episodes | 0.01 ± 0.04 / 0.02 ± 0.04 | 0.03 ± 0.03 / 0.03 ± 0.03 | 0.02 ± 0.05 / 0.05 ± 0.04 |
| share of the P0-to-C gap closed by FT at 8 / 32 / 128 / 512 | 0.10 / 0.33 / 0.51 / 0.71 | 0.07 / 0.35 / 0.53 / 0.71 | -0.02 / 0.02 / 0.14 / 0.51 |
| C - P0 | 0.105 ± 0.010 | 0.112 ± 0.016 | 0.034 ± 0.004 |
| P0 - P0s (reading the world off the item's history) | 0.017 ± 0.005 | 0.063 ± 0.015 | 0.054 ± 0.007 |
| O - C (out of reach of a history-only net) | 0.232 ± 0.028 | 0.149 ± 0.024 | 0.183 ± 0.017 |
| C - C on 1,024 episodes | 0.034 ± 0.003 | 0.023 ± 0.004 | 0.031 ± 0.004 |
| data only (better of D, Dr): Lab episodes for 90% of C / to match P0 | 286 / 85 | 293 / 179 | 358 / more than 512 |
| state-given loss, weights from the prior (median world) | 1.53 [1.13, 2.16] (1.23) | 0.79 [0.64, 0.95] (0.67) | 0.37 [0.27, 0.48] (0.33) |
| state-given loss, weights off by 3% / 10% / 30% | 0.09 / 0.32 / 0.80 | 0.09 / 0.33 / 0.71 | 0.08 / 0.35 / 0.81 |
| input-blind oracle loss on items with a program | 0.085 [0.055, 0.116] | 0.126 [0.100, 0.153] | 0.127 [0.106, 0.150] |
| by class: blind / aimed / regional | 0.013 / 0.086 / 0.154 | 0.011 / 0.127 / 0.240 | 0.012 / 0.131 / 0.238 |
| criterion 4 (0.10); hidden worlds at 0.10 or more | undecided; 6 of 16 | actions matter; 8 of 12 | actions matter; 8 of 12 |
| share of variance carried by the tick alone, largest world | 1.7e-05 | 6.2e-05 | 3.3e-06 |

By query horizon (job 004, the same bootstrap; a breakdown first made after job 003):

| arm | quantity | 1 tick | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| P | skill of C | 0.94 | 0.88 | 0.79 | 0.67 | 0.52 |
| P | P0's share of C | 0.97 [0.96, 0.98] | 0.93 [0.91, 0.95] | 0.86 [0.82, 0.89] | 0.76 [0.70, 0.81] | 0.66 [0.58, 0.74] |
| P | sigma at 8 Lab episodes | 0.03 | 0.05 | 0.12 [0.09, 0.15] | 0.22 [0.17, 0.28] | 0.33 [0.26, 0.42] |
| P | sigma at 32 | 0.02 | 0.04 | 0.09 | 0.16 [0.12, 0.20] | 0.25 [0.20, 0.32] |
| P | sigma at 512 | 0.01 | 0.02 | 0.04 | 0.07 [0.05, 0.09] | 0.11 [0.08, 0.14] |
| N30 | P0's share of C | 0.97 | 0.94 | 0.88 | 0.82 [0.78, 0.86] | 0.67 [0.55, 0.78] |
| N30 | sigma at 8 / 32 / 512 | 0.03 / 0.02 / 0.01 | 0.06 / 0.04 / 0.02 | 0.11 / 0.08 / 0.04 | 0.17 / 0.11 / 0.05 | 0.33 [0.21, 0.44] / 0.23 / 0.10 |
| N10 | P0's share of C | 0.99 | 0.98 | 0.96 | 0.93 | 0.89 [0.85, 0.92] |
| N10 | sigma at 8 / 32 / 512 | 0.01 / 0.01 / 0.00 | 0.02 / 0.02 / 0.01 | 0.04 / 0.04 / 0.02 | 0.07 / 0.06 / 0.03 | 0.11 / 0.11 / 0.06 |

Figures: `results/fig_budget.png` (skill against Lab budget), `results/fig_worlds.png` (per hidden world),
`results/fig_curves.png` (validation curves of every kind of net).

### Reading

1. **Acceptance.** Pooled over the five horizons no arm passes sigma >= 0.15 at any Lab budget; with no Lab at all
   the interval of arm P reaches 0.165 (undecided). rho passes its bar (at most 0.7) trivially: the scripted S does
   nothing. By horizon, arm P passes at 16 ticks with 8 or 32 Lab episodes and at 8 ticks with 8; arm N30 passes at 16
   ticks with 8 (undecided with 32: 0.23 [0.14, 0.33]).
2. **The prior's width is a dial, up to a point.** A 10% neighbourhood is a round-5 exam (0.958). A 30% neighbourhood
   and the screened prior are the same to P0 (0.868, 0.863) once P0 has enough prior worlds; job 003's lower figure
   for N30 (0.787) was an artifact of 24-32 prior worlds.
3. **P0 pays for prior worlds, and the screen makes them dear.** Arm P: 16 prior worlds give 0.68 of C, 64 give
   0.82, 210 give 0.86. With round 5's pre-screen a screened world costs about 41,000 member-ticks to find, of which
   53% pass the exam's gate, so P0 on 210 worlds costs about 21.7 million member-ticks: 65,000 episodes with burn-in,
   against about 2,300 for the gliders pilot (written after the results; `summary.json: compute`).
4. **Lab data does what a hypothesis would.** A data-only learner needs about 290 Lab episodes for 90% of C and 85
   to match P0. A local ridge on 8 Lab episodes already has 0.637, 83% of C: the cheapest policy that needs no
   hypothesis, no simulator and no prior.
5. **Round 5's screen does not predict this.** Given the hidden state the weights matter enormously (a prior draw is
   worse than climatology, loss 1.5; a 10% error loses 0.32). A history-only net at the true weights gains only 0.105
   over P0. Over hidden worlds, sigma follows the state-given loss weakly (rank correlation 0.31 in arm P, 0.38 and
   0.52 in the N arms) and the world's activity (16-tick persistence error at the gate) strongly (0.83, 0.85, 0.67).
   Both correlations were computed after the results.
6. **What an agent would have to do to beat P0.** (a) Use the Lab: fine-tuning is worth +0.035 at 32 episodes and
   +0.074 at 512, with no hypothesis. (b) To do better than that with few Lab episodes it must identify the law:
   arm N10 shows that a net trained on worlds within 10% of the truth has 0.958 of C, so weights inferred to about
   10% and then simulated would recover most of the gap, where it is largest: at 8 to 16 ticks, with at most 32 Lab
   episodes. Nothing here shows that 240 weights can be inferred from that little block-view data; the one scripted
   attempt (33 summary statistics, amortised) recovered nothing. (c) Beyond C, 0.23 of the skill needs the hidden
   level-0 state: with the state in hand the weights must be right to about 6% for the simulator to match C, 10% to
   match P0 (interpolated between the 3%, 10% and 30% plug-ins, after the results).
7. **Actions.** The centres were chosen by the declared rule (largest effect of an aimed 200-nat command in the CPU
   probe: 9.9, 7.9 and 6.8 times the noise floor at 4 ticks; the other four shortlisted worlds 5.1, 3.6, 1.7, 1.6).
   In their neighbourhoods actions matter by criterion 4 (0.126 and 0.127 of the K-to-O range on items with a
   program). On screened-prior worlds it is undecided (0.085; 6 of 16 worlds at 0.10 or more). Blind commands of 200
   nats are invisible everywhere (0.012); aimed pushes cost the input-blind oracle 0.09 to 0.13, regional pushes of
   400 nats 0.15 to 0.24. For the screened prior this pilot is close to observation-only.
8. **Stationarity and seeds.** The tick alone carries at most 6e-05 of any hidden world's block-view variance.
   Seed-to-seed differences of the gaps are at most 0.006 in pooled skill; the intervals are world-to-world spread.

### What C is worth

Criterion 6 (converged if the held-out loss improved by less than 2% of its total gain over the last fifth of the
schedule) holds for 12 of 32 C nets in arm P of job 004 (4 of 32 in job 003), and C on 4,096 episodes is 0.034 ±
0.003 above C on 1,024. C is therefore a lower bound on what the family reaches at the true weights, in steps and in
data. P0 itself misses the criterion narrowly in arm P (late share 0.031 for both seeds); A, P0s, D(512), FT(512) and
the fine-tuned C meet it for most nets (`tables.py` prints the full table).

Job 005 (arm P, same hidden worlds, new items) adds a third point, C on 16,384 episodes: see the section at the end.

### Between jobs (arm P: same hidden and prior worlds; new items, Labs, secret and training seeds)

Every policy except C repeats within 0.004 of pooled skill between jobs 003 and 004 (P0 0.664 and 0.663, FT(512)
0.732 and 0.737, D(512) 0.710 and 0.710, ridge(8) 0.640 and 0.637, S(8) 0.664 and 0.664), P0 on 16 worlds within
0.017. C moved from 0.744 to 0.768 with 2.7 times the data and twice the steps at twice the batch, and with it P0's
share from 0.892 to 0.863. Arm N10 has the same hidden worlds in both jobs; arm N30 has one different (c1672-j1006
for c1672-j1003), because the gate's noise is keyed by a candidate's row and the larger candidate list moved the rows.

## Decisions taken, and why

- **Both priors, on one harness.** "Only the weights are hidden" in its pure form is the screened prior; a
  neighbourhood is "one world, several hidden draws". They turned out equivalent for P0 at 30% and trivial at 10%.
- **Block view only.** The object view is not examined: on the three centres the tracker holds 33% to 98% of the
  mass in 5 to 14 bodies that fuse or split 25 to 125 times per 100 ticks (round-5 screen), several identity changes
  per 16-tick item, and an object-view exam needs a second predictor family.
- **Exam-time gate at vp(16) >= 0.2.** The first version of DESIGN.md had 0.02; a CPU check before any GPU run
  showed nearly frozen worlds passing, where persistence is nearly the oracle. Of the 416 pool worlds 401 would
  pass at 0.02 and 226 pass at 0.2.

## What failed or fell short

- Request 001 was rejected for the length of its notes. Job 002 cost $1.92 for nothing: one dispatch per training
  step under the platform allocator. Fixed by 50 steps per dispatch (9.6 ms per step of the two shared nets instead
  of 70) and a presmoke that measures the speed and stops the job if the projection does not fit.
- C is not converged (above). The N arms of job 003 were not like for like with arm P.
- The amortised S is a weak script: 33 hand-made statistics of block-view windows. Its failure says little about what
  inference of the weights could do.
- The speed guard and deadlines were never exercised in the full passes (nothing was cut).
- Wind: on screened-prior worlds the channel is weak for the 200-nat programs; no other channel was tried. What would
  help, untested: (i) gate worlds on the input-blind loss as well, (ii) programs at the caps for the whole 16 ticks
  (the mix spends 200 to 400 nats in 4 ticks), (iii) an input that is not capped by the hidden mobility, for example
  a shift of a kind's affinity in a block, which enters the same noisy logits and can be charged in nats the same way.

## Rules and analyses written after seeing results

Gate threshold 0.2 (after a CPU check, before any GPU run). Section 5b (after job 002's speed, before any score).
Sections 5c and 5d (jobs 004 and 005, after job 003's and then 004's arm-P results). The by-horizon breakdown, the
rank correlations over worlds, the compute accounting, the weight-error equivalents and the between-job table are
descriptive and were written after job 003; the by-horizon numbers quoted are job 004's, which ran after that
breakdown existed. The criteria of DESIGN.md section 5 were not changed.

## Limits

One family (two kinds, 64 x 64), one predictor family, the block view, horizons up to 16 ticks. 16 hidden worlds of
one screen (prior seed 2027, enriched arm); the three centres are selected worlds. The N arms' twelve hidden worlds
sit in three centres, so their world-clustered intervals understate centre-to-centre spread (per-centre values in
`results/analysis.json: arms.N30.by_group`: P0's share 0.891, 0.838, 0.888). The public code standardisation of job
003 used a few hidden worlds' windows (fixed in 004). Hidden worlds are the same in 003, 004 and 005, so the three
jobs are repeats of the measurement, not of the choice of worlds.

## Files

| file | content |
|---|---|
| `DESIGN.md` | what is public, hidden and told; worlds; policies; criteria and thresholds; dated changes |
| `fx_lib.py`, `fx_net.py` | simulator runner, gate, program mix, vw World / Lab / exam builders, plug-ins, ridge; the net family |
| `run_fx.py`, `job.sh` | the GPU job (presmoke with shape and speed test, then the full pass) |
| `make_pool.py`, `results/pool.json` | the public pool of screened worlds and the centres |
| `make_summary.py`, `extras.py`, `make_claims.py`, `tables.py`, `figs.py`, `fetch.sh` | job outputs to `results/` |
| `results/analysis.json` | job 004, everything recomputed from per-item scores; `analysis_job003.json`, `analysis_job005.json` likewise |
| `results/summary.json` | every quoted number with its source; `results/job/` holds status, review and progress of every job |
| `PROGRESS.md` | log of the study |

Reproduce: `bash fetch.sh r6-foundryexam-004 /tmp/fx`; `python -B make_summary.py
/tmp/fx/jobs/r6-foundryexam-004/out/full --job r6-foundryexam-004`; `python -B extras.py`; `python -B
make_claims.py`; `python -B tables.py --other results/analysis_job003.json`; `python -B figs.py`. CPU test of the
job: `FX_SIZE=smoke OUT=/tmp/fxs bash job.sh` (about 6 minutes).
