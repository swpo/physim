# Design (b) on gliders: an incomplete public law, dial eta (round 6, designer defect_gliders)

Design phase, 11 Nov 2026. CPU only: about 23,000 member-ticks in about 60 CPU-minutes, no GPU, no model call.
Everything measured here is at tiny size (6 hidden states x 5 replicate futures, block view) on public pilot seeds
that must never serve as an exam. Files are in this folder; `results/summary.json` collects every number with
its source. "Estimate" marks what was not run.

**Forecast.** The best candidate beats the public-law policy where it acts, and a generic residual
fitted on one or two Lab episodes repairs it. I expect this design to fail the bars against generic recipes, and
I propose a $5-capped first job that stops the study if the forecast holds.

## 1. The exam

The round-5 ladder exam, cell "4 hidden parameters" (`round5/ladder`): Flow-Lenia gliders with the wind channel,
hidden lR, dm_00, ls_00, lh from the public prior, level-1 block view observed and predicted (population view as
a second cell), history items of 16 input-free ticks, a program from the public mix (none, blind, aimed 200 nats,
regional 300 nats; caps 100 nats per tick, 400 per episode), horizons 1 to 16 ticks. Public: `gworld.tick`, the
coarse-grainings, prior, mix, scales, simulator. Hidden in addition: one term of the law, **stress conversion**
(XW): where the wind magnitude |E| exceeds a threshold, channel 0 turns into channel 1 at rate eta x 0.09 x s per
unit time, s rising smoothly from 0 at |E| = W0 to 1 at W0 + DW (pilot: 0.12, 0.05; per hidden world from a
designer's box). The agent is told: "the simulator may lack mechanisms of the world; which, where and how
strong is not said; there may be none." Dial: eta in {0, 1, 2, 4} (30% of channel 0 converted per tick at full
trigger for eta = 1, 76% for eta = 4, where it saturates).

