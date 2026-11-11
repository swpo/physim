# dialsB: stage 0 of the membrane carrier, the CPU gate of study B

11 Nov 2026. Study B of `../PLAN.md` is an exam on phase-membrane cells whose hidden world holds a carrier species
under the public chemistry (`../sublevel_second`). Stage 0 decides, at no GPU cost, whether the 10-14 agent-hour
build of that exam is worth starting. `DECLARED.md` holds the sizes, policies and the rule, committed (9c00a2d29)
before any run; `DEVIATIONS.md` holds what could not be followed. Every hidden value here is a PILOT value, never
to be reused as an exam. `S` is `results/summary.json`: every number below with its job, file and key.

## Result

**By the declared three-way rule: CLOSE CALL. By the plan's rule read at the point estimates: NO-GO. The build is
not started.**

| condition (focus view, 8 seeds, 8-32 ticks pooled) | number | bar | at the point estimate | with the one-sided 90% bound |
|---|---|---|---|---|
| C1: the better generic recipe, main arm, all start states | closes 0.482 | <= 0.7 | holds | holds clearly |
| C2: the same with each seed's heaviest start state left out | closes 0.664 | <= 0.7 | holds | close |
| C3: the better generic recipe, control arm | closes 0.784 | >= 0.7 | holds | close |
| C4: the recipe told the form, main arm | closes 0.599 | >= 0.7 | **fails** | close |
| C5: the history-only stand-in's P0-to-C share, main arm | -0.087 | >= 0.10 | fails | fails clearly; **depends on A**, in no verdict |

Source: `S` [conditions], [verdict]; job `r6-dialsb-002`, `out/analysis.json`.

**A second finding, made after the results were read and in no verdict, changes what the first one means**
(section 3): at the designer's pilot centre (rho 0.02, D_X 0.5, a0 0.03) the hidden law is numerically unstable.
The carrier field becomes a growing checkerboard wherever there is cell catalyst, and the 32-tick resistance on
which the design rested is in large part that instability. The gate ran at the pilot centre in every seed,
because the declared scan could fix no range around it.

## 1. What ran

| item | value |
|---|---|
| job | `r6-dialsb-002`: one rented CPU machine (nebius, 16 vCPU, 62 GB, $0.54/h), 16:37:59 to 17:03:01 UTC, 25 min; exit 0; **$0.2204 billed** |
| earlier | `r6-dialsb-001`, the same code: stopped by its own speed guard after 5 min, $0.0432 (`nproc` answered 1; DEVIATIONS 3). `r6-dialsB-001`: never acknowledged by the runner, $0 (upper-case id; DEVIATIONS 1) |
| total | **$0.2636 billed** of the study's $5; 0.50 machine-hours; no GPU, no model call |
| code | commit 52ae6e403631, pinned by `ref` in both requests (`s0.py`, `job.sh`); the head of this folder differs only by the review's minor fixes |
| phases | presmoke (244 s; 682 member-ticks/s per process once compiled), speed guard (projected 2,071 s), scan V (53 points) and scan C (13 points), `ranges.json` hashed at 16:45:27 before the gate (SHA-256 f6784d4c...eefe2), the gate (16 processes, 861-974 s each), analysis; 1,432 s on the job's clock |
| the gate | state given, 64 px; seeds 31-38; main arm (carrier converted at cells) and control arm (converted everywhere), lam = 1; per seed and arm: 16 start states formed for 150 ticks, 16 Lab episodes, 24-32 test items (6-8 test states x 4 aimed pulses of 300 nats), 6 truths each; 4.79 million member-ticks, 4.1 CPU-hours |
| policies | pub (public law given the state), O (hidden law), the designer's gains G2 and G3, the adversary's A_act on its 39-point grid, G* (the best of the three by leave-one-episode-out on the Lab), H (told the form: 72 quasi-random points in lam, rho, D_X, a0, least squares on the Lab), a history-only ridge stand-in trained under the public law (P0s) and under the hidden law (Cs) |
| check | the gate's code path on the designer's pilot seed 5 gives his L(pub), L(pub0), L(O) to the last digit, on the rented machine too, and picks the adversary's filter (0.25, 1, 3, 2) (`S` [alignment_with_the_pilots]) |
| review | `jobs/r6-dialsb-002/review.md` (0 blocker, 0 major, 3 minor), read before the results; section 6 |

