# Design (c) on fed vortices: a correct law too expensive at exam scale (round 6, designer compute_limit)

Design phase, 11 Nov 2026. CPU only (2.0 CPU-hours of simulation, S [cpu]; the three 128 px pools took 14 to 18
CPU-minutes each), no GPU, no model call. Everything measured is at tiny size with declared public parameters (eps
0.4, mut128 25; `PILOT_NEVER_REUSE_AS_EXAM`), on level 2 = (N, s_b), the vortex count and the share of kind b,
predicted from its own state: no hidden parameter, no net, no level-1 history. Sources: `S` =
`results/summary.json` [key] here, `V5` = `round5/vortexexam/results/summary.json`. Skill = 1 - L / L(K), fair
energy score, bootstrap se over truth members. "Estimate" marks what was not run.

**Forecast.** The design fails. Level 2 of this world adds up over space: a regression fitted on small-box runs
summed to exam size equals one fitted on exam-size runs (0.448 and 0.459 against 0.454) as long as a box holds
about five vortices; below that nothing repairs it, a law included. Where a law-shaped policy beats brute force, a
constant-drift control scores the same. I propose one $5 job with a stop rule, and a card quantity for finding
worlds where (c) can bind.

## 1. The exam

Round-5 pilot B (`round5/vortexexam`): fed vortices at 128 px, hidden (eps, mu, e), 404 ticks, 200-nat programs of
the public mix; item = level-1 history and program, answer = level 2 at 8, 16, 32 ticks. Public: the exact law
(`vxlib`), prior, mix, scales. Hidden: parameters, noise secret, items. The agent is told "your simulator is
exact; you cannot afford it at exam scale", and three numbers:

- **R**, research compute in exam-episode equivalents (128^2 px x 404 ticks at the native step);
- **r**, the largest box of any run as a share of the exam area, for simulations and for the Lab alike;
- **f**, compute per question as a share of simulating it (32 members x the horizon).

Decision 2 names R and f. I add r because an exam-size Lab is an exam-scale computer of the truth: two exam-size
episodes recalibrate a rescaled 64 px regression from 0.359 to 0.434 +- 0.015, against 0.454 for the exam-size
reference (S [transfer_128.skill.all]).

Zero point: r = 1, R >= 1,350 (P0's 1,024 design episodes and 320 dedicated ones; V5
[platform_job_B.value.member_ticks]), f = 1: every round-5 policy runs unchanged. Check: the zero arm re-scores
pilot B's stored design and items (`origin/gpu-jobs:jobs/r5-vortexexam-006/out`: design.npz, items.npz, exam.npz)
and must give P0 0.488, C 0.519, S(1) 0.517 and sigma 0.061 +- 0.048 within 2 se (V5
[headline.skill_B.value.net]). Settings: (r, R) = (1, 1,350), (1/4, 64), (1/16, 16); f = 0.05; Lab = 4
exam-episode equivalents, 800 nats per episode.

## 2. Mechanism, and what an experimenter must do

A correct-simulator policy can only run boxes smaller than the exam's. They differ in two ways.

1. Fluctuations. The spread of s_b falls as N^-1/2, that of N grows as N^1/2: a predictor trained on small boxes
   and rescaled is too wide (second table below).
2. Dynamics. Below about five vortices the box changes the law. At 32 px (2.3 vortices) density is 9.27 +- 0.16
   per 64^2 px against 7.42 to 7.97, the selection constant 0.143 +- 0.009 against 0.20 to 0.23, the sweep from
   s_b 0.25 to 0.75 takes 133 +- 5 ticks against 67 to 90 (S [finite_size]).

Science should pay because pooling boxes and scaling noise with N is a theory whose domain must be found.

What the experimenter must do: choose box sides. Run the Lab at two sides (at r = 1/4, for example 8 episodes at
64 px and 32 at 32 px: the 4 exam-episode equivalents, no nats) and compare density, sweep time and selection
constant per vortex; if they agree, pool; if not, the box is too small. Stirring does not help: the law's
constants fitted on branches without input, with blind and with aimed 200-nat programs have the same errors (b1:
0.062, 0.095, 0.054; c1: 0.058, 0.069, 0.077; S [screen.law_constants_from_branches_by_arm]).

The weakness: that experiment is a choice of two sizes, which a script can make, and passive data at two sizes
show the defect to any learner. Nothing here needs a designed input.

## 3. Candidates and the screen

The hidden part is what the affordable simulator leaves out. Four candidates, each run from four hidden 64 px
states with eight fresh-noise branches, without input and under an aimed 200-nat program. Round-5 screen: 0 = the
oracle, 1 = climatology; jackknife se over states (S [screen.none.screen], [screen.aimed.screen]). Terms: the law
is d s_b = b1 s (1 - s) + b2 (1 - 2 s) with N relaxing to a level proportional to area; its control has a constant
in place of s (1 - s); "rescaled" multiplies N by the area ratio; "pooled" sums k small-box runs into one
synthetic exam-size episode.

