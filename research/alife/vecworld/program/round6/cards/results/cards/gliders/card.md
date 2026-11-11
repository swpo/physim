# World card: gliders

Family gliders, role designed. Lattice [2, 128, 128], 20 substeps per tick; input: wind 2 x 8 x 8, noise std 0.05. Hidden part: lR, dm_00, ls_00, lh (4 global parameter(s) of the Flow-Lenia law) (prior: round 5 ladder's box for this hidden set (scanned box x 0.6; for 4 parameters = track2/gliders_exam/results/prior.json); theta = the centre). Views: Phi_coarse (block means of 2 channels and of S^2, 16 px blocks); the port's blob tracker (12 slots).

**Verdict** run A: exam-worthy + actions; run B: exam-worthy + actions; run late: exam-worthy + actions. sigma_hat 0.16 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 0.99 / 0.92 / 0.67 | 0.99 / 0.96 / 0.84 / 0.49 / 0.21 / 0.007 | 0.49 |
| bodies, displacement on quiet steps | 0.99 / 0.99 / 1.00 / 1.00 / 1.00 / 0.99 | 0.99 / 0.99 / 0.98 / 0.96 / 0.96 / 0.97 | 0.80 |
| population (count, mean_speed, mass_sd, mass_max, kind_share) | 1.00 / 0.99 / 0.98 / 0.93 / 0.82 / 0.44 | 0.91 / 0.65 / 0.36 / 0.31 / 0.008 / 0.23 | 0.21 |

## 2. Structure

- Bodies: 7.69 +- 1.42 (slots 12, full 0.1% of the time), 99.9% of the matter, radius 6.46 px, half-life 24.2 ticks, net speed 1.76 px/tick.
- Events per 100 ticks and member: 23.6 fusions, 23.4 fissions, 0.00 births, 0.00 deaths.
- Scales: wavelength 12.0 px; neighbouring-block correlation 0.11; block-view autocorrelation at 1 / 8 / 32 ticks 0.97 / 0.22 / -0.065; 45.1% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.99 / 0.98 / 0.96 / 0.96; constant velocity alone 0.99 / 0.98 / 0.96 / 0.96; with the surrounding block view 0.99 / 0.98 / 0.96 / 0.96. Quiet share of 8-tick steps 0.53 (86.0 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 5.0e-08 [1.5e-07], population 0.024 [0.049] (count 0.013, mean_speed 0.049, mass_sd 0.028, mass_max 0.023, kind_share 0.008).
- Share between members' time-means: block view 0.726, population 0.101.
- Late window (+600 ticks) against early: largest shift of a block-channel mean 3.3e-04 sd, largest log sd ratio 0.010, body count x 0.95, events 47.0 -> 43.7, ceiling at 8 0.49 -> 0.50, sigma_hat 0.11 -> 0.100. Same statistics: **yes**.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.989 at 1 tick; falls below 0.5 at 8 ticks; the worst tenth of (state, block) cells carries 61.1% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.31, quadratic 0.24.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.13 / 0.44, a constant drift 0.00 / 0.006, a line in s 0.14 / 0.44 (predictable fraction of the change 0.83 / 0.56).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by -0.019 of the variance; the block view added to the body law by 0.020; block moments added to the population law by 0.010; the population law beats persistence by 0.758.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.32 / -0.086 / 0.028; BA: -0.35 / -0.15 / -0.011. Predictable-fraction gain at 8: -0.187 / -0.203. Smallest R^2 of a learned component on the hand channels: 0.013.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.020 of the block view's variance, 0.125 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 1.59 / 5.57 / 23.0; displacement of the aimed 200-nat input / twin floor 3.34; aimed / blind 4.03. Population level: 0.14.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view -0.003 / 0.055 / 4.62; population 6.8e-05 / 0.007 / 1.61.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.015 / 0.058 / 0.27; sigma_hat block view 0.11, population 0.16.
- Response to the aimed 200-nat input changes by 0.18 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 3.60 nats per tick (3 nats in 0.832 ticks).
- Noise twins: 30.9% of the matter placed differently after 8 ticks; doubling time 8.2 ticks.

## 9. Cost

- 1.455 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (687 member-ticks/s); USD 0.80 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run B | run late |
|---|---|---|---|
| exam_worthy | yes | yes | yes |
| structure | yes | yes | yes |
| interaction | no | no | no |
| reading_worthy | no | no | no |
| actions | yes | yes | yes |
| stationary | no | no | no |
| levels_add | yes | yes | yes |
| learned_differs | no | no | no |

Seed (A against B): 22 of 29 entries agree; not robust: grid.act_ms, grid.aim_ratio, pop.ceil8, pop.sigma_hat, pop.act_ms, l.dceil16_AB, k.law32.

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 0.99 / 0.99, ceiling 0.49 / 0.50.

Source: run A: job r6-cards-002; run B: job r6-cards-001; run late: job r6-cards-001; files `out/cards/gliders__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
