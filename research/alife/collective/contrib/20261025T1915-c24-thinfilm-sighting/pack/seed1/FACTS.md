# Evidence pack: thinfilm-active (seed 1)

- world: `../../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 200s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T1915-c24-thinfilm-sighting/pack --seeds 0 1 --frames 80 --no-movie`
- segmentation: matter > 0.11 of robust range [0.0435, 4.1237], min area 6 px

## Measurements
- components: final 5, mean 9.2, max 18; occupancy final 0.27
- tracks: 53; persistent (alive >= 50% of run): 7; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 46.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 5], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0154/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 15, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 14, merge/split ratio 0.933, nucleations 0
- channel total drift (end/start - 1): [0.0, 4.4263, -213.6684, -569.9395]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 44: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.10; core [0.544, 0.949, 0.468, 0.021] rim [0.227, 0.854, 0.467, 0.082]
  - track 41 at frame 49: holes 0, rim-vs-core 0.37, rim-vs-outside 0.32, heterogeneity 0.12; core [0.588, 0.952, 0.317, 0.053] rim [0.241, 0.858, 0.343, 0.11]
  - track 9 at frame 36: holes 0, rim-vs-core 0.18, rim-vs-outside 0.22, heterogeneity 0.08; core [0.397, 0.945, 0.008, 0.531] rim [0.24, 0.863, 0.051, 0.532]
  - track 46 at frame 58: holes 0, rim-vs-core 0.50, rim-vs-outside 0.45, heterogeneity 0.15; core [0.795, 0.963, 0.474, 0.026] rim [0.302, 0.885, 0.465, 0.101]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.618, rim/outside 5.62 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.376)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 2.15 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.888)
  - radial p_x: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.972 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.419)
  - radial p_y: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.926 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=2200, R_eq 10.7): none; #41 (t=2450, R_eq 11.37): none; #9 (t=1800, R_eq 8.74): none; #46 (t=2900, R_eq 14.53): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