## 2. Reading the numbers

**Main arm.** G* is A_act in all eight seeds. It closes 0.88 of the public-to-oracle gap at 8 ticks, 0.77 at 16 and
0.25 at 32; the 32-tick horizon holds 0.59 of the pooled gap. The recipe told the form closes 0.96, 0.95 and 0.36.
Pooled, 0.48 against 0.60: told the form, the recipe gains 0.12 over the generic one and misses its bar. With each
seed's heaviest start state left out (it holds 0.26 to 0.64 of its seed's gap) G* closes 0.66, with a per-seed
median of 0.80 and five seeds of eight above 0.7; H closes 0.79.

**Control arm.** A_act closes 0.85 (0.90, 0.81, 0.85 at 8, 16, 32 ticks), H 0.96. G* closes 0.78 because the Lab
pick took G3 on seed 37, which closes 0.38 there against A_act's 0.75: C3 is close through the pick, not through
the filter.

**Second view.** The cell-resolved list gives the same picture as the focus view: main arm G* 0.50 and H 0.62
(0.67 and 0.82 with the heaviest left out), control arm 0.81 and 0.98. Scoring which cell was fed opens no gap
between the generic recipe and the told form.

**The stand-in** (five numbers of the last history frames, a ridge per horizon, 30 training futures per item).
Main arm: s = -0.087 over the declared mix (per-seed median -0.019, leave-one-seed-out -0.117 to -0.040); at 8 and
16 ticks 0.036 and 0.036; at 32 ticks the stand-in trained under the hidden law is worse than the one trained
under the public law and has 0.20 of the oracle's skill. Control arm: s = 0.035 (median 0.038, leave-one-seed-out
0.030 to 0.044), state-given gap 0.074, of which 0.37 is kept. Both are below 0.10. The plan forecast 0.05-0.10.

**Scans.** Scan V fixes the hidden set of the public law as dK, Dp, r, chi (one per family, by headroom).
Scan C fails for all three carrier parameters: at the pilot centre the gap without input is 0.130 and under blind
input 0.142, against thresholds of 0.03 and 0.05. By the declared rule the ranges are then the centre alone, so
all eight seeds have the designer's and the adversary's hidden values, and "truths off the grid" holds only in
that H's design does not contain the centre.

## 3. After the fact: the hidden law at the pilot centre is numerically unstable

Written after the job's results were read; `diag_grid.py`, `results/diag_grid.json`, about a CPU-minute here; in
no verdict.

1. **What the declared scan showed.** The gap without input is 0.005-0.006 for D_X from 0.05 to 0.35 and 0.130 at
   D_X = 0.5; it is -0.002 and -0.004 at rho = 0.005 and 0.01, 0.130 at 0.02, and at rho = 0.04 and 0.08 no member
   of 16 has a cell after formation (scan C table below).
2. **Why.** `sublevel.py` steps the carrier X by explicit Euler with the 5-point Laplacian at dt = 0.5. A
   checkerboard pattern in X is multiplied at each native step by 1 - 8 dt D_X - dt rho K / 0.25. At D_X = 0.5 that
   is -(1 + 0.5 rho K / 0.25): its modulus exceeds 1 wherever there is catalyst, for every rho above 0 (1.0108
   inside a cell at rho = 0.02; a tick is 20 native steps). D_X = 0.5 is the edge of stability for diffusion
   alone; with conversion at cells it is past the edge.
