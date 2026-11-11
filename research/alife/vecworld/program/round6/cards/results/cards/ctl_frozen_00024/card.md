# World card: ctl_frozen_00024

Family foundry, role control. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: dull: predictable by the cheap family; run B: dull: predictable by the cheap family; run late: dull: the hidden part has no weight. sigma_hat 0.045 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 |
| bodies, displacement on quiet steps | 0.22 / 0.32 / 0.23 / 0.41 / 0.43 / 0.59 | 0.23 / 0.031 / 0.16 / 0.017 / 0.00 / 0.00 | 0.00 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max) | 0.84 / 0.76 / 0.78 / 0.78 / 0.73 / 0.78 | 0.92 / 0.95 / 0.96 / 0.97 / 0.93 / 0.83 | 0.93 |

## 2. Structure

- Bodies: 13.5 +- 1.35 (slots 24, full 0.0% of the time), 24.4% of the matter, radius 1.82 px, half-life 1199 ticks, net speed 0.014 px/tick.
- Events per 100 ticks and member: 0.70 fusions, 0.28 fissions, 2.19 births, 1.34 deaths.
- Scales: wavelength 13.7 px; neighbouring-block correlation 0.100; block-view autocorrelation at 1 / 8 / 32 ticks 1.00 / 1.00 / 1.00; 1.4% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.23 / 0.16 / 0.017 / 0.00; constant velocity alone 0.00 / 0.00 / 0.00 / 0.00; with the surrounding block view 0.19 / 0.082 / 0.004 / 0.00. Quiet share of 8-tick steps 0.99 (432 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 9.4e-04 [0.002], population 0.172 [0.671] (count 0.020, tracked_mass 0.67, mean_speed 0.022, mass_sd 0.12, mass_max 0.028).
- Share between members' time-means: block view 0.097, population 0.256.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.12 sd, largest log sd ratio 0.60, body count x 0.84, events 0.98 -> 2.02, ceiling at 8 1.00 -> 1.00, sigma_hat 5.1e-04 -> 8.9e-05. Same statistics: **no**.

## 4. Effective laws

- Linear local law on the block view: ceiling 1.000 at 1 tick; falls below 0.5 at no horizon up to 32 ticks; the worst tenth of (state, block) cells carries 65.9% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.97, quadratic 0.92.

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 5.0e-06 of the variance; the block view added to the body law by 0.036; block moments added to the population law by -0.003; the population law beats persistence by 0.099.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -1.5e-04 / -7.8e-04 / -0.003; BA: -1.8e-04 / -7.5e-04 / -0.003. Predictable-fraction gain at 8: 5.7e-04 / 5.7e-04. Smallest R^2 of a learned component on the hand channels: 0.037.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.005 of the block view's variance, 5.704 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 1.44 / 6.62 / 35.1; displacement of the aimed 200-nat input / twin floor 3.35; aimed / blind 2.13. Population level: 2.26.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 0.32 / 3.73 / 1150; population 0.19 / 0.66 / 393.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.90 / 1.72 / 2.64; sigma_hat block view 5.1e-04, population 0.045.
- Response to the aimed 200-nat input changes by 138 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 76.0 nats per tick (3 nats in 0.039 ticks).
- Noise twins: 2.6% of the matter placed differently after 8 ticks; doubling time 17.0 ticks.

## 9. Cost

- 0.048 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (20995 member-ticks/s); USD 0.026 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run B | run late |
|---|---|---|---|
| exam_worthy | no | no | no |
| structure | no | no | yes |
| interaction | yes | no | no |
| reading_worthy | no | no | no |
| actions | yes | yes | yes |
| stationary | yes | yes | no |
| levels_add | no | no | yes |
| learned_differs | no | no | no |

Seed (A against B): 26 of 30 entries agree; not robust: pop.act_ms, s.events100, b.pf_disp8, b.ceil_disp8.

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 1.00 / 1.00.

Source: run A: job r6-cards-001; run B: job r6-cards-001; run late: job r6-cards-001; files `out/cards/ctl_frozen_00024__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
