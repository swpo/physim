# Round 4, study `bias` (track 1): learned level 1 from raw level-0 gliders states

Builds on `../../track1/learned_phi2` (on the block view, closure with a local equivariant encoder learned a tapered
window equal to a designed tent; reconstruction did worse; local vs global head made no difference) and
`../../track1/pilot_pooling*.py` (closed-form ring: reconstruction picks a useless feature, long-horizon closure
recovers block sums). Here level 1 itself is learned from the raw Flow-Lenia field (2 x 128 x 128) of the gliders
world (`../../../vw1/port/aworld.py`, unchanged), and the map (inductive bias -> emergent level-1 variables) is
measured for this one level-0 theory.

## Design (one GPU job, one platform)

| axis | values |
|---|---|
| encoder | N<h>: local, translation-equivariant (stride 16, periodic), receptive field = 16-px block + h px halo, h = 0, 4, 8, 16, linear window + nonlinear branch; L<h>: the same window, linear only; U: unconstrained (dense map of the whole field + MLP residual) |
| latent width | c = 1, 2, 4 numbers per block (8 x 8 grid, 64 c numbers) |
| objective | recon (block content from its own latent); clos (whitened latent predicts itself at h = 1, 4, 16 from 2 lags, global linear head); local (same, one shared local rule on the 3 x 3 neighbourhood); pib (whitened latent + N(0, 0.5^2) predicts the future level-0 block contents at h = 1, 4, 16) |
| seeds | 2 per cell, each fitted on both halves (cross-fitting as learned_phi2) |

Data: per half 32 certification trajectories (300 ticks, test ticks 40/100/160/220, 5 fresh-noise branches x 16
ticks) + 32 training-only trajectories; designer seeds 9701 (A) and 9702 (B), world seed 0, public parameters (no
exam secret). Judges (same for every Phi, including hand designs): closure ceilings of learned_phi2's fixed family
(`lphi.certify`: VW-0 family + local ridge) at h = 1, 2, 4, 8, 16; Gaussian predictive information; within-trajectory
variance share; cross-validated R^2 agreement with hand designs (block mass, block channel means, block view, tent,
object mass, object mass + position at block resolution), both directions; seed agreement.

Code: `b4.py` (layout, grid), `bsim.py` (GPU simulation), `bnets.py` (encoders, objectives), `btrain.py`
(training + encoding), `bcert.py` (CPU certification workers), `bcombine.py` (pooling), `bwin.py` (window
statistics), `job.sh`. Requests: `../../gpu/requests/r4-bias-001.json` (cancelled: vmapped convolution
gradients too slow), `r4-bias-002.json` (cancelled: CUDA out of memory, because jitted functions that closed over the
5 GB device copy of level 0 embedded it as a constant in every executable), `r4-bias-003.json` (data passed as
arguments, compiled functions released between configs).

## Results (GPU job r4-bias-003, H100 80GB PCIe, lambdalabs; 1.95 pod-hours, $6.01 billed; study total $7.94)

Full grid ran: 78 configs + 2 random baselines, 2 seeds x 2 cross-fit halves each (166 certified Phi, none
skipped). Level 0 float64 on the GPU (64 members per half, 300 ticks, 4 test ticks x 5 fresh-noise branches x 16
ticks, designer seeds 9701/9702, public parameters, no exam secret); encoders float32 on the GPU; certification on
the pod CPUs. Numbers with sources: `results/summary.json` (claims under `claims`); figures `results/fig_*.png`.

- Closure with a block-only receptive field rediscovers block mass on its own (R^2 both ways 0.93 N arm, 0.97 L arm;
  local law 0.97 / 0.995; seed R^2 >= 0.997). Nonlinear reconstruction does not (R^2 0.24 with mass, seed R^2 0.08,
  ceiling at h = 4 of 0.09 vs 0.77); linear and unconstrained reconstruction at c = 1 land on block mass.
- With a halo, closure learns a low-pass filtered mass field (the tent at an 8 px halo: R^2 0.93 / 0.97): ceiling at
  h = 16 rises 0.16 -> 0.55 with the halo, but effective dimension falls 44 -> 13 and predictable content I_avail
  214 -> 174 nats (block mass 275). The receptive field sets the smoothing, as in learned_phi2.
- Local law >= global closure; unconstrained closure is worse than block mass and seed-unstable; the predictive
  bottleneck lies in between; extra width (c = 2, 4) adds less-closed, non-mass content; no bias finds the object
  view (best R^2(objmass | Z) 0.685 vs 0.688 for block mass).
- Hand designs keep the most predictable content per number (block channel means 432 / 246 nats I_avail / I_capt
  at h = 1 vs at most 404 / 227 learned at c = 2).
