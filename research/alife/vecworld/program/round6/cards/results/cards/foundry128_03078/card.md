# World card: foundry128_03078

Family foundry, role size. Lattice [2, 128, 128], 4 substeps per tick; input: wind 2 x 16 x 16, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: exam-worthy + reading-worthy + actions. sigma_hat 0.77 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 0.99 / 0.98 | 1.00 / 0.98 / 0.92 / 0.74 / 0.41 / 0.12 | 0.73 |
| bodies, displacement on quiet steps | 0.96 / 0.98 / 0.99 / 1.00 / 1.00 / 1.00 | 0.94 / 0.91 / 0.72 / 0.72 / 0.59 / 0.37 | 0.24 |
| population (count, mean_speed, mass_sd, mass_max) | 0.99 / 0.98 / 0.97 / 0.98 / 0.90 / 0.81 | 0.95 / 0.85 / 0.37 / 0.27 / 0.063 / 0.096 | 0.22 |

## 2. Structure

- Bodies: 52.5 +- 9.25 (slots 96, full 0.0% of the time), 98.4% of the matter, radius 2.71 px, half-life 37.5 ticks, net speed 0.25 px/tick.
- Events per 100 ticks and member: 109 fusions, 102 fissions, 1.33 births, 3.47 deaths.
- Scales: wavelength 7.67 px; neighbouring-block correlation 0.083; block-view autocorrelation at 1 / 8 / 32 ticks 0.99 / 0.68 / 0.14; 12.5% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.94 / 0.72 / 0.72 / 0.59; constant velocity alone 0.94 / 0.72 / 0.72 / 0.59; with the surrounding block view 0.94 / 0.72 / 0.72 / 0.59. Quiet share of 8-tick steps 0.74 (1073 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 3.0e-04 [9.0e-04], population 0.339 [0.776] (count 0.78, mean_speed 0.046, mass_sd 0.35, mass_max 0.19).
- Share between members' time-means: block view 0.080, population 0.062.

## 4. Effective laws

- Linear local law on the block view: ceiling 0.997 at 1 tick; falls below 0.5 at 16 ticks; the worst tenth of (state, block) cells carries 71.7% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.27, quadratic 0.20.

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 0.007 of the variance; the block view added to the body law by 0.055; block moments added to the population law by 0.019; the population law beats persistence by 0.279.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: -0.14 / -0.11 / -0.080; BA: -0.15 / -0.13 / -0.018. Predictable-fraction gain at 8: -0.002 / -0.003. Smallest R^2 of a learned component on the hand channels: 0.026.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 0.006 of the block view's variance, 0.070 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 1.10 / 4.45 / 17.1; displacement of the aimed 200-nat input / twin floor 2.66; aimed / blind 6.80. Population level: 0.31.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 4.05 / 32.1 / 363; population 2.60 / 20.9 / 368.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.54 / 0.84 / 1.34; sigma_hat block view 0.31, population 0.77.
- Response to the aimed 200-nat input changes by 4.69 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 4060 nats per tick (3 nats in 7.4e-04 ticks).
- Noise twins: 7.6% of the matter placed differently after 8 ticks; doubling time 7.5 ticks.

## 9. Cost

- 0.190 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (5253 member-ticks/s); USD 0.11 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A |
|---|---|
| exam_worthy | yes |
| structure | yes |
| interaction | yes |
| reading_worthy | yes |
| actions | yes |
| stationary | yes |
| levels_add | yes |
| learned_differs | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 0.74 / 0.73.

Source: run A: job r6-cards-001; files `out/cards/foundry128_03078__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
