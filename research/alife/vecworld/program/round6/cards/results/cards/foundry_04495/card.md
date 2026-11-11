# World card: foundry_04495

Family foundry, role candidate. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: exam-worthy + actions; run late: exam-worthy + actions. sigma_hat 0.19 at the grid level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 0.99 / 0.96 / 0.86 / 0.61 / 0.087 | 0.82 |
| bodies, displacement on quiet steps | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.99 / 0.99 / 0.98 / 0.99 | 0.98 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 0.99 / 0.99 / 0.95 / 0.87 | 0.98 |

## 2. Structure

- Bodies: 8.88 +- 7.14 (slots 24, full 7.3% of the time), 89.3% of the matter, radius 1.54 px, half-life 68.4 ticks, net speed 0.15 px/tick.
- Events per 100 ticks and member: 8.50 fusions, 1.75 fissions, 1.67 births, 0.42 deaths.
- Scales: wavelength 12.3 px; neighbouring-block correlation 0.26; block-view autocorrelation at 1 / 8 / 32 ticks 0.99 / 0.48 / 0.032; 16.1% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.99 / 0.99 / 0.99 / 0.98; constant velocity alone 0.99 / 0.99 / 0.99 / 0.98; with the surrounding block view 0.99 / 0.99 / 0.99 / 0.98. Quiet share of 8-tick steps 0.90 (178 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 4.2e-04 [0.001], population 0.601 [0.927] (count 0.93, tracked_mass 0.72, mean_speed 0.48, mass_sd 0.50, mass_max 0.88, kind_share 0.087).
- Share between members' time-means: block view 0.092, population 0.089.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.060 sd, largest log sd ratio 0.38, body count x 0.11, events 10.2 -> 0.00, ceiling at 8 0.86 -> 0.91, sigma_hat 0.19 -> 0.13. Same statistics: **no**.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.999 at 1 tick; falls below 0.5 at 32 ticks; the worst tenth of (state, block) cells carries 85.5% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.99, quadratic 0.99.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.74 / 0.52, a constant drift 0.00 / 0.00, a line in s 0.85 / 0.62 (predictable fraction of the change 1.00 / 0.89).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 0.029 of the variance; the block view added to the body law by 0.001; block moments added to the population law by -8.0e-05; the population law beats persistence by 0.010.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.20 / -0.21 / -0.034; BA: -0.41 / -0.44 / -0.062. Predictable-fraction gain at 8: -8.4e-04 / -0.002. Smallest R^2 of a learned component on the hand channels: 0.11.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.016 of the block view's variance, 0.364 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 22.5 / 77.4 / 257; displacement of the aimed 200-nat input / twin floor 41.1; aimed / blind 335. Population level: 4.86.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 13.5 / 90.3 / 4102; population 1.92 / 14.2 / 2803.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.43 / 1.13 / 1.39; sigma_hat block view 0.19, population 0.024.
- Response to the aimed 200-nat input changes by 93.5 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 5808 nats per tick (3 nats in 5.2e-04 ticks).
- Noise twins: 3.7% of the matter placed differently after 8 ticks; doubling time 11.1 ticks.

## 9. Cost

- 0.046 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (21743 member-ticks/s); USD 0.025 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run late |
|---|---|---|
| exam_worthy | yes | yes |
| structure | no | no |
| interaction | no | no |
| reading_worthy | no | no |
| actions | yes | yes |
| stationary | yes | yes |
| levels_add | yes | yes |
| learned_differs | no | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.83 / 0.87.

Source: run A: job r6-cards-001; run late: job r6-cards-001; files `out/cards/foundry_04495__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
