# Evidence pack: kstrail-rd-twin (seed 7)

- world: `../../../../contrib/20261025T0632-c01-kstrail-rd-twin/twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 121s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/work_c05/rev_kt/twin/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.8229], min area 6 px

## Measurements
- components: final 7, mean 6.8, max 14; occupancy final 0.06
- tracks: 130; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 7], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.872/time; max body lengths 11.6
- replication (lineage window K = 20 frames = time 60, default): splits 29, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 21, merge/split ratio 0.724, nucleations 52
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 48 at frame 141: holes 0, rim-vs-core 0.38, rim-vs-outside 0.38, heterogeneity 0.20; core [0.949, 0.853, 0.644] rim [0.642, 0.688, 0.503]
  - track 52 at frame 143: holes 0, rim-vs-core 0.37, rim-vs-outside 0.46, heterogeneity 0.22; core [0.987, 0.934, 0.697] rim [0.697, 0.761, 0.539]
  - track 34 at frame 131: holes 0, rim-vs-core 0.29, rim-vs-outside 0.34, heterogeneity 0.16; core [0.906, 0.717, 0.551] rim [0.643, 0.616, 0.479]
  - track 90 at frame 175: holes 0, rim-vs-core 0.36, rim-vs-outside 0.46, heterogeneity 0.22; core [0.986, 0.922, 0.656] rim [0.702, 0.745, 0.518]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 39 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.706, rim/outside 3.9 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.54)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 2.07 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.65)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 1.76 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.526)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #48 (t=423, R_eq 7.88): none; #52 (t=429, R_eq 8.37): none; #34 (t=393, R_eq 6.65): none; #90 (t=525, R_eq 9.08): none

## Warnings
- radial: 3 of 39 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
