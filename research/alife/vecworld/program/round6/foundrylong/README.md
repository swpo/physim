# foundrylong: the long-horizon hidden-weights exam (round 6)

**PILOT ONLY.** Every hidden world, Lab episode and item here is public pilot material (functions of public seeds, or
written to public outputs). Nothing of this study may ever be reused as an exam.

The pilot `../foundryexam` found one setting where the no-hypothesis recipe falls short of the true-weights
reference: the foundry's two-kind transport automaton with all 250 weights hidden, the screened prior (arm P), queries
at 16 ticks, at most 32 Lab episodes. This study asks, in two declared stages (`DECLARED.md`, committed before any
request; changes in `DEVIATIONS.md`), whether that is a real opening for science or an artefact of the recipe's
compute, and whether a hypothesis (the weights, fitted through the simulator) closes it.

Every number below is in `results/summary.json` with its source.

## Stage 1: is the gap only the recipe's compute? (job r6-foundrylong-001, 2.35 h, $4.92)

Same 16 hidden worlds as the pilot, new items, Labs and secret; episodes of 49 frames, queries at 8, 16 and 32 ticks.
P0 trained on 1,000 screened prior worlds (3 seeds; 790 new worlds from 15,040 pre-screened draws of prior seed 2028,
818 of 1,490 candidates passed the exam-time gate), a cross-validated fine-tune FT(N), D(N), the ridge, and the
reference C on up to 16,384 true-weight episodes per world.

| skill (K = 0, O = 1) | 8 ticks | 16 ticks | 32 ticks |
|---|---|---|---|
| C(16,384) | 0.677 | 0.581 | 0.508 |
| FT(32) (the null) | 0.571 | 0.455 | 0.357 |
| P0(1,000) | 0.540 | 0.421 | 0.321 |
| P0(210) / P0(64) | 0.481 / 0.410 | 0.354 / 0.273 | 0.226 / 0.160 |
| ridge Dr(32) | 0.487 | 0.352 | 0.254 |
| D(32) | 0.341 | 0.190 | 0.022 |

| criterion (declared) | number | verdict |
|---|---|---|
| S1: sigma(16 ticks, 32 Lab episodes) against the best of P0, FT, D, ridge | 0.218; p10 0.187 (min over leave-one-world-out 0.178); p90 0.253; median world 0.199 | **SURVIVES** |
| S1a: robust to one more step of compute | the step 210 -> 1,000 prior worlds took 0.114 of sigma; doubling P0's training steps 0.003; lower bound after one more step 0.06 | **"at this compute"** |
| S3: P0's curve over prior worlds | s0(16) = 0.531 / 0.390 / 0.276 at 64 / 210 / 1,000 worlds; last step 0.114 +- 0.020 | **still falling** at every horizon |
| S4: the reference's data curve | +0.048 of skill at 16 ticks for 4,096 -> 16,384 episodes | **not converged**: C is a lower bound |
| S5: actions | 0.115 at 16 ticks (p05 0.077); regional programs 0.21 | undecided |
| S2: training rule | P0(1,000) not trained by the 80% rule at 8 and 16 ticks (late gains about 1%; doubling the schedule gains 0.003 of skill); C mostly not trained (late gains about 4%); FT's cross-validation chose the grid's lowest rate in 122 of 144 cases | flags, not verdicts |

Reading. At five times the pilot's prior compute and with a tuned fine-tune, the generic recipe still leaves 0.22 of
the range at 16 ticks (0.30 at 32 ticks), with every world left out. But the gap is a value at this compute, not a
bound: P0 improves by about 0.11 of the range per fivefold step in prior worlds and shows no sign of flattening, while
more training steps on the same worlds give nothing. The recipe is limited by the number of distinct prior worlds it
sees, and C itself is not converged in data, so the gap would also widen with a better reference.

## Stage 2: can a hypothesis close it, and do experiments pay? (job r6-foundrylong-003, 1.88 h, $3.92)

Same 16 hidden worlds, new items, Labs and secret. Per world a Lab of 32 exam-mix episodes and a paired Lab of 32
designed episodes (same initial states and free-tick noise; 12.5 nats in every test tick, aimed and regional pushes on
the densest block). Generic candidates on each Lab: P0(1,000) (stage 1's parameters), FT(32) (cross-validated, rate
grid moved down, addendum 3), D(32), ridge. The hypothesis W: the 250 weights fitted by Adam through the simulator
on the Lab with the exam's own 16-tick score as the loss (32 prior worlds' weights prescreened, the best 4 refined for
143 steps, the count the speed guard allowed; addendum 4), then a nudged ensemble of the fitted world's own states
held to each item's 17 frames and simulated under its program. W+: the C recipe on 4,096 episodes simulated at the
fitted weights. (r6-foundrylong-002 stopped itself at its presmoke speed guard, which had counted compilation, $0.10.)

