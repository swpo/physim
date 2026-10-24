# Evidence pack: sporecell3-det (seed 1)

- world: `../../../worlds/sporecell3-det/world.py`, family `particle`
- parent: sporecell3; mutation: promoted gate settings: surface detachment k_det=0.05 for particles with < 60 matter neighbours (dt-converged release route)
- run: 101 frames x 100 steps x dt 0.02 = time 200; grid [128, 128]; wall 465s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell3-det/world.py --out threads/particle-life/packs/sporecell3-det --seeds 0 1 --frames 100 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 7.7159], min area 6 px

## Measurements
- components: final 14, mean 7.1, max 14; occupancy final 0.02
- tracks: 24; persistent (alive >= 50% of run): 8; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 16, 10], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0443/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 40, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 24
- channel total drift (end/start - 1): [-0.8892, 126.3, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.26, rim-vs-outside 0.39, heterogeneity 0.04; core [0.002, 1.0, 0.0, 0.0] rim [0.012, 0.744, 0.0, 0.0]
  - track 1 at frame 63: holes 0, rim-vs-core 0.23, rim-vs-outside 0.36, heterogeneity 0.05; core [0.059, 0.994, 0.0, 0.0] rim [0.038, 0.761, 0.0, 0.0]
  - track 3 at frame 64: holes 0, rim-vs-core 0.22, rim-vs-outside 0.37, heterogeneity 0.04; core [0.002, 0.998, 0.0, 0.0] rim [0.008, 0.775, 0.0, 0.0]
  - track 4 at frame 65: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.05; core [0.006, 0.999, 0.0, 0.0] rim [0.018, 0.68, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 41 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial F food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 0.504 (aggregate of 41 individuals; 1/41 membrane-like individually; rim level 0.0306)
  - radial C0 core kind 0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 11.6 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.789)
  - radial M membrane: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 1.98 (aggregate of 41 individuals; 5/41 membrane-like individually; rim level 0.0136)
  - radial C1 core kind 1: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 2.71 (aggregate of 41 individuals; 1/41 membrane-like individually; rim level 0.217)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=124, R_eq 4.37): none; #1 (t=126, R_eq 3.78): none; #3 (t=128, R_eq 3.95): none; #4 (t=130, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
