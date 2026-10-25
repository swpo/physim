# Evidence pack: thinfilm-active (seed 8)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 157s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2103-c21-review-thinfilm/rerun_default --seeds 7 8 --frames 80 --no-movie`
- segmentation: matter > 0.10 of robust range [0.0496, 4.5204], min area 6 px

## Measurements
- components: final 7, mean 9.8, max 17; occupancy final 0.26
- tracks: 60; persistent (alive >= 50% of run): 6; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.86 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 4], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0218/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.889, nucleations 0
- channel total drift (end/start - 1): [0.0, 4.6273, 233.9988, -558.53]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 44: holes 0, rim-vs-core 0.26, rim-vs-outside 0.19, heterogeneity 0.08; core [0.416, 0.932, 0.879, 0.172] rim [0.179, 0.835, 0.83, 0.201]
  - track 21 at frame 45: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.11; core [0.545, 0.949, 0.119, 0.171] rim [0.223, 0.857, 0.173, 0.207]
  - track 16 at frame 43: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.11; core [0.545, 0.953, 0.743, 0.066] rim [0.252, 0.862, 0.685, 0.106]
  - track 44 at frame 53: holes 0, rim-vs-core 0.27, rim-vs-outside 0.19, heterogeneity 0.09; core [0.421, 0.932, 0.019, 0.36] rim [0.176, 0.834, 0.069, 0.378]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.607, rim/outside 5.34 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.364)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 1.99 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.896)
  - radial p_x: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 1 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.511)
  - radial p_y: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 0.94 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.37)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=2200, R_eq 9.32): none; #21 (t=2250, R_eq 11.06): none; #16 (t=2150, R_eq 10.98): none; #44 (t=2650, R_eq 9.46): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
