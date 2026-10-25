# Evidence pack: nrch (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 182 frames x 1000 steps x dt 0.05 = time 9050; grid [192, 192]; wall 1057s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1342-c13-review-crystal-ramp/world.py --out collective/contrib/20261025T1342-c13-review-crystal-ramp/rerun/seed2 --seeds 2 --spf 1000 --frames 181 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.9077, 0.928], min area 6 px

## Measurements
- components: final 24, mean 23.6, max 36; occupancy final 0.27
- tracks: 476; persistent (alive >= 50% of run): 21; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 42 long-lived tracks moved >= 1 body length; max speed 0.269/time; max body lengths 92.4
- replication (lineage window K = 20 frames = time 1000, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.333, nucleations 462
- channel total drift (end/start - 1): [0.1565, 4.7143]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 309 at frame 108: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.922, 0.378] rim [0.658, 0.423]
  - track 323 at frame 110: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.923, 0.381] rim [0.664, 0.417]
  - track 338 at frame 114: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.921, 0.387] rim [0.655, 0.425]
  - track 361 at frame 116: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.924, 0.388] rim [0.657, 0.423]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [30, 61, 91, 120, 151, 181]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 8.73 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.796)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.958 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.573)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #309 (t=5400, R_eq 10.43): none; #323 (t=5500, R_eq 10.65): none; #338 (t=5700, R_eq 11.13): none; #361 (t=5800, R_eq 10.85): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
