# World card: foundry_01672

Family foundry, role shortlist. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: exam-worthy + actions; run B: exam-worthy + actions; run late: exam-worthy + actions. sigma_hat 0.49 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 0.99 / 0.94 | 1.00 / 0.99 / 0.93 / 0.76 / 0.46 / 0.031 | 0.75 |
| bodies, displacement on quiet steps | 0.99 / 0.99 / 1.00 / 1.00 / 1.00 / 1.00 | 0.98 / 0.98 / 0.97 / 0.95 / 0.93 / 0.88 | 0.81 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 1.00 / 1.00 / 1.00 / 0.99 / 0.96 / 0.84 | 0.98 / 0.87 / 0.80 / 0.44 / 0.29 / 0.046 | 0.46 |

## 2. Structure

- Bodies: 4.06 +- 1.21 (slots 24, full 0.0% of the time), 65.0% of the matter, radius 4.29 px, half-life 37.3 ticks, net speed 0.62 px/tick.
- Events per 100 ticks and member: 11.0 fusions, 9.92 fissions, 0.83 births, 0.20 deaths.
- Scales: wavelength 12.1 px; neighbouring-block correlation 0.29; block-view autocorrelation at 1 / 8 / 32 ticks 0.99 / 0.50 / 0.007; 15.0% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.98 / 0.97 / 0.95 / 0.93; constant velocity alone 0.98 / 0.97 / 0.95 / 0.91; with the surrounding block view 0.98 / 0.97 / 0.95 / 0.91. Quiet share of 8-tick steps 0.66 (88.0 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 1.1e-05 [3.1e-05], population 0.041 [0.130] (count 0.10, tracked_mass 0.13, mean_speed 0.016, mass_sd -0.056, mass_max 0.037, kind_share 0.022).
- Share between members' time-means: block view 0.164, population 0.086.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.001 sd, largest log sd ratio 0.026, body count x 0.95, events 20.9 -> 21.0, ceiling at 8 0.76 -> 0.75, sigma_hat 0.28 -> 0.30. Same statistics: **yes**.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.998 at 1 tick; falls below 0.5 at 16 ticks; the worst tenth of (state, block) cells carries 66.4% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.44, quadratic 0.45.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.031 / 0.039, a constant drift 0.002 / 0.016, a line in s 0.029 / 0.041 (predictable fraction of the change 1.00 / 0.77).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 0.017 of the variance; the block view added to the body law by -0.072; block moments added to the population law by 0.020; the population law beats persistence by 0.105.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.34 / -0.23 / 0.024; BA: -0.33 / -0.22 / 0.077. Predictable-fraction gain at 8: -0.014 / -0.013. Smallest R^2 of a learned component on the hand channels: 0.057.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.024 of the block view's variance, 0.335 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 5.23 / 20.5 / 72.2; displacement of the aimed 200-nat input / twin floor 11.3; aimed / blind 9.00. Population level: 4.17.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 14.8 / 125 / 346; population 40.3 / 634 / 2558.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.47 / 0.94 / 1.72; sigma_hat block view 0.28, population 0.49.
- Response to the aimed 200-nat input changes by 38.9 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 6994 nats per tick (3 nats in 4.3e-04 ticks).
- Noise twins: 7.3% of the matter placed differently after 8 ticks; doubling time 7.9 ticks.

## 9. Cost

- 0.049 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (20306 member-ticks/s); USD 0.027 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run B | run late |
|---|---|---|---|
| exam_worthy | yes | yes | yes |
| structure | yes | yes | yes |
| interaction | no | no | no |
| reading_worthy | no | no | no |
| actions | yes | yes | yes |
| stationary | yes | yes | yes |
| levels_add | yes | yes | yes |
| learned_differs | no | no | no |

Seed (A against B): 25 of 30 entries agree; not robust: grid.aim_ratio, grid.xresp, pop.ceil8, l.dceil16_AB, k.law32.

Size (64 px against foundry128_01672; counts per area, action entries left out): 23 of 26 entries agree; not robust: grid.member_share, pop.ceil8, k.law32.

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.74 / 0.76.

Source: run A: job r6-cards-001; run B: job r6-cards-001; run late: job r6-cards-001; files `out/cards/foundry_01672__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
