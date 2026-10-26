# Evidence pack: phoretic-colloids (seed 9)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 159s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1845-c43-review-phoretic/world.py --out collective/contrib/20261026T1845-c43-review-phoretic/rerun/seed9 --seeds 9 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6981], min area 6 px

## Measurements
- components: final 10, mean 14.6, max 22; occupancy final 0.05
- tracks: 323; persistent (alive >= 50% of run): 4; longest 576 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 13, 6], H1 [0, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.544/time; max body lengths 7.1
- replication (lineage window K = 20 frames = time 10, default): splits 21, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 38, merge/split ratio 1.81, nucleations 243
- channel total drift (end/start - 1): [0.5257, 0.17, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 336: holes 0, rim-vs-core 0.36, rim-vs-outside 0.29, heterogeneity 0.19; core [0.856, 0.168, 0.6] rim [0.53, 0.257, 0.475]
  - track 99 at frame 437: holes 0, rim-vs-core 0.24, rim-vs-outside 0.33, heterogeneity 0.09; core [0.883, 0.009, 0.486] rim [0.653, 0.043, 0.41]
  - track 19 at frame 289: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.17; core [0.88, 0.209, 0.566] rim [0.586, 0.143, 0.462]
  - track 284 at frame 739: holes 0, rim-vs-core 0.25, rim-vs-outside 0.24, heterogeneity 0.19; core [0.732, 0.417, 0.403] rim [0.51, 0.311, 0.362]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 15 (aggregate of 72 individuals; 2/72 membrane-like individually; rim level 0.657)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 14.9 (aggregate of 72 individuals; 32/72 membrane-like individually; rim level 0.346)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 2.69 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.557)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=168, R_eq 3.95): ['B density']; #99 (t=218.5, R_eq 3.09): ['B density']; #19 (t=144.5, R_eq 3.78): none; #284 (t=369.5, R_eq 2.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