| skill at 16 ticks (8 / 32 in brackets) | mix Lab | designed Lab |
|---|---|---|
| C(16,384) | 0.593 (0.678 / 0.509) | |
| G* = FT(32) | 0.470 (0.579 / 0.364) | 0.461 |
| P0(1,000) | 0.434 | |
| W (fitted weights) | 0.404 (0.483 / 0.325) | 0.414 |
| W+ (simulate-to-train at the fit) | 0.326 | 0.356 |
| D(32) / ridge | 0.209 / 0.360 | 0.254 / 0.362 |
| W at the TRUE weights | 0.527 (0.603 / 0.477) | |
| W at another screened world's weights | -0.70 | |

| criterion (declared) | number | verdict |
|---|---|---|
| T1 science share against G*, 16 ticks | sigma_G 0.208; p10 0.178 (min over leave-one-out 0.170); p90 0.242 | **pass** (32 ticks: 0.286, pass; 8 ticks: 0.145, undecided) |
| T2 generic share | rho_G = 0.226 (p90 0.255) of P0's gap to C | **pass** (<= 0.7) |
| T3 solvable | W* = W; recovery of the G*-to-C gap -0.54; W beats G* at t = -1.86 (better in 5 of 16 worlds) | **fails** |
| T4 experiments pay | designed minus mix for W: +0.006 +- 0.018 of loss; for G*: -0.005 +- 0.002 | **fails** |
| T5 actions | 0.119 (p05 0.078); regional programs 0.20 | undecided |
| T6 not one horizon, not one world | T1 and T3 do not both hold at 8 and 32 ticks | fails |
| **stage 2** | neither the declared pass (T1-T6) nor the declared fail (T1 fails or T2 > 0.7) | **undecided** |

Reading (DECLARED.md section 3, row "T1 passes, T3 fails"). The gap is real against the best generic recipe on new
items and Labs: the tuned fine-tune leaves 0.21 of the range at 16 ticks and 0.29 at 32, with every world left out.
No scripted policy closes it. The weight inference is not the first limit: the same predictor at the TRUE weights
reaches only 0.527 at 16 ticks, below the reference net C (0.593; C better in 12 of 16 worlds, t = 3.2). The fitted
weights get W 90% of the way from a wrong world's weights to the true ones in skill (0.404 against 0.527), but they
are as far from the truth in parameter space as a prior draw (the law is sloppy): simulate-to-train at the fit (W+,
0.326) is far below the same recipe at the truth (C(4,096), 0.533 in stage 1). So the test is hard for two reasons
at once: a history of 192 block averages does not pin the fine state well enough for a nudged ensemble, and Lab data
pin the predictive part of the law only roughly. Designed experiments (full-budget, every-tick pushes) did not help
W or FT; they helped D (+0.026 +- 0.004 of loss at 16 ticks), the only policy that learns from the Lab alone.

Added after seeing the results (readings, not criteria): the "90% of the way" share and the parameter distance of
the fits (`w_info.json`: median RMS distance 1.48 prior SDs from the truth, as far as a random prior draw).

## What failed or is weak

- W's fits ran 143 Adam steps, not the declared 200 (the speed guard's choice, addendum 4); W is a lower bound of what
  this hypothesis reaches. One W per world and Lab is the better of two starts, from 4 refined of 32 prescreened.
- The first fit loss (one-tick forecasts) fitted the loss and not the law, and the first CPU fits used a fair score with
  a doubled spread term; both were found on CPU before any stage-2 job (addendum 3).
- Job 002's speed guard counted compilation as fit time and stopped the job ($0.10).
- P0 and C are not trained by the 80% rule (late gains 1-5%); C is not converged in data; every share is a value at
  this compute. P0's curve in prior worlds is nested in worlds available, not in what each net saw (review 001).
- S5 and T5 (actions) are undecided: inputs carry about 0.12 of the range, regional pushes 0.2.

## What it means for the lead's direction, and the next step

