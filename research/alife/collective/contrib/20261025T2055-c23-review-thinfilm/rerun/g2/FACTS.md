# Evidence pack: thinfilm-active (seed 5)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2055-c23-review-thinfilm/rerun/g2 --seeds 5 --frames 80 --no-movie`
- segmentation: matter > 0.09 of robust range [0.042, 4.9915], min area 6 px

## Measurements
- components: final 1, mean 3.6, max 14; occupancy final 0.26
- tracks: 91; persistent (alive >= 50% of run): 0; longest 21 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 1, 1], H1 [1, 1, 1]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0625/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 1000, default): splits 26, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 29, merge/split ratio 1.11, nucleations 0
- channel total drift (end/start - 1): [0.0, 4.3418, -671.8699, 477.259]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 57 at frame 27: holes 0, rim-vs-core 0.14, rim-vs-outside 0.12, heterogeneity 0.07; core [0.267, 0.901, 0.848, 0.815] rim [0.149, 0.841, 0.809, 0.799]
  - track 81 at frame 52: holes 0, rim-vs-core 0.19, rim-vs-outside 0.16, heterogeneity 0.11; core [0.321, 0.858, 0.734, 0.092] rim [0.155, 0.776, 0.707, 0.145]
  - track 90 at frame 71: holes 0, rim-vs-core 0.45, rim-vs-outside 0.67, heterogeneity 0.24; core [0.877, 0.787, 0.462, 0.724] rim [0.447, 0.92, 0.404, 0.723]
  - track 51 at frame 23: holes 0, rim-vs-core 0.25, rim-vs-outside 0.22, heterogeneity 0.14; core [0.422, 0.891, 0.341, 0.914] rim [0.194, 0.809, 0.362, 0.849]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.678, rim/outside 3.11 (aggregate of 18 individuals; 3/18 membrane-like individually; rim level 0.259)
  - radial |p| polar order: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.47 (aggregate of 18 individuals; 2/18 membrane-like individually; rim level 0.769)
  - radial p_x: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.03 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.512)
  - radial p_y: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.07 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.567)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #57 (t=1350, R_eq 7.33): none; #81 (t=2600, R_eq 8.06): none; #90 (t=3550, R_eq 34.87): none; #51 (t=1150, R_eq 10.11): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 18 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