| affordable simulator run from the hidden state | cost f | no input | aimed input |
|---|---|---|---|
| A. box area: four 32 px tiles | 1 | 1.58 +- 0.51 | 1.84 +- 0.35 |
| A. one 32 px tile, rescaled | 1/4 | 3.55 +- 0.15 | 3.48 +- 0.38 |
| B. horizon: half of it | 1/2 | 0.56 +- 0.15 | 0.66 +- 0.10 |
| B. horizon: a quarter | 1/4 | 1.42 +- 0.09 | 1.38 +- 0.28 |
| C. time step x 2 | 1/2 | -0.03 +- 0.05 | -0.07 +- 0.04 |
| C. time step x 5 | 1/5 | -0.08 +- 0.04 | -0.01 +- 0.05 |
| D. ensemble: 3 members of 7 | 3/7 | -0.04 +- 0.05 | -0.03 +- 0.06 |
| level-2 law from (N, s_b) alone | 0 | 0.42 +- 0.06 | 0.57 +- 0.08 |
| its control without the selection term | 0 | 0.52 +- 0.08 | 0.69 +- 0.11 |
| generic level-2 regression | 0 | 0.38 +- 0.05 | 0.51 +- 0.09 |
| oracle ignoring the program | 1 | | 0.18 +- 0.05 |

C and D do not bind: a step five times longer loses nothing at level 2, and three members score as seven. B binds,
but a level-2 model at no cost beats half a simulation. A alone leaves the affordable simulator useless. No row
moves under designed input by more than its error. **Chosen: A**, as the cap r.

What recipes make of the cap, scored at 128 px (8 truth members x 24 items; the 32, 48, 64 px pools cost 5.5, 3.5,
5.0 exam episodes in px-ticks; S [transfer_128.skill.all]):

| policy | from 64 px (r = 1/4) | from 48 px | from 32 px (r = 1/16) |
|---|---|---|---|
| generic regression, rescaled | 0.359 +- 0.018 | 0.270 +- 0.016 | 0.146 +- 0.017 |
| generic regression on pooled boxes (4, 7, 16 summed) | 0.448 +- 0.023 | 0.459 +- 0.017 | 0.287 +- 0.024 |
| level-2 law with the N^-1/2 noise rule | 0.336 +- 0.024 | 0.275 +- 0.033 | -0.145 +- 0.047 |
| the law without the noise rule | 0.270 +- 0.015 | 0.160 +- 0.022 | -0.088 +- 0.031 |
| control: no selection term, same noise rule | 0.328 +- 0.022 | 0.248 +- 0.033 | -0.174 +- 0.052 |
| extrapolation in 1/area from 32 and 48 px: law, control, generic | | 0.370, 0.368, 0.243 | |
| fitted on 7 exam-size episodes: regression, law, control | 0.454 +- 0.021, 0.386, 0.388 | | |
| tick climatology of 7 exam-size episodes | 0.405 +- 0.044 | | |

| paired difference (S [transfer_128.paired_differences]) | value (z) |
|---|---|
| exam-size regression minus pooled regression, 64, 48, 32 px | +0.006 (0.5), -0.005 (-0.5), +0.167 (7.7) |
| law minus control, 64 px: all cells, kind-share cell | +0.008 (1.3), +0.042 (3.2) |
| law minus pooled regression, 64 px | -0.112 (-5.2) |
| mut128 100 (`results/mut100.json`, 4 truth members): pooled 64 px, exam-size, rescaled | 0.486, 0.483, 0.400 |

Pooling closes the gap from 64 and 48 px and not from 32 px. At mut128 100 a 64 px box has one mutation event per
80 ticks, as the 32 px box has above, and still pools: the 32 px box fails for its vortex count.

Budget curve at the 64 px stand-in (20 truth members, se 0.02 to 0.04; S [budget_curve.skill.all]):

| R, exam-size episodes | 1 | 2 | 4 | 8 | 15 |
|---|---|---|---|---|---|
| analog ensemble | 0.04 | 0.15 | 0.19 | 0.22 | 0.23 |
| regression on level 2 | 0.08 | 0.20 | 0.25 | 0.27 | 0.28 |
| regression on level-1 summaries | -0.02 | 0.18 | 0.25 | 0.29 | 0.30 |
| level-2 law | 0.16 | 0.21 | 0.24 | 0.25 | 0.26 |
| control: constant drift | 0.18 | 0.21 | 0.22 | 0.23 | 0.24 |

The law overtakes brute-force learning only at R = 1 (+0.126, z 6.3 over the analog; +0.086, z 5.8 over the
regression), where the control is level with it (-0.015, z -1.7); from R = 8 the regression is better (z -2.3,
-3.1). Fitted on exam-size data cut at tick 140, the law extrapolates worse than a constant drift (-0.08 against
0.14; S [horizon_transfer.skill.all]).

## 4. Reference policies (each a script)