This is the first setting in the program where the generic recipes leave a gap that survives a tuned null, five times
the pilot's prior compute, new items and every world left out (0.21 of the range at 16 ticks, 0.29 at 32), AND where
the obvious scientific move (infer the law, then simulate) does not trivially win. It is not trivially easy. But it
is hard partly for a reason that is not science of the law: even with the true law in hand, a filter on the block
view loses to a net trained on 16,384 true-law episodes. An agent would have to (1) infer the predictive part of the
weights from Lab data (fit through the simulator against its own long-horizon score: box-feasible, about 40-50 min of
2 cores per 200 steps), and (2) build a state filter as good as C's, which in this study took simulate-to-train at
16,384 episodes per world (12.7 h of simulation on 2 cores): GPU-scale. And because P0 keeps improving with prior
worlds (0.11 of sigma per fivefold step, no flattening), the bar moves with the research compute an exam grants.

Next step (CPU, about a day of agent time, no GPU): replace the nudged ensemble with a better filter at known weights
(a particle filter with resampling on the block view, or a net trained on simulations at the fitted weights at
16,384 episodes) and measure W(true) against C on stage 2's public items; if W(true) reaches C, the setting is a test
of law inference and the exam profile can be priced (research budget in full episodes from `cpu_part.py`); if not,
the block view should be made less lossy (finer blocks) before this world family is used for rollouts. A GPU rerun
(about $5) is worth it only after that.

## Weight inference on CPU (before the stage-2 job; one public world)

`fl_w.py`: the hypothesis is the 250 numbers; the unobserved state is marginalised by an ensemble of the candidate
world's own states held to the observed block means at every observed tick (`nudge`); the fit loss is the exam's own
score on Lab episodes: from the assimilated ensemble at an anchor tick, a 16-tick forecast, fair energy score against
the observed frame (gradient through the forecast ticks).

- With the true weights this predictor reaches skill 0.85 / 0.78 / 0.70 at 8 / 16 / 32 ticks on seed2027-46 (8 items),
  above what C(16,384) reaches on average (0.68 / 0.58 / 0.51): the reference C is not the ceiling.
- Weights moved by 10% in prior units: 0.63 at 16 ticks; 30%: 0.37; another screened world's weights: -0.75.
- A fit with a one-tick loss reaches the truth's loss level but not the law that matters at long horizons (0.24 at 16
  ticks from a 30% start); the 16-tick loss takes it to 0.68 in 40 Adam steps on 8 episodes; from another screened
  world's weights to 0.37 in 60 steps, still improving.

## What an exam profile on this setting needs (CPU, `cpu_part.py`)

- Speed on 2 cores of this (shared, so lower bounds) container: 124 member-ticks per second in float64, 235 in float32
  (64 x 64, batch 32); a full 348-tick episode takes 2.8 s (float64) or 1.5 s (float32): about 1,290 or 2,430 full
  episodes per CPU-hour of 2 cores. The A100 runs 41,700 member-ticks per second in float64.
- An instance bundle (32 Lab episodes, 96 items with histories and programs, 12 replicate futures at the 3 queries,
  climatology) is 7.7 MB in float32 (5.1 MB compressed; block views barely compress); building it takes 112,000
  member-ticks, 15 min on 2 cores.
- Reference rows a box cannot make: P0 (64,000 prior episodes plus the screen of 15,040 draws: 50 h and 110 h of
  simulation on 2 cores, about 11 h of training per seed) and C (5.7 million member-ticks per world: 12.7 h, plus about
  2.7 h of training). They are precomputed on a GPU (0.15 h, 0.33 h, 0.04 h per world). FT's cross-validation (about
  22 min per world and seed), D, the ridge, O and K fit on a box. A W-type fit costs 12-15 s per Adam step on 2 cores
  (40-50 min for 200 steps): an agent with the simulator can afford weight inference on a box; it cannot afford the
  generic recipe's prior simulations.

## Files

`DECLARED.md` (the plan), `DEVIATIONS.md` (addenda 1-5), `PROGRESS.md` (log), `fl_lib.py` (training driver over the
pilot's code), `run_fl.py` + `job.sh` (stage 1), `fl_w.py` (weight inference, designed programs), `run_fl2.py` +
`job_s2.sh` (stage 2), `make_summary.py`, `make_summary2.py`, `make_final.py`, `cpu_part.py`, `w_cpu.py`, `make_sel.py`;
`inputs/` (the pilot's worlds, the code norm, the pre-screened draws of seed 2028, stage 1's public parameters);
`results/` (analyses, CPU measurements, `summary.json`).
