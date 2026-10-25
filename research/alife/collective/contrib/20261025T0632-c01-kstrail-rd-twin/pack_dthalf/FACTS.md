# Evidence pack: kstrail-rd-twin (seed 0)

- world: `../twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 120 steps x dt 0.025 (--dt; world META dt 0.05) = time 600; grid [192, 192]; wall 90s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack_dthalf --seeds 0 --spf 120 --dt 0.025 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7382], min area 6 px

## Measurements
- components: final 11, mean 7.5, max 17; occupancy final 0.06
- tracks: 208; persistent (alive >= 50% of run): 0; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 8, 7], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.848/time; max body lengths 10.7
- replication (lineage window K = 20 frames = time 60, default): splits 50, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 36, merge/split ratio 0.72, nucleations 75
- channel total drift (end/start - 1): [0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 161: holes 0, rim-vs-core 0.17, rim-vs-outside 0.14, heterogeneity 0.10; core [0.734, 0.615, 0.442] rim [0.578, 0.56, 0.403]
  - track 94 at frame 151: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.16; core [0.923, 0.782, 0.574] rim [0.643, 0.653, 0.471]
  - track 21 at frame 113: holes 0, rim-vs-core 0.15, rim-vs-outside 0.15, heterogeneity 0.10; core [0.717, 0.67, 0.532] rim [0.602, 0.606, 0.468]
  - track 45 at frame 116: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.17; core [0.955, 0.793, 0.564] rim [0.665, 0.672, 0.493]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 3.44 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.576)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 1.87 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.672)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 1.62 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.543)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #109 (t=483, R_eq 5.92): none; #94 (t=453, R_eq 7.51): none; #21 (t=339, R_eq 5.75): none; #45 (t=348, R_eq 6.51): none

## Warnings
- radial: 2 of 42 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
