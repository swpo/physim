# Evidence pack: kstrail-rd-twin (seed 2)

- world: `../../twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 40s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7207], min area 6 px

## Measurements
- components: final 9, mean 8.3, max 18; occupancy final 0.06
- tracks: 197; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 6], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.876/time; max body lengths 10.9
- replication (lineage window K = 20 frames = time 60, default): splits 48, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 33, merge/split ratio 0.688, nucleations 69
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 156: holes 0, rim-vs-core 0.38, rim-vs-outside 0.37, heterogeneity 0.20; core [0.962, 0.932, 0.741] rim [0.66, 0.766, 0.576]
  - track 75 at frame 139: holes 0, rim-vs-core 0.28, rim-vs-outside 0.34, heterogeneity 0.16; core [0.91, 0.767, 0.562] rim [0.658, 0.673, 0.499]
  - track 45 at frame 111: holes 0, rim-vs-core 0.10, rim-vs-outside 0.11, heterogeneity 0.07; core [0.631, 0.555, 0.397] rim [0.545, 0.522, 0.373]
  - track 48 at frame 113: holes 0, rim-vs-core 0.02, rim-vs-outside 0.06, heterogeneity 0.04; core [0.555, 0.526, 0.395] rim [0.532, 0.519, 0.393]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 4.16 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.612)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 1.99 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.7)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 1.7 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.556)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #95 (t=468, R_eq 8.06): none; #75 (t=417, R_eq 6.7): none; #45 (t=333, R_eq 5.44): none; #48 (t=339, R_eq 2.93): none

## Warnings
- radial: 3 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