| policy | what it does |
|---|---|
| K, O | as in round 5 |
| C | trained at the true parameters on exam-size simulations without limit |
| C_r | the same on pooled boxes of area r; C minus C_r is the scale gap without the parameter gap |
| P0(R, r) | prior simulations on boxes of area r, rescaled, and pooled |
| D(N) | the Lab alone, rescaled, and pooled |
| G1 | pooled P0 fine-tuned on pooled Lab episodes |
| G2 | a residual model fitted to pooled Lab data on top of pooled P0 |
| G3 | every coefficient linear in 1/area over two sides |
| G4 | (r = 1 only) spread recalibration on exam-size Lab episodes |
| S(N) | round 5's inference (`vxsbi`) on a pooled design, then training at the posterior |
| H | told the form (replicator-mutator drift with per-vortex constants, noise as N^-1/2, vortex number proportional to area, constants linear in 1/area), no value; splits its Lab ticks between two sides, tests convergence of density and sweep time, fits, extrapolates, iterates the law |
| H_ctl | H with a constant in place of the selection term (the round-5 checker's control) |
| H_ns | H without the noise rule |

G1 to G4 and the pooled variants of P0 and D are the generic recipes that sigma and rho are measured against.

## 5. Acceptance, declared now

At (r = 1/4, R = 64) and (r = 1/16, R = 16), truths as clusters:

| bar | threshold |
|---|---|
| 1. zero point | reproduces (section 1) |
| 2. the cap binds | C minus the best rescaled policy >= 0.15 of the K-to-C gap |
| 3. sigma_c | (L(G*) - L(C)) / (L(K) - L(C)) >= 0.15, G* the best of P0, D, G1 to G4, pooled variants included |
| 4. H solves it | (L(G*) - L(H)) / (L(G*) - L(C)) >= 0.5 |
| 5. H is a theory | H beats H_ctl at z >= 3 over truths on all cells; otherwise H is "few constants" |
| 6. rho | <= 0.7 with S on the pooled design |

Failure: at r = 1/4, G* within 0.15 of C (forecast: yes, pooled equals the reference); at r = 1/16, H misses bar 4
(forecast: yes, nothing from 32 px exceeds 0.29 against 0.45). I will conclude nothing about agents, other worlds
or level 1, and will not call bar 3 without bar 4 a science test: that is an exam no reference solves.

## 6. Sizes and cost

Stop-rule job, one, cap $5: pilot B's ten truths with their stored design and 480 items of 8 replicates (redone if
the items lack what a pooled predictor needs: 0.19 million member-ticks, about $0.7); new pooled designs of 256
parameter points x 4 boxes at 64 px and x 16 at 32 px; 4 pooled Lab and 16 pooled true-parameter episodes per
truth at both sides; 2 training seeds; ridge family with H, H_ctl, H_ns. That is 0.37 million exam-equivalent
member-ticks, $1.2 to 1.7 at $3.3 to 4.5 per million, about $2.5 with training on a 40 GB A100 (estimate; the 32
px rate is not measured); largest array 4,096 members x 32^2 x 5 fields. **Stop rule:** the study ends unless bars
3 and 4 both hold at one setting.

Full study, only then: ten new pilot truths, the zero arm (1.05 million member-ticks), both settings, nets, G1 to
G4: about 1.6 million member-ticks, $5 to 7, cap $12 (estimate).

Declared budgets (decision 2): R = 64 exam-episode equivalents (zero point 1,350) and f = 0.05, with r = 1/4.

## 7. Risks, their cheapest tests, and what would change the program

| risk | cheapest test |
|---|---|
| Pooling fails for nets on level-1 histories (lists do not add as (N, s_b) do) | the stop-rule job |
| Two parameter points only; eps, mu, e not varied | the stop-rule job, over pilot B's prior |
| The level-2 law is not one law: b1 is 0.20 to 0.23 on whole trajectories (S [finite_size]), 0.45 to 0.53 on branches from mid-sweep states (S [screen.law_constants_from_branches_by_arm]) | refit H's form on round 5's law runs, CPU |
| The budget unit is soft: a step five times longer costs nothing at level 2, so R = 64 buys 320 | declare the reference integrator; cap total compute |
| 8 truth members, 4 screen states, no programs in the transfer tables | the stop-rule job |

What would change the program: a world whose card shows a **pooling defect** (exam-size reference minus the pooled
small-box recipe; here 0.006 at 64 px, 0.167 at 32 px) of at least 0.15 at a box side where a level-k law fitted
on small boxes still holds. On fed vortices that window is empty. I recommend: put the pooling defect on the world
card (three pools; `analyse.py` [transfer_128]), keep R and f as declared numbers on every exam with r as a third,
and do not run (c) as its own exam on this world.

| file | what |
|---|---|
| `run_boxes.py` | pools of level-2 trajectories per box side (`vxlib.Runner` unchanged) |
| `screen_state.py` | the state-given screen: branches, tiles, longer time step, input arms |
| `analyse.py <scratch>` | `results/summary.json`: finite_size, budget_curve, horizon_transfer, transfer_128, screen, cpu |
| `check_mut100.py <scratch>` | `results/mut100.json` |
| `run_pools.sh`, `run_after*.sh`, `run_mut100.sh` | the order in which everything was run; the two "x 4" lines of `run_after.sh` stop at an assertion (250 / 4 native steps is not an integer), x 2 and x 5 replace them |
