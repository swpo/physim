# Round 5, study `bias2` (track 1): two more rows of the map (level-0 theory x inductive bias) -> emergent variables

Round 4 (`../../round4/bias`) did one row: on raw Flow-Lenia gliders states, closure and local-law encoders learn block
mass. Here the same reduced grid runs on two level-0 theories in which nothing is conserved, the fed-vortex world
(`../../track1/vortex_world`: vorticity `om`, fuel `Y`, labels `a`, `b`) and the phase-membrane world
(`../../track1/membrane_world`: `phi`, `S`, `K`, `L`), and on gliders again as an anchor judged by exactly the same code.
Numbers with sources: `results/summary.json` (`claims`; every placeholder is filled from a result file by `cinterp.py`).
State of the work and of the GPU jobs: `PROGRESS.md`, `results/job_history.json`.

## Design

| axis | values |
|---|---|
| world | vortex (study tick 5 time units), membrane (40 time units), gliders (1 tick); 128 x 128, public parameters, world seed 0 |
| encoder | N0 / N8: local, translation-equivariant, 16-px block + 0 / 8 px halo, linear window + nonlinear branch; L0 / L8: the window only; U: dense, 64 c x 64 c whitening; Uc: dense, per-channel whitening. Same training settings for all (3,000 steps, batch 128, no weight decay) |
| width | c = 1, 2 numbers per block (gliders: 1), 8 x 8 blocks |
| objective | recon (block content from its own latent); clos (whitened latent predicts itself at h = 1, 4, 16 from 2 lags, global linear head); local (the same with one shared rule on the 3 x 3 neighbourhood) |
| seeds | 2 per config, each fitted on both halves (cross-fitted); designer seeds 9711/9712 (vortex), 9721/9722 (membrane), 9731/9732 (gliders) |

Data per half: 64 trajectories x 300 study ticks (32 certified at ticks 40/100/160/220 with 5 fresh-noise branches of
16 ticks, 32 for training only), float64 on the GPU. Judges, the same for every Phi and every hand design: closure
ceilings of learned_phi2's fixed predictor family at h = 1, 2, 4, 8, 16; effective dimension (participation ratio);
predictable content; seed agreement.

Round-4 checker's points, applied: agreement with hand designs by per-block local readouts with shared weights
(`loc1`, `loc1q`, `loc9`; round 4's all-block ridge kept as `glob`), both directions; explicit comparison with the
tent-windowed version of each feature; comparisons at matched effective dimension (interpolation along hand window
families, the most closed hand design with at least the latent's effective dimension, paired trajectory bootstraps
against hand windows on both sides); dense controls with the local encoders' training settings.

Hand designs: block means and 4 / 8 / 16-px tents of each field and of |om|, om^2, a + b, b - a, label-weighted
vorticity (vortex); of phi, S, K, L, wall 4 phi (1 - phi), phi K, cell area (membrane); of mass, c0, c1, c0 - c1,
mass^2 (gliders); 1 to 5 multi-channel designs; closed-form slow features (SFA) and PCA fitted on the other half.

## Results

GPU jobs: r5-bias2-004 (membrane, gliders) and r5-bias2-005 (vortex) on a nebius H200, 0.70 + 0.54 pod-hours,
$4.68 + $3.63; follow-up r5-bias2-007 (three worlds) on a lambdalabs A100 40GB, 1.17 pod-hours, $2.34. Billed in total
$10.64 of the $35 cap. All configs trained, none skipped by a deadline: 34 / 34 / 19 (grid), 10 per world (follow-up).

### The grid (closure loss on per-channel whitened latents)

What a linear block-only closure encoder (one number per block) finds:

| world | conserved | closure finds | evidence |
|---|---|---|---|
| gliders | total mass | block mass | per-block R2 0.97 (local law 0.994), flat window, seed agreement 1.000, box-mean share of variance 0.000 |
| vortex | nothing | the block reading of a slow box-scale fuel and label mode; no vorticity | R2 0.967 from the four block means, weights on Y, a, b (0.98, 0.22, -0.20), vorticity 0.000; R2 0.948 with closed-form SFA; seed agreement 0.999; effective dimension 7 of 64; box mean 36% of its variance, and that box mean is the box-mean label b / fuel (R2 0.97 each, 0.999 jointly) |
| membrane | nothing | a within-block spatial gradient of phi - K + L; not a block mean | R2 0.044 from the four block means; window: flat share 0.015, gradient share 0.45, K gradient opposite to phi's in 4 of 4 replicas; direction arbitrary, so seed agreement 0.59 with equal ceilings |

- With this loss, "closure finds mass" holds only in the mass-conserving theory. The loss rewards predicted variance
  per unit of pooled variance, so where nothing is conserved it takes the largest slow mode it can reach: a box-scale
  composition mode in the vortex world (the nonlinear encoders push further: effective dimension 2-4, box mean 50-71%
  of the variance; the dense encoder with per-channel whitening collapses onto one global number with ceiling 0.94
  at h = 16, which is the box-mean label b at R2 0.89), a sub-block geometric moment in the membrane world. In gliders
  the same collapse finds nothing (ceiling 0.004): the conserved total is constant.
- Vorticity, the most closed hand block mean of the vortex world (ceiling 0.34 at h = 16), is not chosen at c = 1; at
  c = 2 linear closure holds it as the second variable (R2 0.93).
- Learned against hand designs of at least the same effective dimension (h = 16): gliders, small gains (+0.007 to
  +0.041) on the mass family's trade-off curve; vortex, nothing learned beats the 16-px vorticity tent (0.74; the best
  local latent ties it with less than half its effective dimension); membrane, nonlinear closure is +0.20 to +0.25
  (z about 30) above the most closed hand design (closed-form extended SFA, 0.27), and +0.25 to +0.38 above block K and
  its tents. In the membrane world the block means of the fields are poor level-1 variables at long horizons.