3. **Measured.** Without any input, two members: at the pilot centre X is 99.5% checkerboard, of amplitude 0.49
   at tick 150 (where every item starts) and 34 at tick 182, and the substrate is clipped at zero. At D_X = 0.35,
   or at rho = 0.01, or with conversion everywhere (the control arm), X is smooth (largest value 0.011-0.013,
   grid-scale part 0.0001). At rho = 0.04 the fields are not finite by tick 150. In the gate's own start states
   (seeds 31 and 36, main arm, 16 members each) the checkerboard amplitude at tick 150 runs from 0.0001 in members
   without cells to 1.6-1.8, median 0.13 and 0.08; at tick 182 it reaches 155 and 32, the substrate is clipped at
   zero in 5 and 2 members, and one member is not finite. A member whose fields are not finite reads as an empty
   cell list at level 1, without an error.
4. **What follows.**
   - The main-arm truths at 32 ticks are in large part a numerical blow-up whose size differs by orders of
     magnitude between start states. That fits the heaviest start state, the 32-tick gap that no generic recipe
     closes, and a told-form recipe that cannot close it either: its D_X lies below 0.5. In the designer's own
     check H's grid held D_X = 0.5 exactly; there it closed 0.91 of the 32-tick gap (the adversary's rerun, seed 6).
   - The designer's rows for conversion at cells (`../sublevel_second/DESIGN.md`, table 3b) and all four of the
     adversary's seeds were run at this point. No run exists of conversion at cells against generic recipes at
     stable values.
   - Not affected, as far as measured: the control arm within 32 ticks, and scan C's rows at D_X up to 0.35, where
     the state-given gap under aimed input is 0.165-0.179 (0.364 at the centre).
   - Not measured: how much of the main arm's gap at 16 and 32 ticks a stable step would leave.

## 4. What the outcome means in the plan's table

The plan's row is "B: stage 0 fails | A filter on the command repairs the carrier except in rare start states. B
is not built, at no GPU cost. With A confirmed, defects that act on the response to an input are closed on two
worlds (on the second by a state-given CPU check only); what stays open is a defect whose correction needs hidden
state that only the history reveals." Stage 0 did not pass, so this row applies and B is not built. Three
qualifications:

- By the three-way reading nothing fails clearly: the literal failure is C4, by 0.10, with a bound that
  straddles the bar.
- The row's words need one correction. The "rare start states" are the numerical blow-up of section 3. Where
  the instability is absent or small, the filter closes 0.85 (control arm) and 0.77-0.88 (main arm, 8 and 16 ticks).
- The row "main arm and control arm both resist generic repair" does not apply: the filter closes 0.85 in the
  control arm.

C5 points the same way as the plan's forecast for stage 1 (a history-only predictor keeps little): 0.035 in the
arm without the instability. It is reported only; whether a stand-in may gate is study A's question.

## 5. What a build would need; the next step and its cost

**Not now.** B as designed should not be built: at its pilot centre the hidden world is not a valid simulation.

**If the carrier is to be tested rather than closed**, one more CPU job answers it:
1. a stable carrier: D_X at most 0.35 at dt = 0.5 (admissible in scan C), or a sub-stepped or implicit step for X,
   and a stability check (the grid-scale part of X) on the world card;
2. scan C again around a stable centre: its rho and a0 rows were taken at D_X = 0.5 and say nothing about stable
   worlds;
3. the same gate, same conditions and thresholds, declared before the run.
Cost: this study's job again, about 25 minutes of a 16-vCPU machine, about $0.25 (cap $2.50), and 1.5-2
agent-hours; `s0.py` needs only the centre as an argument. Present evidence forecasts generic repair at or above
0.7 there (the filter closes 0.85 in the control arm and 0.77-0.88 at 8 and 16 ticks in the main arm), a NO-GO
without the close call. That is a forecast, not a measurement.

**If a stable carrier ever passes stage 0**, the build is the plan's list (the exam, a net family whose training
programs include filtered commands, inference in 17 dimensions, R, F, A_act, H, H_mix, the control arm; 10-14
agent-hours; stage 1 about $2-3, stage 2 $4-6), with this from stage 0:
- the hidden set dK, Dp, r, chi with the boxes of scan V. F, a, b, dL and th have no viable box of +-10% at 64 px:
  the viable region of the public law is narrow;
