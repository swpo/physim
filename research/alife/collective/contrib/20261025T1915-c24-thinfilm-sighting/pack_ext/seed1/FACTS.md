# Evidence pack: thinfilm-active (seed 1)

- world: `../../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 201s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T1915-c24-thinfilm-sighting/pack_ext --seeds 0 1 --frames 80 --no-movie`
- segmentation: matter > 0.07 of robust range [-0.0431, 8.2197], min area 6 px

## Measurements
- components: final 1, mean 1.8, max 6; occupancy final 0.39
- tracks: 42; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.42, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 3, 2], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 1000, default): splits 16, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 9, merge/split ratio 0.562, nucleations 0
- channel total drift (end/start - 1): [-0.0, 7.8066, -27.8379, 78.5834]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 54: holes 0, rim-vs-core 0.46, rim-vs-outside 0.57, heterogeneity 0.25; core [0.788, 0.776, 0.387, 0.619] rim [0.347, 0.869, 0.476, 0.593]
  - track 22 at frame 19: holes 0, rim-vs-core 0.18, rim-vs-outside 0.21, heterogeneity 0.10; core [0.285, 0.875, 0.856, 0.192] rim [0.127, 0.817, 0.807, 0.211]
  - track 39 at frame 74: holes 0, rim-vs-core 0.27, rim-vs-outside 0.44, heterogeneity 0.21; core [0.53, 0.842, 0.385, 0.213] rim [0.285, 0.834, 0.502, 0.209]
  - track 40 at frame 74: holes 0, rim-vs-core 0.26, rim-vs-outside 0.61, heterogeneity 0.22; core [0.615, 0.843, 0.475, 0.789] rim [0.363, 0.882, 0.5, 0.721]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.493, rim/outside 2.96 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.223)
  - radial |p| polar order: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 1.45 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.713)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.16 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.436)
  - radial p_y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 1.15 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.443)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=2700, R_eq 40.94): none; #22 (t=950, R_eq 12.26): none; #39 (t=3700, R_eq 24.32): none; #40 (t=3700, R_eq 34.56): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 5 of 12 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