- Local law against global closure: the same variable in gliders and the vortex world; in the membrane world the
  linear local law learns block cell material (R2 0.93 with block K, seed agreement 0.93) where global closure learns
  the gradient.
- Reconstruction: linear reconstruction learns the highest-variance block mean (fuel in the vortex world, R2 0.82;
  K in the membrane world, 0.98; mass in gliders, 0.97); nonlinear reconstruction at width 1 is seed-unstable and
  least closed in the vortex world and gliders (as round 4), and close to block phi in the membrane world (0.81).
- Dense control with full whitening (U): less closed than the local closure encoder in all three worlds (-0.06 to
  -0.14 at h = 16), never a per-block variable (per-block seed agreement 0.000).
- Seed agreement of closure with a global head: gliders 0.987-1.000; vortex 0.999 linear block-only, 0.52 linear with
  the halo, 0.49-0.88 nonlinear; membrane 0.12-0.59.

### The follow-up (closure loss on spatially whitened latents, `B5_ARMS=w`, encoders Lw / Nw)

Why: the vortex result above is a collapse (effective dimension 2-8) allowed by the loss's normalisation, so it could
not say whether closure prefers a transported density. Lw / Nw are the same local encoders with the closure loss
computed on latents whitened over all 64 blocks (every spatial mode has equal weight); the frozen Phi keeps per-channel
whitening. The job re-simulated the worlds and re-ran the per-channel closure configs and the hand designs on the
same data.

| world | block-only closure on spatially whitened latents finds | evidence |
|---|---|---|
| gliders | block mass | R2 0.991 linear (flat window share 0.999), 0.984 nonlinear; seed agreement 1.000 / 0.999 |
| vortex | block vorticity | R2 0.768 linear, 0.862 nonlinear; vorticity 78% of the linear latent's variance, flat window; seed agreement 0.997 / 0.969; effective dimension 34 (block vorticity 33; per-channel closure 7); R2 with SFA 0.018; with the halo, the vorticity tent (0.87) |
| membrane | nonlinear: a reproducible variable that is no hand block mean; linear: phi - K + L again, not reproducible | nonlinear: seed agreement 0.925 (per-channel 0.14), best block mean phi K 0.545, closed-form extended SFA 0.713, ceiling 0.43 at h = 16, +0.15 (z 24) above the most closed hand design; linear: seed agreement 0.09 |

- So closure finds the block density of the transported field in both theories that have one (mass, conserved;
  vorticity, advected but fed and dissipated) once the loss weights spatial modes equally. Conservation is not
  required; what conservation gave gliders for free is a constant global mode, which removes the collapse.
- The price: in the vortex world the whitened-closure latents are about as closed as hand block vorticity (+0.03 to
  +0.08 at h = 4, -0.02 to -0.04 at h = 16) and less closed than the collapsed per-channel latents (-0.12 at h = 8),
  with 5 to 8 times their effective dimension and more predictable content (I_capt 102-130 nats against 82).
- With the 8-px halo the spatial whitening works against the taper in gliders (agreement with the mass tent 0.71
  against 0.93 per-channel; seed agreement 0.55).
- Replication: the per-channel linear results reproduce on fresh simulations and another GPU type to within 0.001
  (vortex ceiling 0.353 against 0.352, SFA agreement 0.948 twice; gliders mass 0.971 twice); the membrane advantage of
  nonlinear closure over block K reproduces (+0.251 against +0.252); the vortex nonlinear closure ceiling does not
  (0.47 against 0.55 at h = 16).

## Files

`c5.py` (layout, grid, hand designs), `csim.py` (GPU simulation), `cnets.py`, `ctrain.py` (training, encoding),
`chand.py`, `cwin.py`, `ccert.py` (CPU certification workers), `ccombine.py`, `job.sh`; local analysis:
`cfetch.sh`, `canalyze.py` (tables, matched dimension, dominance), `cextra.py` (global part of the latents, window
shapes), `cpair.py` + `cpairs_run.sh` (paired bootstraps), `cclaims.py` + `cinterp.py` (claims), `csummary.py`;
`cpilot.py` (CPU pilots of the time scales; their designer seeds are never reused).
`results/`: `summary.json`, `analysis.json`, `extra.json`, `pairs_<world>.json`, `table_<world>.txt`,
`<world>/combined.json.gz` (the pod's pooled output), status and progress files of the jobs; `<world>_w` = the
follow-up job's run of `<world>`.
Raw arrays are not committed; per-item errors, latent subsamples and windows are at
`origin/gpu-jobs:jobs/<job_id>/out/<world>/{items,latsub,windows}`.
