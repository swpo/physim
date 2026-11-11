# World card: foundry_07913

Family foundry, role candidate. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: dull: predictable by the cheap family; run late: dull: predictable by the cheap family. sigma_hat 0.046 at the grid level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 0.99 / 0.98 | 1.00 / 1.00 / 1.00 / 0.98 / 0.89 / 0.66 | 0.97 |
| bodies, displacement on quiet steps | 0.95 / 0.97 / 0.98 / 0.98 / 0.98 / 0.98 | 0.88 / 0.89 / 0.90 / 0.89 / 0.82 / 0.66 | 0.88 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 0.99 / 0.99 / 0.98 / 0.97 / 0.98 / 0.97 | 0.99 / 0.99 / 0.97 / 0.97 / 0.93 / 0.86 | 0.97 |

## 2. Structure

- Bodies: 14.5 +- 4.32 (slots 24, full 3.9% of the time), 82.5% of the matter, radius 2.27 px, half-life 202 ticks, net speed 0.097 px/tick.
- Events per 100 ticks and member: 4.77 fusions, 1.14 fissions, 1.91 births, 1.14 deaths.
- Scales: wavelength 9.00 px; neighbouring-block correlation 0.10; block-view autocorrelation at 1 / 8 / 32 ticks 1.00 / 0.95 / 0.59; 3.8% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.88 / 0.90 / 0.89 / 0.82; constant velocity alone 0.87 / 0.90 / 0.89 / 0.78; with the surrounding block view 0.88 / 0.90 / 0.89 / 0.83. Quiet share of 8-tick steps 0.95 (406 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 5.7e-04 [0.002], population 0.505 [0.921] (count 0.77, tracked_mass 0.92, mean_speed 0.035, mass_sd 0.52, mass_max 0.49, kind_share 0.30).
- Share between members' time-means: block view 0.054, population 0.193.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.028 sd, largest log sd ratio 0.27, body count x 0.57, events 5.91 -> 0.047, ceiling at 8 0.98 -> 1.00, sigma_hat 0.046 -> 0.007. Same statistics: **no**.

## 4. Effective laws

- Linear local law on the block view: ceiling 1.000 at 1 tick; falls below 0.5 at no horizon up to 32 ticks; the worst tenth of (state, block) cells carries 84.3% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.97, quadratic 0.97.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.00 / 0.00, a constant drift 0.00 / 0.00, a line in s 0.00 / 0.00 (predictable fraction of the change 0.88 / 0.82).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 5.1e-04 of the variance; the block view added to the body law by 9.4e-04; block moments added to the population law by 0.002; the population law beats persistence by 0.002.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.014 / -0.011 / 0.094; BA: -0.016 / -0.004 / 0.11. Predictable-fraction gain at 8: 1.0e-04 / 1.9e-04. Smallest R^2 of a learned component on the hand channels: 0.17.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.009 of the block view's variance, 1.902 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 3.81 / 16.5 / 76.1; displacement of the aimed 200-nat input / twin floor 9.33; aimed / blind 15.9. Population level: 6.24.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 2.61 / 15.9 / 7483; population 1.91 / 12.1 / 79.3.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 5.68 / 11.4 / 11.7; sigma_hat block view 0.046, population 0.041.
- Response to the aimed 200-nat input changes by 10.2 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 847 nats per tick (3 nats in 0.004 ticks).
- Noise twins: 5.2% of the matter placed differently after 8 ticks; doubling time 7.7 ticks.

## 9. Cost

- 0.046 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (21705 member-ticks/s); USD 0.025 per million member-ticks at USD 1.99/h.

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

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.98 / 0.98.

Source: run A: job r6-cards-001; run late: job r6-cards-001; files `out/cards/foundry_07913__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
