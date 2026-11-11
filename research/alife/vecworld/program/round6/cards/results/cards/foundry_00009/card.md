# World card: foundry_00009

Family foundry, role prior. Lattice [2, 64, 64], 4 substeps per tick; input: wind 2 x 8 x 8, noise std 0.25. Hidden part: 240 weights of the law net (+ 10 scalars, kept by the neighbours) (prior: round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour). Views: block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2.

**Verdict** run A: dull: the hidden part has no weight. sigma_hat 0.070 at the pop level.

![card](card.png)

Sizes: 16 members (8 fit), 400 ticks after 50 of burn-in, 32 test states x 6 replicas x 32 ticks; neighbours at [0.03, 0.1, 1.0] of the prior (2 directions x 2). Ratios are from medians over test states (typical state); `mean` marks the mean-based value.

## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks

| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |
|---|---|---|---|
| block view | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 0.98 | 1.00 |
| bodies, displacement on quiet steps | 0.38 / 0.43 / 0.55 / 0.65 / 0.77 / 0.85 | 0.046 / 0.075 / 0.077 / 0.00 / 0.00 / 0.00 | 0.00 |
| population (count, tracked_mass, mean_speed, mass_sd, mass_max, kind_share) | 0.93 / 0.91 / 0.88 / 0.84 / 0.84 / 0.85 | 0.94 / 0.93 / 0.95 / 0.90 / 0.94 / 0.77 | 0.81 |

## 2. Structure

- Bodies: 13.7 +- 1.76 (slots 24, full 0.0% of the time), 61.6% of the matter, radius 2.91 px, half-life 210 ticks, net speed 0.022 px/tick.
- Events per 100 ticks and member: 1.38 fusions, 0.016 fissions, 15.7 births, 14.3 deaths.
- Scales: wavelength 9.54 px; neighbouring-block correlation 0.10; block-view autocorrelation at 1 / 8 / 32 ticks 1.00 / 1.00 / 0.99; 1.5% of the matter relocated per tick.
- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling 0.046 / 0.077 / 0.00 / 0.00; constant velocity alone 0.00 / 0.00 / 0.00 / 0.00; with the surrounding block view 0.027 / 0.053 / 0.00 / 0.00. Quiet share of 8-tick steps 0.95 (400 test rows).

## 3. Stationarity

- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): block view 0.002 [0.005], population 0.497 [0.904] (count 0.039, tracked_mass 0.90, mean_speed 0.097, mass_sd 0.65, mass_max 0.52, kind_share 0.77).
- Share between members' time-means: block view 0.118, population 0.180.

## 4. Effective laws

- Linear local law on the block view: ceiling 1.000 at 1 tick; falls below 0.5 at no horizon up to 32 ticks; the worst tenth of (state, block) cells carries 78.1% of its excess error at 8 ticks.
- Population law at 8 ticks: linear ceiling 0.90, quadratic 0.88.
- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling 0.00 / 0.32, a constant drift 0.00 / 0.00, a line in s 0.00 / 0.35 (predictable fraction of the change 0.44 / 0.76).

## 5. Levels

- The slot list added to the block view's predictor lowers its error at 8 ticks by 1.2e-05 of the variance; the block view added to the body law by -0.017; block moments added to the population law by 0.002; the population law beats persistence by 0.094.

## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)

- Ceiling gain at 8 / 16 / 32 ticks, halves AB: 1.5e-04 / 9.3e-04 / 0.007; BA: 1.5e-04 / 6.9e-04 / 0.007. Predictable-fraction gain at 8: 3.4e-04 / 3.8e-04. Smallest R^2 of a learned component on the hand channels: 0.002.

## 7. Actions (block view, 4 ticks after the input starts)

- The aimed 200-nat shift is 2.7e-04 of the block view's variance, 0.400 of the cheap family's error.
- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats 0.22 / 0.90 / 3.85; displacement of the aimed 200-nat input / twin floor 0.48; aimed / blind 0.48. Population level: 0.051.

## 8. Hidden part

- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view 0.57 / 8.84 / 1043; population -0.021 / 0.50 / 242.
- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view 0.43 / 0.54 / 0.65; sigma_hat block view 0.002, population 0.070.
- Response to the aimed 200-nat input changes by 0.88 oracle variances when the hidden part moves by the prior. Evidence index for a 10% move: 321 nats per tick (3 nats in 0.009 ticks).
- Noise twins: 2.5% of the matter placed differently after 8 ticks; doubling time 14.5 ticks.

## 9. Cost

- 0.049 ms per member-tick on the job's GPU with the tracker on every member, compile excluded (20420 member-ticks/s); USD 0.027 per million member-ticks at USD 1.99/h.

## Gates and robustness

| gate | run A |
|---|---|
| exam_worthy | no |
| structure | no |
| interaction | yes |
| reading_worthy | no |
| actions | yes |
| stationary | yes |
| levels_add | yes |
| learned_differs | no |

Estimator size (even against odd test states, block view at 8 ticks): predictable fraction 1.00 / 1.00, ceiling 1.00 / 1.00.

Source: run A: job r6-cards-001; files `out/cards/foundry_00009__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards (`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.
