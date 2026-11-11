# World card: ctl_uniform_00000

Family foundry, role control. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: dull: predictable by the cheap family; run B: dull: predictable by the cheap family; run late: dull: predictable by the cheap family. sigma_hat 0.005 at the grid level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 0.84 / 0.76 / 0.66 / 0.58 / 0.52 / 0.47 | 1.00 / 0.99 / 1.01 / 0.99 / 0.99 / 0.98 | 1.00 |
| bodies, displacement on quiet steps | n/a / n/a / n/a / n/a / n/a / n/a | n/a / n/a / n/a / n/a / n/a / n/a | n/a |

## 2. Structure

- Bodies: 0.00 +- 0.00 (slots 24, full 0.0% of the time), 0% of the matter, radius 0.00 px, half-life n/a ticks, net speed 0.00 px/tick.
- Events per 100 ticks and member: 0.00 fusions, 0.00 fissions, 0.00 births, 0.00 deaths.
- Scales: wavelength 3.53 px; neighbouring-block correlation 0.60; block-view autocorrelation at 1 / 8 / 32 ticks 0.91 / 0.75 / 0.62; 3.6% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling n/a / n/a / n/a / n/a; constant velocity alone n/a / n/a / n/a / n/a; with the surrounding block view n/a / n/a / n/a / n/a. Quiet share of 8-tick steps n/a (0 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 9.1e-06 [2.7e-05], population n/a [n/a].
- Share between members' time-means: block view 0.410, population n/a.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.012 sd, largest log sd ratio 0.57, body count x 1.00, events 0.00 -> 0.00, ceiling at 8 0.99 -> 0.99, sigma_hat 0.005 -> 0.002. Same statistics: **no**.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.996 at 1 tick; falls below 0.5 at no horizon up to 32 ticks; the worst tenth of (state, block) cells carries 66.0% of its excess error at 8 ticks.

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 1.1e-16 of the variance; the block view added to the body law by n/a; block moments added to the population law by n/a; the population law beats persistence by n/a.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: 0.001 / -0.011 / -0.003; BA: 0.004 / -0.008 / 0.004. Predictable-fraction gain at 8: 0.181 / 0.170. Smallest R^2 of a learned component on the hand channels: 4.0e-04.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.944 of the block view's variance, 3.600 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 0.88 / 3.56 / 14.2; displacement of the aimed 200-nat input / twin floor 1.73; aimed / blind 1.60. Population level: n/a.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 0.005 / 0.048 / 3.24; population n/a / n/a / n/a.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.81 / 2.38 / 5.96; sigma_hat block view 0.005, population n/a.
- Response to the aimed 200-nat input changes by 0.25 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 0.48 nats per tick (3 nats in 6.281 ticks).
- Noise twins: 4.0% of the matter placed differently after 8 ticks; doubling time 115 ticks.

## 9. Cost

- 0.046 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (21675 member-ticks/s); USD 0.026 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run B | run late |
|---|---|---|---|
| exam_worthy | no | no | no |
| structure | no | no | no |
| interaction | no | no | no |
| reading_worthy | no | no | no |
| actions | yes | yes | yes |
| stationary | no | no | no |
| levels_add | no | no | no |
| learned_differs | no | no | no |

Seed (A against B): 30 of 30 entries agree.

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 0.64 / 0.56, ceiling 1.00 / 0.99.

Source: run A: job r6-cards-001; run B: job r6-cards-001; run late: job r6-cards-001; files `out/cards/ctl_uniform_00000__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
