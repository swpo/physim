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
statistics), `job.sh`. Request: `../../gpu/requests/r4-bias-001.json`.
