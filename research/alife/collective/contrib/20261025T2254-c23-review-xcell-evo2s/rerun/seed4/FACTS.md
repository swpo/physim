# Evidence pack: xcell-evo2-S (seed 4)

- world: `../../../../../../threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 704s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py --out collective/contrib/20261025T2254-c23-review-xcell-evo2s/rerun/seed4 --seeds 4 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8711], min area 6 px

## Measurements
- components: final 10, mean 10.5, max 13; occupancy final 0.11
- tracks: 34; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 3.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.167/time; max body lengths 11.9
- replication (lineage window K = 20 frames = time 200, default): splits 12, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.3409, None, 4.0954, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.67, rim-vs-outside 0.57, heterogeneity 0.20; core [0.934, 0.615, 0.833, 0.8] rim [0.578, 0.92, 0.44, 0.525]
  - track 9 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.58, heterogeneity 0.21; core [0.93, 0.607, 0.828, 0.87] rim [0.566, 0.939, 0.425, 0.553]
  - track 8 at frame 87: holes 0, rim-vs-core 0.68, rim-vs-outside 0.59, heterogeneity 0.21; core [0.932, 0.617, 0.828, 0.854] rim [0.583, 0.926, 0.442, 0.554]
  - track 30 at frame 185: holes 0, rim-vs-core 0.68, rim-vs-outside 0.59, heterogeneity 0.21; core [0.939, 0.608, 0.838, 0.884] rim [0.598, 0.932, 0.45, 0.586]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (body): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 86.8 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.864)
  - radial m (CH membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.49, rim/outside 9.29 (aggregate of 67 individuals; 66/67 membrane-like individually; rim level 0.942)  MEMBRANE-LIKE
  - radial h (marker): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.728, rim/outside 69.5 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.708)
  - radial q (waste): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 26 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.772)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): m (CH membrane)
- membrane-like channels per top track at mid-life: #0 (t=1010, R_eq 7.33): ['m (CH membrane)']; #9 (t=1010, R_eq 7.65): ['m (CH membrane)']; #8 (t=870, R_eq 7.59): ['m (CH membrane)']; #30 (t=1850, R_eq 7.36): ['m (CH membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