- A_act in the null: it was the better generic recipe in 15 of 16 seed-arms;
- every bar read per horizon and with the heaviest start state left out; non-finite fields as a declared failure
  of a truth, since level 1 hides them;
- a history-only share measured before any net: the stand-in gives 0.035 where the world is stable.

## 6. What failed, and limits

- **The gate did not test the carrier mechanism at 32 ticks**, for the reason of section 3, and it has no fresh
  hidden values: scan C failed by its rule and every seed sits at the pilot centre.
- Two requests cost time: an upper-case job id the runner ignores, and a processor count read after
  OMP_NUM_THREADS was set (DEVIATIONS 1, 3).
- C3 depends on the Lab pick: the filter alone closes 0.85, G* 0.78.
- The channel-noise keys are the same in every seed and arm (they come from the world seed and a call counter,
  as in `gvh.py`). Seeds differ in start states and programs. The bounds treat seeds as independent.
- The three-way reading, the second view, H's search, the stand-in's features and the scans' thresholds are this
  study's choices, all fixed before any run (DECLARED 2). Section 3 and `diag_grid.py` came after the results.
- H is one script. A better search might pass 0.7 at a stable truth; at an unstable one the question is moot.
- State given, 64 px, scripts only: nothing here says what a history-only net or an agent would do.
- From the review, not fixed in the run: one core per process was not enforced (the job finished in 24 minutes
  of a 3-hour limit), a gate process saves nothing until it ends, and the per-horizon medians and ranges were
  missing from `analysis.json` (now in `results/per_horizon.json`, made by `horizons.py` from the job's scores;
  its pooled values equal the job's). Scan V's file names differed by case only (DK / dK); the copies here carry an
  index.

## 7. Tables

All tables, including the cell-resolved view and the control arm's stand-in: `results/tables.md` (printed by
`tables.py` from the job's files). G* = the better generic recipe. Shares are of the public-to-oracle gap.

### Per seed, main arm (focus view, 8-32 ticks pooled)

| seed | rho, D_X, a0 (pilot) | items | heaviest state's share of the gap | G* is | G2 | G3 | A_act | G* | G*, heaviest out | H | H, heaviest out |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | 0.0200, 0.500, 0.0300 | 28 | 0.51 | A_act | +0.18 | +0.16 | +0.23 | +0.23 | +0.38 | +0.28 | +0.48 |
| 32 | 0.0200, 0.500, 0.0300 | 32 | 0.49 | A_act | +0.21 | +0.16 | +0.50 | +0.50 | +0.87 | +0.53 | +0.96 |
| 33 | 0.0200, 0.500, 0.0300 | 24 | 0.60 | A_act | +0.06 | +0.07 | +0.51 | +0.51 | +0.98 | +0.48 | +0.95 |
| 34 | 0.0200, 0.500, 0.0300 | 32 | 0.30 | A_act | +0.50 | +0.30 | +0.54 | +0.54 | +0.69 | +0.67 | +0.89 |
| 35 | 0.0200, 0.500, 0.0300 | 32 | 0.29 | A_act | +0.24 | +0.21 | +0.29 | +0.29 | +0.36 | +0.60 | +0.50 |
| 36 | 0.0200, 0.500, 0.0300 | 24 | 0.51 | A_act | +0.38 | -0.30 | +0.90 | +0.90 | +0.80 | +0.98 | +0.97 |
| 37 | 0.0200, 0.500, 0.0300 | 28 | 0.26 | A_act | +0.59 | +0.32 | +0.78 | +0.78 | +0.81 | +0.96 | +0.96 |
| 38 | 0.0200, 0.500, 0.0300 | 28 | 0.64 | A_act | +0.23 | +0.24 | +0.37 | +0.37 | +0.89 | +0.42 | +1.03 |
| **pooled** | | | | | **+0.29** | **+0.17** | **+0.48** | **+0.48** | **+0.66** | **+0.60** | **+0.79** |
| median of seeds | | | | | +0.24 | +0.19 | +0.51 | +0.51 | +0.80 | +0.57 | +0.96 |
| leave-one-seed-out range | | | | | +0.25 to +0.32 | +0.15 to +0.21 | +0.44 to +0.53 | +0.44 to +0.53 | +0.63 to +0.77 | +0.55 to +0.64 | +0.76 to +0.89 |
| bootstrap over seeds, 5%-95% | | | | | +0.20 to +0.38 | +0.08 to +0.24 | +0.38 to +0.62 | +0.38 to +0.62 | +0.52 to +0.82 | +0.48 to +0.72 | +0.65 to +0.95 |

### Per horizon, main arm (focus view, pooled over seeds)

| view | start states | policy | 4 ticks | 8 | 16 | 32 | pooled 8-32 |
|---|---|---|---|---|---|---|---|
| focus | all | G2 | +0.97 | +0.88 | +0.76 | -0.07 | +0.29 |
| focus | all | G3 | +0.91 | +0.90 | +0.70 | -0.26 | +0.17 |
| focus | all | A_act | +0.91 | +0.88 | +0.77 | +0.25 | +0.48 |
| focus | all | G* | +0.91 | +0.88 | +0.77 | +0.25 | +0.48 |
| focus | all | H | +0.94 | +0.96 | +0.95 | +0.36 | +0.60 |
| focus | heaviest out | G2 | +0.97 | +0.89 | +0.77 | -0.16 | +0.44 |
| focus | heaviest out | G3 | +0.90 | +0.90 | +0.70 | -0.52 | +0.28 |
| focus | heaviest out | A_act | +0.90 | +0.87 | +0.77 | +0.43 | +0.66 |
| focus | heaviest out | G* | +0.90 | +0.87 | +0.77 | +0.43 | +0.66 |
| focus | heaviest out | H | +0.94 | +0.95 | +0.94 | +0.55 | +0.79 |

Share of the pooled gap at 8, 16, 32 ticks (focus view): 0.18, 0.22, 0.59.

### Per seed and horizon, main arm (focus view, all start states)

| seed | G* 8 | G* 16 | G* 32 | A_act 8 | A_act 16 | A_act 32 | H 8 | H 16 | H 32 |
|---|---|---|---|---|---|---|---|---|---|
| 31 | +0.89 | +0.76 | +0.03 | +0.89 | +0.76 | +0.03 | +0.89 | +0.97 | +0.06 |
| 32 | +0.95 | +0.85 | +0.35 | +0.95 | +0.85 | +0.35 | +1.00 | +0.93 | +0.36 |
| 33 | +0.94 | +0.99 | +0.15 | +0.94 | +0.99 | +0.15 | +1.00 | +0.97 | +0.08 |
| 34 | +0.82 | +0.55 | +0.33 | +0.82 | +0.55 | +0.33 | +1.01 | +1.00 | +0.16 |
| 35 | +0.88 | +0.85 | +0.04 | +0.88 | +0.85 | +0.04 | +0.78 | +0.80 | +0.52 |
| 36 | +0.97 | +0.73 | +0.94 | +0.97 | +0.73 | +0.94 | +1.01 | +0.99 | +0.97 |
| 37 | +0.83 | +0.70 | +0.86 | +0.83 | +0.70 | +0.86 | +0.97 | +0.96 | +0.96 |
| 38 | +0.91 | +0.90 | +0.15 | +0.91 | +0.90 | +0.15 | +1.00 | +1.02 | +0.18 |

### Per seed, control arm (focus view, 8-32 ticks pooled)

| seed | rho, D_X, a0 (pilot) | items | heaviest state's share of the gap | G* is | G2 | G3 | A_act | G* | G*, heaviest out | H | H, heaviest out |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | 0.0200, 0.500, 0.0300 | 28 | 0.22 | A_act | +0.49 | +0.40 | +0.81 | +0.81 | +0.83 | +0.96 | +0.97 |
| 32 | 0.0200, 0.500, 0.0300 | 32 | 0.26 | A_act | +0.44 | +0.44 | +0.87 | +0.87 | +0.82 | +0.96 | +0.94 |
| 33 | 0.0200, 0.500, 0.0300 | 24 | 0.23 | A_act | +0.66 | +0.05 | +0.95 | +0.95 | +0.97 | +0.96 | +0.97 |
| 34 | 0.0200, 0.500, 0.0300 | 32 | 0.25 | A_act | +0.63 | +0.48 | +0.87 | +0.87 | +0.88 | +0.85 | +0.98 |
| 35 | 0.0200, 0.500, 0.0300 | 32 | 0.22 | A_act | +0.71 | +0.70 | +0.82 | +0.82 | +0.79 | +0.97 | +0.99 |
| 36 | 0.0200, 0.500, 0.0300 | 24 | 0.50 | A_act | +0.49 | +0.09 | +0.91 | +0.91 | +0.83 | +0.97 | +0.93 |
| 37 | 0.0200, 0.500, 0.0300 | 28 | 0.20 | G3 | +0.61 | +0.38 | +0.75 | +0.38 | +0.41 | +0.98 | +0.96 |
| 38 | 0.0200, 0.500, 0.0300 | 28 | 0.35 | A_act | +0.54 | +0.51 | +0.88 | +0.88 | +0.87 | +1.03 | +1.10 |
| **pooled** | | | | | **+0.58** | **+0.38** | **+0.85** | **+0.78** | **+0.77** | **+0.96** | **+0.98** |
| median of seeds | | | | | +0.58 | +0.42 | +0.87 | +0.87 | +0.83 | +0.97 | +0.97 |
| leave-one-seed-out range | | | | | +0.56 to +0.60 | +0.34 to +0.43 | +0.84 to +0.88 | +0.76 to +0.88 | +0.74 to +0.86 | +0.95 to +0.97 | +0.96 to +0.98 |
| bootstrap over seeds, 5%-95% | | | | | +0.53 to +0.63 | +0.26 to +0.49 | +0.81 to +0.89 | +0.65 to +0.89 | +0.64 to +0.88 | +0.92 to +0.98 | +0.96 to +1.00 |

### Per horizon, control arm (focus view, pooled over seeds)

| view | start states | policy | 4 ticks | 8 | 16 | 32 | pooled 8-32 |
|---|---|---|---|---|---|---|---|
| focus | all | G2 | +0.98 | +0.88 | +0.72 | +0.01 | +0.58 |
| focus | all | G3 | +0.91 | +0.91 | +0.67 | -0.66 | +0.38 |
| focus | all | A_act | +0.93 | +0.90 | +0.81 | +0.85 | +0.85 |
| focus | all | G* | +0.94 | +0.92 | +0.83 | +0.55 | +0.78 |
| focus | all | H | +0.96 | +0.98 | +0.95 | +0.93 | +0.96 |
| focus | heaviest out | G2 | +0.99 | +0.89 | +0.72 | -0.27 | +0.62 |
| focus | heaviest out | G3 | +0.92 | +0.91 | +0.66 | -1.16 | +0.45 |
| focus | heaviest out | A_act | +0.93 | +0.91 | +0.81 | +0.75 | +0.84 |
| focus | heaviest out | G* | +0.94 | +0.93 | +0.83 | +0.23 | +0.77 |
| focus | heaviest out | H | +0.96 | +0.98 | +0.95 | +1.02 | +0.98 |

Share of the pooled gap at 8, 16, 32 ticks (focus view): 0.34, 0.38, 0.28.

### Per seed and horizon, control arm (focus view, all start states)

| seed | G* 8 | G* 16 | G* 32 | A_act 8 | A_act 16 | A_act 32 | H 8 | H 16 | H 32 |
|---|---|---|---|---|---|---|---|---|---|
| 31 | +0.90 | +0.78 | +0.75 | +0.90 | +0.78 | +0.75 | +0.89 | +0.97 | +1.02 |
| 32 | +0.94 | +0.84 | +0.86 | +0.94 | +0.84 | +0.86 | +1.00 | +0.87 | +1.00 |
| 33 | +0.93 | +0.98 | +0.90 | +0.93 | +0.98 | +0.90 | +1.01 | +0.97 | +0.71 |
| 34 | +0.92 | +0.85 | +0.82 | +0.92 | +0.85 | +0.82 | +0.98 | +0.97 | +0.36 |
| 35 | +0.89 | +0.89 | +0.16 | +0.89 | +0.89 | +0.16 | +0.95 | +0.99 | +0.93 |
| 36 | +0.95 | +0.69 | +0.97 | +0.95 | +0.69 | +0.97 | +0.99 | +0.88 | +0.99 |
| 37 | +0.95 | +0.76 | -2.53 | +0.85 | +0.65 | +0.84 | +0.96 | +0.94 | +1.17 |
| 38 | +0.90 | +0.86 | +0.88 | +0.90 | +0.86 | +0.88 | +1.02 | +1.02 | +1.06 |

### The stand-in, main arm

| items | share s = (L(P0s) - L(Cs)) / (L(K) - L(Cs)) | state-given gap | kept | skill of Cs, of the oracle's |
|---|---|---|---|---|
| declared mix, 8-32 ticks | -0.087 | 0.153 | -0.36 | 0.628 |
| aimed only | -0.075 | 0.185 | -0.26 | 0.625 |
| blind only | -0.160 | 0.048 | -2.02 | 0.611 |
| none only | -0.093 | 0.047 | -1.32 | 0.664 |
| mix, 8 ticks | 0.036 | 0.071 | +0.42 | 0.834 |
| mix, 16 ticks | 0.036 | 0.093 | +0.30 | 0.772 |
| mix, 32 ticks | -1.255 | 0.325 | -0.79 | 0.204 |

s per seed: -0.015, -0.023, -0.208, -0.015, 0.043, -1.199, 0.045, -0.160; median -0.019; leave-one-seed-out -0.117 to -0.040; bootstrap over seeds 5%-95% -0.217 to -0.008.

### Scan C

| parameter | value | gap without input | gap, blind input | gap, aimed input | states with a focus cell | admissible |
|---|---|---|---|---|---|---|
| DX | 0.05 | 0.005 | 0.009 | 0.165 | 15 | yes |
| DX | 0.1 | 0.006 | 0.008 | 0.167 | 15 | yes |
| DX | 0.2 | 0.006 | 0.008 | 0.171 | 15 | yes |
| DX | 0.35 | 0.006 | 0.009 | 0.179 | 15 | yes |
| DX | 0.5 | 0.130 | 0.142 | 0.364 | 15 | no |
| a0 | 0.02 | 0.297 | 0.304 | 0.495 | 15 | no |
| a0 | 0.025 | 0.213 | 0.223 | 0.420 | 15 | no |
| a0 | 0.03 | 0.130 | 0.142 | 0.364 | 15 | no |
| a0 | 0.04 | 0.107 | 0.117 | 0.228 | 15 | no |
| a0 | 0.05 | 0.093 | 0.101 | 0.219 | 15 | no |
| rho | 0.005 | -0.002 | 0.025 | 0.411 | 15 | yes |
| rho | 0.01 | -0.004 | 0.017 | 0.305 | 15 | yes |
| rho | 0.02 | 0.130 | 0.142 | 0.364 | 15 | no |
| rho | 0.04 | n/a | n/a | n/a | 0 | no |
| rho | 0.08 | n/a | n/a | n/a | 0 | no |

Ranges: DX 0.5 to 0.5 (scan failed: the centre alone); a0 0.03 to 0.03 (scan failed: the centre alone); rho 0.02 to 0.02 (scan failed: the centre alone).

### Scan V

| parameter | family | viable at 0.8, 0.9, 1.1, 1.2 x default | headroom at those | box (x default) | headroom (smaller edge) | eligible |
|---|---|---|---|---|---|---|
| DK | transport | yes, yes, yes, yes | -0.003, -0.003, 0.007, 0.005 | 0.8 to 1.2 | -0.003 | no |
| DL | transport | yes, yes, yes, yes | 0.013, 0.006, 0.005, 0.009 | 0.8 to 1.2 | 0.009 | no |
| DS | transport | no, yes, yes, yes | 0.364, 0.046, 0.066, 0.230 | 0.9 to 1.2 | 0.046 | yes |
| Dp | transport | yes, yes, yes, yes | 0.438, 0.150, 0.098, 0.354 | 0.8 to 1.2 | 0.354 | yes |
| F | metabolism | no, no, yes, no | n/a, 0.360, 0.964, n/a | none | n/a | no |
| a | phase | yes, yes, no, no | 0.220, 0.014, 0.124, n/a | none | n/a | no |
| b | metabolism | no, yes, no, no | n/a, 0.273, 0.395, n/a | none | n/a | no |
| c | metabolism | yes, yes, yes, no | 0.200, 0.034, 0.028, 0.162 | 0.8 to 1.1 | 0.028 | yes |
| chi | link | yes, yes, yes, yes | 0.112, 0.026, 0.017, 0.066 | 0.8 to 1.2 | 0.066 | yes |
| dK | decay | yes, yes, yes, yes | 1.106, 0.286, 0.461, 0.821 | 0.8 to 1.2 | 0.821 | yes |
| dL | decay | no, yes, no, no | n/a, 0.737, 0.575, n/a | none | n/a | no |
| r | phase | yes, yes, yes, yes | 0.292, 0.083, 0.078, 0.161 | 0.8 to 1.2 | 0.161 | yes |
| th | phase | no, no, no, no | n/a, 0.851, 0.779, n/a | none | n/a | no |

Noise floor (the default law against itself): 0.003 +- 0.007. Hidden set: dK in 0.016 to 0.024 (decay, headroom 0.821), Dp in 0.08 to 0.12 (transport, headroom 0.354), r in 0.16 to 0.24 (phase, headroom 0.161), chi in 1.6 to 2.4 (link, headroom 0.066).

## 8. Files

| file | what |
|---|---|
| `DECLARED.md`, `DEVIATIONS.md`, `PROGRESS.md` | the rule before any run; what could not be followed; the log |
| `s0.py` | scans, ranges with hash, the gate per seed and arm, analysis, presmoke, alignment check |
| `job.sh` | the job: presmoke, speed guard, phases with a deadline |
| `make_summary.py`, `tables.py`, `horizons.py` | `results/summary.json`, `results/tables.md`, `results/per_horizon.json` from the job's published files |
| `diag_grid.py` | the after-the-fact diagnostic of section 3 -> `results/diag_grid.json` |
| `results/job/` | the job's JSON outputs (`analysis.json`, `ranges.json` and its hash, `gate/`, `scan/`, `align.json`, `status.json`); the per-item scores (npz) stay on `origin/gpu-jobs:jobs/r6-dialsb-002/out/gate/` |

To reproduce: `git archive origin/gpu-jobs jobs/r6-dialsb-002 jobs/r6-dialsb-001 | tar -x -C SCRATCH`, then
`make_summary.py SCRATCH/jobs/r6-dialsb-002 SCRATCH/jobs/r6-dialsb-001`, `horizons.py SCRATCH/jobs/r6-dialsb-002/out/gate
SCRATCH/jobs/r6-dialsb-002/out/analysis.json`, `tables.py`. The job itself: `S0_SIZE=full S0_NPROC=16 bash job.sh` at
commit 52ae6e403631 (the vw1 venv's python; jax 0.12.0.1, numpy 2.5.4, scipy 1.18.1).
