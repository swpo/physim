# Evidence pack: fed-vortices (seed 6)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2065], min area 6 px

## Measurements
- components: final 35, mean 34.1, max 38; occupancy final 0.14
- tracks: 89; persistent (alive >= 50% of run): 31; longest 151 frames; alive start-to-end: 11
- size of persistent tracks: max/min area ratio 5.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 35, 35], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.274/time; max body lengths 10.4
- replication (lineage window K = 20 frames = time 60, default): splits 21, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.429, nucleations 0
- channel total drift (end/start - 1): [-0.5498, 0.1482, -1037.9268, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.66, rim-vs-outside 0.31, heterogeneity 0.17; core [0.797, 0.105, 0.914, 0.616] rim [0.426, 0.314, 0.718, 0.155]
  - track 5 at frame 76: holes 0, rim-vs-core 0.74, rim-vs-outside 0.34, heterogeneity 0.20; core [0.842, 0.113, 0.052, 0.717] rim [0.437, 0.338, 0.257, 0.175]
  - track 19 at frame 76: holes 0, rim-vs-core 0.70, rim-vs-outside 0.29, heterogeneity 0.19; core [0.799, 0.117, 0.914, 0.641] rim [0.403, 0.317, 0.706, 0.135]
  - track 75 at frame 111: holes 0, rim-vs-core 0.55, rim-vs-outside 0.36, heterogeneity 0.17; core [0.752, 0.159, 0.093, 0.601] rim [0.448, 0.292, 0.251, 0.187]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 207 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 17.4 (aggregate of 207 individuals; 1/207 membrane-like individually; rim level 0.68)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.2, rim/outside 0.781 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.493)
  - radial vorticity (signed): peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.988 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.482)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.667, rim/outside 30.7 (aggregate of 207 individuals; 2/207 membrane-like individually; rim level 0.516)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 4.89): none; #5 (t=228, R_eq 4.69): none; #19 (t=228, R_eq 4.69): none; #75 (t=333, R_eq 5.86): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 207 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
