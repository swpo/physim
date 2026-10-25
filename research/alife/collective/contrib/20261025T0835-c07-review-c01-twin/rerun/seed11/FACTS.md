# Evidence pack: kstrail-rd-twin (seed 11)

- world: `../../../20261025T0632-c01-kstrail-rd-twin/twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/contrib/20261025T0835-c07-review-c01-twin/rerun --seeds 7 11 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.799], min area 6 px

## Measurements
- components: final 6, mean 6.8, max 15; occupancy final 0.05
- tracks: 141; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 6, 5], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.892/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 60, default): splits 34, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 22, merge/split ratio 0.647, nucleations 52
- channel total drift (end/start - 1): [-0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 133: holes 0, rim-vs-core 0.24, rim-vs-outside 0.25, heterogeneity 0.13; core [0.773, 0.75, 0.646] rim [0.589, 0.643, 0.533]
  - track 95 at frame 168: holes 0, rim-vs-core 0.26, rim-vs-outside 0.31, heterogeneity 0.14; core [0.865, 0.69, 0.508] rim [0.63, 0.601, 0.449]
  - track 88 at frame 161: holes 0, rim-vs-core 0.35, rim-vs-outside 0.42, heterogeneity 0.21; core [0.973, 0.878, 0.585] rim [0.673, 0.723, 0.487]
  - track 87 at frame 160: holes 0, rim-vs-core 0.21, rim-vs-outside 0.28, heterogeneity 0.11; core [0.776, 0.647, 0.51] rim [0.626, 0.556, 0.399]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.74, rim/outside 4.03 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.581)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 1.98 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.647)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 1.66 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.514)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=399, R_eq 6.96): none; #95 (t=504, R_eq 7.27): none; #88 (t=483, R_eq 9.44): none; #87 (t=480, R_eq 6.08): none

## Warnings
- radial: 1 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
