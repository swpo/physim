# Evidence pack: marangoni-droplets (seed 7)

- world: `../../20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 349s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T1239-c10-review-marangoni/a-20 --seeds 7 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0485, 1.2697], min area 6 px

## Measurements
- components: final 8, mean 5.0, max 8; occupancy final 0.10
- tracks: 14; persistent (alive >= 50% of run): 0; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.11, -0.5145, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 161: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.08; core [0.947, 0.028, 0.15] rim [0.744, 0.111, 0.113]
  - track 7 at frame 161: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.09; core [0.945, 0.028, 0.171] rim [0.747, 0.111, 0.125]
  - track 8 at frame 161: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.09; core [0.945, 0.028, 0.171] rim [0.747, 0.111, 0.125]
  - track 9 at frame 161: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.08; core [0.947, 0.028, 0.151] rim [0.75, 0.11, 0.113]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 48.1 (aggregate of 34 individuals; 2/34 membrane-like individually; rim level 0.883)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14, rim/outside 0.637 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.223)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 3.99 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.281)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=16100, R_eq 7.9): none; #7 (t=16100, R_eq 7.98): none; #8 (t=16100, R_eq 7.98): none; #9 (t=16100, R_eq 7.88): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
