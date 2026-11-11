# World card: foundry_04289

Family foundry, role candidate. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: exam-worthy + reading-worthy + actions; run late: exam-worthy + reading-worthy + actions. sigma_hat 0.52 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 0.98 | 1.00 / 0.99 / 0.96 / 0.82 / 0.54 / 0.21 | 0.83 |
| bodies, displacement on quiet steps | 0.99 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 0.69 / 0.78 / 0.80 / 0.78 / 0.74 / 0.65 | 0.71 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 1.00 / 0.98 / 0.98 / 0.97 / 0.96 / 0.90 | 0.86 / 0.83 / 0.73 / 0.41 / 0.32 / 0.11 | 0.58 |

## 2. Structure

- Bodies: 13.8 +- 2.75 (slots 24, full 0.047% of the time), 86.4% of the matter, radius 2.63 px, half-life 27.8 ticks, net speed 0.38 px/tick.
- Events per 100 ticks and member: 27.4 fusions, 18.8 fissions, 33.7 births, 24.8 deaths.
- Scales: wavelength 9.07 px; neighbouring-block correlation 0.13; block-view autocorrelation at 1 / 8 / 32 ticks 1.00 / 0.81 / 0.37; 10.8% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.69 / 0.80 / 0.78 / 0.74; constant velocity alone 0.66 / 0.80 / 0.78 / 0.74; with the surrounding block view 0.70 / 0.80 / 0.78 / 0.76. Quiet share of 8-tick steps 0.65 (262 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 1.5e-04 [3.6e-04], population 0.113 [0.267] (count 0.25, tracked_mass 0.27, mean_speed 0.023, mass_sd 0.017, mass_max 0.001, kind_share 0.12).
- Share between members' time-means: block view 0.186, population 0.053.
- Late window (+1950 ticks) against early: largest shift of a block-channel mean 0.016 sd, largest log sd ratio 0.034, body count x 1.05, events 46.2 -> 48.6, ceiling at 8 0.82 -> 0.85, sigma_hat 0.23 -> 0.21. Same statistics: **yes**.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.999 at 1 tick; falls below 0.5 at 32 ticks; the worst tenth of (state, block) cells carries 61.5% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.41, quadratic 0.41.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.19 / 0.46, a constant drift 0.00 / 0.00, a line in s 0.15 / 0.47 (predictable fraction of the change 0.91 / 0.94).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 0.003 of the variance; the block view added to the body law by 0.019; block moments added to the population law by 0.012; the population law beats persistence by 0.077.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.087 / -0.073 / 0.046; BA: -0.12 / -0.100 / -0.013. Predictable-fraction gain at 8: -0.001 / -0.002. Smallest R^2 of a learned component on the hand channels: 0.025.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.002 of the block view's variance, 0.050 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 2.23 / 9.01 / 38.5; displacement of the aimed 200-nat input / twin floor 4.93; aimed / blind 3.89. Population level: 0.061.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 5.73 / 49.1 / 1508; population 1.00 / 12.6 / 3843.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.61 / 0.79 / 0.97; sigma_hat block view 0.23, population 0.52.
- Response to the aimed 200-nat input changes by 7.18 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 1592 nats per tick (3 nats in 0.002 ticks).
- Noise twins: 4.6% of the matter placed differently after 8 ticks; doubling time 7.8 ticks.

## 9. Cost

- 0.046 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (21764 member-ticks/s); USD 0.025 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A | run late |
|---|---|---|
| exam_worthy | yes | yes |
| structure | yes | yes |
| interaction | yes | yes |
| reading_worthy | yes | yes |
| actions | yes | yes |
| stationary | yes | yes |
| levels_add | yes | yes |
| learned_differs | no | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.82 / 0.82.

Source: run A: job r6-cards-001; run late: job r6-cards-001; files `out/cards/foundry_04289__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