Zero point: at eta = 0 the hidden tick is `gworld.tick` itself. Checked now: with traced zero strengths `dlaw.tick`
is bitwise equal to `gworld.tick` over 2 members x 8 ticks with inputs above the trigger (`results/check_zero.json`
[bitwise_equal_to_gworld]). In the study the eta = 0 arm reruns the ladder's eight pilot truths and must
reproduce sigma = 0.018 +- 0.004 (block) within 2 SE; the comparison is statistical, since GPU runs are not
bit-deterministic. The baseline does not depend on the item class (sigma 0.013 to 0.020 in each of the four;
`results/baseline_by_class.json`, recomputed from the ladder's saved scores), so the reading "classes aimed and
regional only" has the same zero point.

## 2. Mechanism, and what an experimenter must do

Why P0 should fail: every public-law simulation conserves the two channel masses separately, so P0 has never seen
a push change what matter is. Half the mix triggers the term (peak field 0.228 for the aimed push, 0.153 for the
regional; `results/probe.json`). Without inputs the term is silent: the background wind peaked at 0.119 in 400
ticks against a threshold of 0.12 (one of six burn-ins saw a weak crossing), and the scored input-free futures
are bit-identical under the two laws.

What exposes it, all at level 1: (1) bookkeeping: the sum over blocks of the channel-0 mean is constant in every
input-free episode and falls after a push while total mass stays (to 5e-13); (2) a dose-response series on the
2 x 2 blocks at the heaviest group, each arm at most 200 nats (`results/dose_XW.json`, eta = 4):

| nats per tick (peak field) | 12.5 (0.114) | 25 (0.161) | 50 (0.228) | 100 (0.322) |
|---|---|---|---|---|
| channel 0 lost in the pushed blocks, 1 tick | 0.01 | 0.17 | 0.47 | 0.74 |
| the same, 2 ticks | 0.03 | 0.31 | 0.64 | 0.93 |

(SE over 6 states 0.01 to 0.05.) Eight arms of about 6 ticks give threshold, ramp and rate; (3) controls on empty and on
channel-1 blocks; (4) the term is written into the simulator and checked on held-out mix episodes.

## 3. Candidates and three screens

Screen 1 is round 5's: the public-law simulator from the hidden state against the oracle, as a share of
climatology-to-oracle, with common noise so that an inert term scores exactly zero (`screen.py`). Horizons 1 to 8,
jackknife SE over states.

| hidden part (kind) | no input | mix aimed | mix regional | designed, 200 nats | history-only share (aimed / regional) |
|---|---|---|---|---|---|
| G gust: wind gain doubles above the threshold (flow term) | 0.000 | 0.040 +- 0.009 | 0.032 +- 0.004 | 0.063 +- 0.014 | not run |
| XW stress conversion, eta = 1 (channel coupling) | 0.000 | 0.150 +- 0.018 | 0.223 +- 0.025 | 0.264 +- 0.024 | 0.025 / 0.072 |
| **XW, eta = 4** | 0.000 | 0.294 +- 0.043 | 0.417 +- 0.031 | 0.455 +- 0.035 | 0.098 +- 0.016 / 0.242 +- 0.027 |
| M scar: slow hidden field, 20-tick memory, at its maximum | 0.000 | 0.126 +- 0.021 | 0.168 +- 0.016 | 0.248 +- 0.028 | 0.018 / 0.051 |
| X conversion above a density threshold | 0.000 | 0.000 | 0.000 | 0.000 (converging wind) | 0 |
| T terrain: static force field | 0.196 +- 0.021 | 0.198 +- 0.021 | 0.200 +- 0.016 | not run | 0.00 / 0.00 (the surrogate has no positions) |
| calibration: hidden parameter lR + 0.06 | 0.068 +- 0.014 | 0.066 +- 0.012 | not run | not run | 0.004 +- 0.009 / not run |

Sources: `results/screen_*.json` [programs.*.screen_pooled], `results/surrogate.json` [share_pooled].
G is weak. X is inert: the wind cannot compress matter to the trigger. T acts without inputs. M saturates below
XW. **XW is chosen**: zero without inputs, largest with the mix, larger still with the designed push, and a
level-1 anomaly to find. To 16 ticks at eta = 4 the screen is 0.320 +- 0.051 (aimed) and 0.498 +- 0.027
(regional; 0.95 at the 16th tick) (`results/views_XW_4.json`); the population view gives 0.30 +- 0.12 and
0.41 +- 0.10.

Screen 2 (new, `surrogate.py`): round 5 showed that the state-given screen overstates what a history-only
predictor keeps (4 to 6% in the block view). LLR is a small simulation-trained family (per-block ridge by region
of the push, residual ensemble) with 0.54 to 0.69 of oracle skill (the ladder's nets: 0.65 to 0.69). Trained
under the public law it plays P0, under the true law C. On the calibration arm it gives a share of 0.003 to
0.004, where the ladder's nets gave 0.005. For XW at eta = 4, horizons 1 to 16: 0.109 +- 0.016 (aimed), 0.300 +- 0.032
(regional); 19% and 38% of the state-given loss survive. Forecast, an estimate: 0.20 on the two triggered
classes, 0.10 on the full mix (blind not run, taken as zero).

Screen 3 (new): RES(n), a generic residual with no knowledge of the term: LLR(public) with its block maps
corrected on n single true-world episodes of the class.

| XW eta = 4, horizons 1 to 16 | n = 1 | n = 2 | n = 3 |
|---|---|---|---|
| gap public-to-true closed, aimed | 0.94 +- 0.08 | 1.46 +- 0.14 | 1.48 +- 0.10 |
| gap closed, regional | 0.70 +- 0.03 | 0.93 +- 0.07 | 1.06 +- 0.07 |

Above 1 means RES beats the true-law family trained on 25 futures. The same holds for M (1.0 and 1.2 at n = 2,
regional and designed).

## 4. Reference policies (all scripts; one net family, plus LLR as a second family)

| policy | what it is |
|---|---|
| K, O | climatology; the true law from the hidden state |
| C | the conditioned net trained on true-form simulations, at the true parameters and constants |
| P0, S(N) | round 5's: public-law prior simulations; scripted inference of the four parameters with the public law |
| D(N) | data only (also the no-simulator arm) |
| FT(N) | P0's net fine-tuned on N Lab mix episodes, steps by cross-validation |
| RES(N) | P0 plus the per-block residual of screen 3 fitted on N Lab mix episodes |
| H(N) | told the form, not the values: two episodes for S, eight dose arms, synthetic likelihood for (theta, W0, DW, rate) on the corrected simulator, then the C family at posterior draws. H_mix: the same from mix episodes only |

## 5. Acceptance, declared now

Block view, eta = 4, Lab of N = 32 episode equivalents (1,056 ticks; N = 2 and 8 also reported), shares re-picked
inside every world-cluster bootstrap resample.

1. sigma against the better of P0 and D >= 0.15 on the triggered classes (forecast 0.20; full mix reported,
   forecast 0.10, below the bar).
2. sigma_g, with FT, RES and S added to the null, >= 0.15. Forecast: near 0 at N >= 8. Fails.
3. rho_g = (L(P0) - L(best of S, FT, RES)) / (L(P0) - L(C)) <= 0.7. Forecast 0.9 or more. Fails.
4. Solvable: H(32) recovers >= 0.7 of P0-to-C and beats the best generic recipe at z >= 3 over worlds.
5. Zero point as in section 1; with input-free Lab data FT and D equal their eta = 0 values within 2 SE.

Failure is bar 2 or 3 failing at N = 8: the incomplete law is repaired without a hypothesis. I will not conclude
from a pass that agents do science (only rollouts say), nor that H's form can be found by an agent; from a
failure, nothing about hidden finer levels or other worlds, nor about nets beyond the two generic recipes. The
surrogate numbers are forecasts from 6 states, not measurements of sigma.

## 6. Sizes and cost

| | stage 1 (decides) | stage 2 (only if bars 2 and 3 hold at N = 8) |
|---|---|---|
| dial, truths | eta 0 and 4; 4 of the ladder's truths | eta 0, 1, 2, 4; all 8 |
| per truth and eta | Lab 32 mix + 32 input-free; 96 items (24 per class), 12 replicates, 8 public-law plug-ins | + 32 designed episodes, 16 transfer items (pushes of 50 to 400 nats) |
| training sets | public and true-form families, 768 points x 8 episodes each | + H's emulator, 768 x 8 designed |
| policies, seeds | K, O, C, P0, D, S, FT, RES at N = 2, 8, 32; 2 net seeds for P0 and C | + H, H_mix |
| member-ticks (estimate) | 1.4 million | 2.2 million more |
| cost (estimate), cap | $1.5 on a 40 GB A100; cap $5 | $3.5; cap $15 |

Simulation alone is $0.6 and $0.9 at $0.40 per million. Largest array 7 x 10^7 elements. Compute budgets told to
the agent: research 8,192 full episodes (82 member-ticks each; 8 times P0's set, sized so that H fits);
prediction 0.05 of simulating a question.

## 7. Risks, cheapest tests, and what would change the program

| risk | cheapest test | status |
|---|---|---|
| a generic residual repairs the term | screen 3, CPU | seen: one episode closes 0.70 to 0.94; stage 1 checks it with nets |
| the share is capped (half the items and a quarter of the blocks are touched) | screen 2 | forecast 0.10 on the full mix; the triggered-class reading is declared |
| LLR is not the nets: a real C may leave RES behind at long horizons | stage 1 | open |
| the trigger leaks without inputs | bar 5 | fired in one of six burn-ins (300 ticks), weakly; input-free futures bit-identical |
| the form is public (this repo) | none needed for a pilot | an exam needs a form written and sealed privately: under (b) the secret is code |

If stage 1 confirms the forecast: an incomplete law whose defect shows at the observed level under the exam's
own programs does not make the exam test science, because "simulate the prior, then fit a residual" replaces
"simulate the prior"; sigma should then be defined against RES everywhere. Design (b) is worth pursuing only
where a per-block residual cannot express the defect (a hidden map fixed per world, events at the level of
bodies, a hidden slow variable with memory longer than an item, the hidden-finer-level designs), or where the
budget forbids sampling the exam's conditions, which is design (c). If stage 1 refutes it (FT and RES close
less than 0.7 while C beats P0 by 0.15 on the triggered classes), this is the first design to pass and goes to
stage 2 and to rollouts. Either way the three screens cost about 10 CPU-minutes per candidate and belong on the
world card.

Files: `dlaw.py` (the law with the five terms), `probe.py`, `check_zero.py`, `screen.py`, `views.py`, `dose.py`,
`surrogate.py`, `baseline_by_class.py`, `make_summary.py`; each docstring says what it runs. `PROGRESS.md` is the log.
