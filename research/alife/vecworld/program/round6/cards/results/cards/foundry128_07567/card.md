# World card: foundry128_07567

Family foundry, role size. Lattice [2, 128, 128], 4 substeps per tick; input: wind 2 x 16 x 16, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: exam-worthy + actions. sigma_hat 0.71 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 0.99 / 0.97 / 0.86 | 0.99 / 0.95 / 0.78 / 0.54 / 0.35 / 0.18 | 0.53 |
| bodies, displacement on quiet steps | 0.97 / 0.99 / 1.00 / 1.00 / 0.91 / 0.86 | 0.48 / 0.46 / 0.37 / 0.20 / 0.00 / 0.00 | 0.028 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 0.94 / 0.90 / 0.84 / 0.82 / 0.70 / 0.50 | 0.68 / 0.30 / 0.22 / 0.35 / 0.29 / 0.21 | 0.35 |

## 2. Structure

- Bodies: 44.1 +- 3.69 (slots 96, full 0.0% of the time), 36.0% of the matter, radius 2.63 px, half-life 11.1 ticks, net speed 1.07 px/tick.
- Events per 100 ticks and member: 203 fusions, 298 fissions, 157 births, 251 deaths.
- Scales: wavelength 12.7 px; neighbouring-block correlation 0.16; block-view autocorrelation at 1 / 8 / 32 ticks 0.97 / 0.30 / 0.25; 13.9% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.48 / 0.37 / 0.20 / 0.00; constant velocity alone 0.31 / 0.32 / 0.021 / 0.00; with the surrounding block view 0.47 / 0.36 / 0.20 / 0.00. Quiet share of 8-tick steps 0.20 (177 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 5.9e-05 [7.1e-05], population 0.089 [0.224] (count 0.039, tracked_mass 0.22, mean_speed 0.084, mass_sd 0.052, mass_max 0.043, kind_share 0.096).
- Share between members' time-means: block view 0.140, population 0.175.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.990 at 1 tick; falls below 0.5 at 16 ticks; the worst tenth of (state, block) cells carries 58.0% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.35, quadratic 0.34.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.67 / 0.71, a constant drift 0.00 / 0.030, a line in s 0.67 / 0.69 (predictable fraction of the change 0.87 / 0.61).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 0.002 of the variance; the block view added to the body law by 0.026; block moments added to the population law by 0.052; the population law beats persistence by 0.542.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.090 / -7.2e-04 / 0.13; BA: -0.10 / 9.3e-04 / 0.11. Predictable-fraction gain at 8: -0.010 / -0.010. Smallest R^2 of a learned component on the hand channels: 2.5e-04.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.013 of the block view's variance, 0.055 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 0.67 / 2.73 / 11.1; displacement of the aimed 200-nat input / twin floor 1.69; aimed / blind 4.35. Population level: 0.34.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 10.6 / 115 / 89.2; population 3.82 / 37.0 / 364.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.44 / 0.97 / 1.57; sigma_hat block view 0.44, population 0.71.
- Response to the aimed 200-nat input changes by 3.23 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 2283 nats per tick (3 nats in 0.001 ticks).
- Noise twins: 8.7% of the matter placed differently after 8 ticks; doubling time 8.2 ticks.

## 9. Cost

- 0.191 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (5236 member-ticks/s); USD 0.11 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A |
|---|---|
| exam_worthy | yes |
| structure | no |
| interaction | yes |
| reading_worthy | no |
| actions | yes |
| stationary | yes |
| levels_add | yes |
| learned_differs | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 0.99 / 0.99, ceiling 0.55 / 0.54.

Source: run A: job r6-cards-001; files `out/cards/foundry128_07567__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
