# Evidence pack: kstrail-rd-twin (seed 0)

- world: `../../twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7469], min area 6 px

## Measurements
- components: final 8, mean 7.3, max 17; occupancy final 0.06
- tracks: 204; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 7], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.851/time; max body lengths 11.7
- replication (lineage window K = 20 frames = time 60, default): splits 49, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 32, merge/split ratio 0.653, nucleations 77
- channel total drift (end/start - 1): [-0.0, 0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 104 at frame 160: holes 0, rim-vs-core 0.18, rim-vs-outside 0.15, heterogeneity 0.11; core [0.742, 0.613, 0.444] rim [0.572, 0.553, 0.402]
  - track 16 at frame 111: holes 0, rim-vs-core 0.13, rim-vs-outside 0.12, heterogeneity 0.09; core [0.673, 0.632, 0.513] rim [0.563, 0.583, 0.479]
  - track 94 at frame 151: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.16; core [0.917, 0.783, 0.582] rim [0.648, 0.655, 0.473]
  - track 42 at frame 118: holes 0, rim-vs-core 0.33, rim-vs-outside 0.36, heterogeneity 0.18; core [0.963, 0.829, 0.584] rim [0.674, 0.695, 0.5]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.748, rim/outside 3.81 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.58)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 1.98 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.69)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 1.7 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #104 (t=480, R_eq 5.89): none; #16 (t=333, R_eq 5.61): none; #94 (t=453, R_eq 7.36): none; #42 (t=354, R_eq 6.6): none

## Warnings
- radial: 1 of 38 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
