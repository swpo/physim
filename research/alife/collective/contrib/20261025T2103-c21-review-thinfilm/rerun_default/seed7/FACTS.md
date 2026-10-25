# Evidence pack: thinfilm-active (seed 7)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2103-c21-review-thinfilm/rerun_default --seeds 7 8 --frames 80 --no-movie`
- segmentation: matter > 0.10 of robust range [0.0504, 4.7549], min area 6 px

## Measurements
- components: final 7, mean 9.4, max 15; occupancy final 0.25
- tracks: 66; persistent (alive >= 50% of run): 5; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 37.71 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 5], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0165/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 20, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [0.0, 4.2796, -665.0935, -641.2268]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 44: holes 0, rim-vs-core 0.32, rim-vs-outside 0.27, heterogeneity 0.10; core [0.511, 0.948, 0.094, 0.829] rim [0.21, 0.862, 0.127, 0.774]
  - track 45 at frame 47: holes 0, rim-vs-core 0.26, rim-vs-outside 0.20, heterogeneity 0.09; core [0.404, 0.918, 0.954, 0.762] rim [0.176, 0.816, 0.901, 0.721]
  - track 48 at frame 49: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.13; core [0.616, 0.954, 0.244, 0.098] rim [0.225, 0.863, 0.28, 0.158]
  - track 13 at frame 35: holes 0, rim-vs-core 0.16, rim-vs-outside 0.22, heterogeneity 0.07; core [0.356, 0.907, 0.146, 0.21] rim [0.208, 0.861, 0.153, 0.249]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.62, rim/outside 6.22 (aggregate of 60 individuals; 1/60 membrane-like individually; rim level 0.375)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 2.21 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.907)
  - radial p_x: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.965 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.427)
  - radial p_y: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.935 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=2200, R_eq 10.79): none; #45 (t=2350, R_eq 9.1): none; #48 (t=2450, R_eq 12.83): none; #13 (t=1750, R_eq 7.94): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
