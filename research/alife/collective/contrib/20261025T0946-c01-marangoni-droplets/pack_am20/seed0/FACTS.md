# Evidence pack: marangoni-droplets (seed 0)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 280s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T0946-c01-marangoni-droplets/pack_am20 --seeds 0 1 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0498, 1.2449], min area 6 px

## Measurements
- components: final 8, mean 5.4, max 8; occupancy final 0.10
- tracks: 14; persistent (alive >= 50% of run): 4; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.16 (1 = constant size)
- enclosures: components with a hole mean 0.25, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1167, -0.5334, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 138: holes 0, rim-vs-core 0.16, rim-vs-outside 0.60, heterogeneity 0.09; core [0.949, 0.029, 0.214] rim [0.818, 0.081, 0.13]
  - track 5 at frame 138: holes 0, rim-vs-core 0.22, rim-vs-outside 0.54, heterogeneity 0.09; core [0.949, 0.026, 0.177] rim [0.753, 0.111, 0.141]
  - track 8 at frame 141: holes 0, rim-vs-core 0.23, rim-vs-outside 0.53, heterogeneity 0.09; core [0.951, 0.027, 0.187] rim [0.738, 0.113, 0.147]
  - track 10 at frame 151: holes 0, rim-vs-core 0.22, rim-vs-outside 0.61, heterogeneity 0.11; core [0.959, 0.027, 0.39] rim [0.816, 0.082, 0.229]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 30.3 (aggregate of 34 individuals; 4/34 membrane-like individually; rim level 0.826)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.79, rim/outside 0.618 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.21)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 2.96 (aggregate of 34 individuals; 8/34 membrane-like individually; rim level 0.233)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=13800, R_eq 8.18): none; #5 (t=13800, R_eq 8.18): none; #8 (t=14100, R_eq 8.18): none; #10 (t=15100, R_eq 8.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
