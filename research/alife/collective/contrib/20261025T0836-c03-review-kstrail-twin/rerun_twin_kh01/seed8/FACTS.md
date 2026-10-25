# Evidence pack: rdtrail_slow5 (seed 8)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 19s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/kst/twin_kh01/seed8 --seeds 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9936], min area 6 px

## Measurements
- components: final 11, mean 7.3, max 13; occupancy final 0.14
- tracks: 64; persistent (alive >= 50% of run): 1; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.06 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.261/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 60, default): splits 27, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 5, merges 4, merge/split ratio 0.148, nucleations 0
- channel total drift (end/start - 1): [2.861, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 133: holes 0, rim-vs-core 0.37, rim-vs-outside 0.42, heterogeneity 0.18; core [0.863, 0.67, 0.662] rim [0.554, 0.514, 0.522]
  - track 35 at frame 160: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.17; core [0.82, 0.569, 0.688] rim [0.5, 0.416, 0.545]
  - track 17 at frame 74: holes 0, rim-vs-core 0.44, rim-vs-outside 0.40, heterogeneity 0.21; core [0.889, 0.76, 0.654] rim [0.543, 0.541, 0.481]
  - track 55 at frame 190: holes 0, rim-vs-core 0.31, rim-vs-outside 0.50, heterogeneity 0.19; core [0.868, 0.668, 0.645] rim [0.623, 0.523, 0.511]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 8.5 (aggregate of 48 individuals; 2/48 membrane-like individually; rim level 0.603)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 3.71 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.54)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 2.68 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.647)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=399, R_eq 17.36): none; #35 (t=480, R_eq 12.32): none; #17 (t=222, R_eq 17.3): none; #55 (t=570, R_eq 16.21): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
