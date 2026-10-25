# Evidence pack: marangoni-droplets (seed 7)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 400 steps x dt 0.25 (--dt; world META dt 0.5) = time 20000; grid [128, 128]; wall 547s; status ok
- command: `python -m labkit.run collective/contrib/c17-marangoni-wip/world.py --out collective/contrib/c17-marangoni-wip/rerun_a20_dt2/seed7 --seeds 7 --dt 0.25 --spf 400 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0223, 1.2497], min area 6 px

## Measurements
- components: final 37, mean 26.0, max 46; occupancy final 0.12
- tracks: 274; persistent (alive >= 50% of run): 37; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.00199/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 2000, default): splits 105, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 39, merge/split ratio 0.371, nucleations 23
- channel total drift (end/start - 1): [0.2015, -0.6851, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 150 at frame 136: holes 0, rim-vs-core 0.22, rim-vs-outside 0.39, heterogeneity 0.06; core [0.947, 0.013, 0.018] rim [0.724, 0.037, 0.011]
  - track 154 at frame 136: holes 0, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.07; core [0.934, 0.009, 0.077] rim [0.728, 0.032, 0.069]
  - track 174 at frame 136: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.07; core [0.923, 0.011, 0.087] rim [0.633, 0.043, 0.069]
  - track 261 at frame 141: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.06; core [0.929, 0.012, 0.027] rim [0.637, 0.042, 0.017]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 161 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 29.8 (aggregate of 161 individuals; 0/161 membrane-like individually; rim level 0.856)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.97, rim/outside 0.726 (aggregate of 161 individuals; 0/161 membrane-like individually; rim level 0.0909)
  - radial |v| (flow speed): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 2.52 (aggregate of 161 individuals; 3/161 membrane-like individually; rim level 0.0784)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #150 (t=13600, R_eq 3.78): none; #154 (t=13600, R_eq 4.15): none; #174 (t=13600, R_eq 4.18): none; #261 (t=14100, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
