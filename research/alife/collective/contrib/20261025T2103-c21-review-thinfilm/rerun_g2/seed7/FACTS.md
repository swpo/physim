# Evidence pack: thinfilm-active (seed 7)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 148s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2103-c21-review-thinfilm/rerun_g2 --seeds 7 8 --frames 80 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0287, 6.2159], min area 6 px

## Measurements
- components: final 1, mean 3.3, max 15; occupancy final 0.22
- tracks: 89; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 1000, default): splits 27, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio 1.04, nucleations 0
- channel total drift (end/start - 1): [-0.0, 3.5772, 77.3674, 90.4393]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 78 at frame 53: holes 0, rim-vs-core 0.59, rim-vs-outside 0.59, heterogeneity 0.23; core [0.889, 0.955, 0.083, 0.478] rim [0.368, 0.916, 0.351, 0.411]
  - track 45 at frame 18: holes 0, rim-vs-core 0.25, rim-vs-outside 0.22, heterogeneity 0.12; core [0.409, 0.921, 0.079, 0.295] rim [0.176, 0.85, 0.135, 0.3]
  - track 60 at frame 21: holes 0, rim-vs-core 0.24, rim-vs-outside 0.28, heterogeneity 0.13; core [0.419, 0.945, 0.224, 0.911] rim [0.227, 0.849, 0.324, 0.871]
  - track 81 at frame 68: holes 0, rim-vs-core 0.14, rim-vs-outside 0.23, heterogeneity 0.12; core [0.317, 0.862, 0.123, 0.712] rim [0.196, 0.845, 0.18, 0.756]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.574, rim/outside 2.91 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.228)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 1.44 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.731)
  - radial p_x: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.885 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.366)
  - radial p_y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 1.02 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.451)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #78 (t=2650, R_eq 37.26): none; #45 (t=900, R_eq 10.46): none; #60 (t=1050, R_eq 12.91): none; #81 (t=3400, R_eq 9.42): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 17 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 17 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
