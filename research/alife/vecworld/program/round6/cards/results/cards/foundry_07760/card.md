# World card: foundry_07760

Family foundry, role candidate. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: exam-worthy + reading-worthy + actions; run late: dull: predictable by the cheap family. sigma_hat 0.18 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 0.99 | 1.00 / 1.00 / 0.99 / 0.95 / 0.79 / 0.46 | 0.93 |
| bodies, displacement on quiet steps | 0.79 / 0.89 / 0.94 / 0.97 / 0.98 / 0.99 | 0.78 / 0.79 / 0.77 / 0.67 / 0.69 / 0.72 | 0.68 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 0.97 / 0.97 / 0.97 / 0.95 / 0.93 / 0.95 | 0.96 / 0.96 / 0.91 / 0.82 / 0.73 / 0.64 | 0.81 |

## 2. Structure

- Bodies: 14.7 +- 3.58 (slots 24, full 2.7% of the time), 94.1% of the matter, radius 1.89 px, half-life 104 ticks, net speed 0.12 px/tick.
- Events per 100 ticks and member: 13.1 fusions, 10.3 fissions, 0.88 births, 0.95 deaths.
- Scales: wavelength 6.21 px; neighbouring-block correlation 0.095; block-view autocorrelation at 1 / 8 / 32 ticks 1.00 / 0.93 / 0.54; 6.9% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.78 / 0.77 / 0.67 / 0.69; constant velocity alone 0.74 / 0.70 / 0.60 / 0.63; with the surrounding block view 0.76 / 0.74 / 0.66 / 0.65. Quiet share of 8-tick steps 0.90 (367 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 0.002 [0.005], population 0.440 [0.933] (count 0.62, tracked_mass 0.93, mean_speed 0.25, mass_sd 0.32, mass_max 0.28, kind_share 0.23).
- Share between members' time-means: block view 0.022, population 0.151.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.089 sd, largest log sd ratio 0.54, body count x 0.62, events 23.4 -> 9.19, ceiling at 8 0.95 -> 1.00, sigma_hat 0.090 -> 0.003. Same statistics: **no**.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.999 at 1 tick; falls below 0.5 at 32 ticks; the worst tenth of (state, block) cells carries 85.9% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.82, quadratic 0.82.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.00 / 0.00, a constant drift 0.038 / 0.027, a line in s 0.00 / 0.00 (predictable fraction of the change 0.82 / 0.88).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 0.005 of the variance; the block view added to the body law by 0.003; block moments added to the population law by 0.007; the population law beats persistence by 0.011.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.064 / -0.15 / -0.100; BA: -0.050 / -0.11 / -0.13. Predictable-fraction gain at 8: -0.002 / -0.002. Smallest R^2 of a learned component on the hand channels: 0.014.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.017 of the block view's variance, 1.226 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 4.88 / 16.3 / 68.6; displacement of the aimed 200-nat input / twin floor 12.9; aimed / blind 12.7. Population level: 1.47.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 0.70 / 5.36 / 399; population 0.19 / 4.96 / 1206.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.59 / 0.72 / 0.85; sigma_hat block view 0.090, population 0.18.
- Response to the aimed 200-nat input changes by 11.3 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 309 nats per tick (3 nats in 0.010 ticks).
- Noise twins: 8.7% of the matter placed differently after 8 ticks; doubling time 8.3 ticks.

## 9. Cost

- 0.046 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (21944 member-ticks/s); USD 0.025 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run late |
|---|---|---|
| exam_worthy | yes | no |
| structure | yes | yes |
| interaction | yes | yes |
| reading_worthy | yes | yes |
| actions | yes | yes |
| stationary | yes | no |
| levels_add | yes | no |
| learned_differs | no | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.95 / 0.95.

Source: run A: job r6-cards-001; run late: job r6-cards-001; files `out/cards/foundry_07760__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
