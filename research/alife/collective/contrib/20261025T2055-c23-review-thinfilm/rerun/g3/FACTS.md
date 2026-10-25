# Evidence pack: thinfilm-active (seed 6)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 88s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2055-c23-review-thinfilm/rerun/g3 --seeds 6 --frames 80 --no-movie`
- segmentation: matter > 0.13 of robust range [0.0448, 3.6026], min area 6 px

## Measurements
- components: final 2, mean 6.4, max 16; occupancy final 0.30
- tracks: 70; persistent (alive >= 50% of run): 2; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.36 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 2], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0583/time; max body lengths 6.9
- replication (lineage window K = 20 frames = time 1000, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 24, merge/split ratio 1.14, nucleations 0
- channel total drift (end/start - 1): [0.0, 4.8506, -47.4803, 529.0326]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 39: holes 0, rim-vs-core 0.37, rim-vs-outside 0.33, heterogeneity 0.16; core [0.619, 0.903, 0.34, 0.869] rim [0.269, 0.832, 0.362, 0.774]
  - track 21 at frame 31: holes 0, rim-vs-core 0.34, rim-vs-outside 0.22, heterogeneity 0.15; core [0.537, 0.89, 0.212, 0.781] rim [0.222, 0.811, 0.262, 0.71]
  - track 29 at frame 22: holes 0, rim-vs-core 0.32, rim-vs-outside 0.22, heterogeneity 0.13; core [0.518, 0.907, 0.345, 0.896] rim [0.239, 0.803, 0.339, 0.792]
  - track 48 at frame 45: holes 0, rim-vs-core 0.43, rim-vs-outside 0.38, heterogeneity 0.19; core [0.706, 0.929, 0.359, 0.855] rim [0.292, 0.886, 0.371, 0.751]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 4.23 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.398)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 1.95 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.84)
  - radial p_x: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.968 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.42)
  - radial p_y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 1.39 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.72)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=1950, R_eq 10.4): none; #21 (t=1550, R_eq 9.74): none; #29 (t=1100, R_eq 9.08): none; #48 (t=2250, R_eq 17.3): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
