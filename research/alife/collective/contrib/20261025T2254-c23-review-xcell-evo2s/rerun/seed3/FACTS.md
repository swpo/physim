# Evidence pack: xcell-evo2-S (seed 3)

- world: `../../../../../../threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 699s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py --out collective/contrib/20261025T2254-c23-review-xcell-evo2s/rerun/seed3 --seeds 3 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.875], min area 6 px

## Measurements
- components: final 12, mean 10.7, max 12; occupancy final 0.13
- tracks: 36; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 6.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.174/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 200, default): splits 13, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.2548, None, 17.8335, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.52, heterogeneity 0.15; core [0.932, 0.622, 0.09, 0.901] rim [0.581, 0.936, 0.048, 0.588]
  - track 12 at frame 109: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.15; core [0.928, 0.598, 0.091, 0.912] rim [0.573, 0.938, 0.048, 0.608]
  - track 15 at frame 94: holes 0, rim-vs-core 0.56, rim-vs-outside 0.51, heterogeneity 0.16; core [0.935, 0.604, 0.091, 0.869] rim [0.595, 0.931, 0.049, 0.579]
  - track 30 at frame 175: holes 0, rim-vs-core 0.55, rim-vs-outside 0.50, heterogeneity 0.16; core [0.936, 0.618, 0.09, 0.771] rim [0.581, 0.928, 0.048, 0.496]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (body): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 86.7 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.872)
  - radial m (CH membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.58, rim/outside 9.8 (aggregate of 65 individuals; 64/65 membrane-like individually; rim level 0.948)  MEMBRANE-LIKE
  - radial h (marker): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 22.8 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.219)
  - radial q (waste): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 29 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.787)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): m (CH membrane)
- membrane-like channels per top track at mid-life: #9 (t=1010, R_eq 7.48): ['m (CH membrane)']; #12 (t=1090, R_eq 7.53): ['m (CH membrane)']; #15 (t=940, R_eq 7.46): ['m (CH membrane)']; #30 (t=1750, R_eq 7.33): ['m (CH membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
