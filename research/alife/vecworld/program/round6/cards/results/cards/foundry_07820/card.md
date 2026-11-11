# World card: foundry_07820

Family foundry, role candidate. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: dull: predictable by the cheap family; run late: dull: predictable by the cheap family. sigma_hat 0.065 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 0.99 / 0.99 | 1.00 / 1.00 / 1.00 / 0.99 / 0.95 / 0.79 | 0.97 |
| bodies, displacement on quiet steps | 0.36 / 0.55 / 0.67 / 0.81 / 0.88 / 0.92 | 0.26 / 0.28 / 0.27 / 0.17 / 0.22 / 0.12 | 0.24 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 0.93 / 0.93 / 0.91 / 0.91 / 0.88 / 0.90 | 0.94 / 0.96 / 0.95 / 0.94 / 0.91 / 0.84 | 0.95 |

## 2. Structure

- Bodies: 18.5 +- 2.71 (slots 24, full 0.4% of the time), 97.1% of the matter, radius 1.65 px, half-life 241 ticks, net speed 0.043 px/tick.
- Events per 100 ticks and member: 6.11 fusions, 3.94 fissions, 4.81 births, 3.67 deaths.
- Scales: wavelength 7.09 px; neighbouring-block correlation -0.053; block-view autocorrelation at 1 / 8 / 32 ticks 1.00 / 0.98 / 0.89; 4.5% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.26 / 0.27 / 0.17 / 0.22; constant velocity alone 0.00 / 0.00 / 0.00 / 0.00; with the surrounding block view 0.21 / 0.23 / 0.24 / 0.25. Quiet share of 8-tick steps 0.96 (526 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 2.0e-04 [6.1e-04], population 0.364 [0.847] (count 0.52, tracked_mass 0.85, mean_speed 0.10, mass_sd 0.43, mass_max 0.22, kind_share 0.064).
- Share between members' time-means: block view 0.112, population 0.258.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.10 sd, largest log sd ratio 0.47, body count x 0.48, events 10.0 -> 0.75, ceiling at 8 0.99 -> 0.99, sigma_hat 0.024 -> 0.014. Same statistics: **no**.

## 4. Effective laws

- Linear local law on the block view: ceiling 1.000 at 1 tick; falls below 0.5 at no horizon up to 32 ticks; the worst tenth of (state, block) cells carries 91.8% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.94, quadratic 0.90.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.00 / 0.10, a constant drift 0.00 / 0.00, a line in s 0.00 / 0.10 (predictable fraction of the change 0.43 / 0.69).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 4.8e-04 of the variance; the block view added to the body law by -0.002; block moments added to the population law by -0.010; the population law beats persistence by 0.081.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.003 / 0.003 / 0.030; BA: -2.3e-04 / 0.010 / 0.047. Predictable-fraction gain at 8: -0.002 / -0.002. Smallest R^2 of a learned component on the hand channels: 0.006.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.027 of the block view's variance, 4.278 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 3.46 / 13.3 / 53.3; displacement of the aimed 200-nat input / twin floor 8.25; aimed / blind 6.44. Population level: 13.1.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 0.85 / 11.9 / 179; population 0.28 / 2.31 / 2445.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.58 / 0.67 / 0.73; sigma_hat block view 0.024, population 0.065.
- Response to the aimed 200-nat input changes by 11.0 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 604 nats per tick (3 nats in 0.005 ticks).
- Noise twins: 9.6% of the matter placed differently after 8 ticks; doubling time 7.7 ticks.

## 9. Cost

- 0.045 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (22177 member-ticks/s); USD 0.025 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run late |
|---|---|---|
| exam_worthy | no | no |
| structure | yes | no |
| interaction | yes | yes |
| reading_worthy | yes | no |
| actions | yes | yes |
| stationary | yes | no |
| levels_add | no | no |
| learned_differs | no | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.99 / 0.98.

Source: run A: job r6-cards-001; run late: job r6-cards-001; files `out/cards/foundry_07820__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
