# Evidence pack: nrch (seed 5)

- world: `../../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 2000 steps x dt 0.05 = time 12000; grid [192, 192]; wall 1938s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0958-c12-review-nrch/world.py --out collective/contrib/20261025T0958-c12-review-nrch/rerun_dt2/seed5 --seeds 5 --frames 120 --spf 2000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0524, 1.0791], min area 6 px

## Measurements
- components: final 5, mean 5.5, max 15; occupancy final 0.22
- tracks: 51; persistent (alive >= 50% of run): 5; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0941/time; max body lengths 20.4
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.714, nucleations 32
- channel total drift (end/start - 1): [0.0, -511.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 79: holes 0, rim-vs-core 0.26, rim-vs-outside 0.43, heterogeneity 0.19; core [0.94, 0.394] rim [0.685, 0.365]
  - track 42 at frame 85: holes 0, rim-vs-core 0.24, rim-vs-outside 0.42, heterogeneity 0.18; core [0.924, 0.331] rim [0.687, 0.364]
  - track 27 at frame 68: holes 0, rim-vs-core 0.21, rim-vs-outside 0.38, heterogeneity 0.16; core [0.905, 0.368] rim [0.704, 0.415]
  - track 44 at frame 87: holes 0, rim-vs-core 0.15, rim-vs-outside 0.57, heterogeneity 0.20; core [0.965, 0.459] rim [0.817, 0.429]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 6.35 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.813)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.979 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.538)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #35 (t=7900, R_eq 16.41): none; #42 (t=8500, R_eq 16.41): none; #27 (t=6800, R_eq 11.83): none; #44 (t=8700, R_eq 23.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
