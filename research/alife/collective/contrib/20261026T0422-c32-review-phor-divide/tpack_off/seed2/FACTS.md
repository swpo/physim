# Evidence pack: phoretic-colloids (seed 2)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0422-c32-review-phor-divide/world.py --out collective/contrib/20261026T0422-c32-review-phor-divide/tpack_off --seeds 2 3 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7937], min area 6 px

## Measurements
- components: final 9, mean 14.1, max 30; occupancy final 0.06
- tracks: 156; persistent (alive >= 50% of run): 4; longest 641 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 9, 6], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.424/time; max body lengths 8.7
- replication (lineage window K = 20 frames = time 10, default): splits 7, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 5, merges 28, merge/split ratio 4, nucleations 114
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 108 at frame 484: holes 0, rim-vs-core 0.25, rim-vs-outside 0.26, heterogeneity 0.12; core [0.779, 0.189, 0.381] rim [0.541, 0.231, 0.332]
  - track 132 at frame 511: holes 0, rim-vs-core 0.31, rim-vs-outside 0.30, heterogeneity 0.16; core [0.817, 0.27, 0.602] rim [0.54, 0.309, 0.475]
  - track 128 at frame 484: holes 0, rim-vs-core 0.39, rim-vs-outside 0.29, heterogeneity 0.22; core [0.8, 0.452, 0.779] rim [0.468, 0.417, 0.578]
  - track 152 at frame 787: holes 0, rim-vs-core 0.26, rim-vs-outside 0.23, heterogeneity 0.25; core [0.653, 0.481, 0.583] rim [0.435, 0.401, 0.471]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 23.7 (aggregate of 82 individuals; 1/82 membrane-like individually; rim level 0.671)
  - radial B density: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 17.4 (aggregate of 82 individuals; 41/82 membrane-like individually; rim level 0.378)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 3.18 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.567)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #108 (t=242, R_eq 2.71): ['B density']; #132 (t=255.5, R_eq 4.3): ['B density']; #128 (t=242, R_eq 5.67): ['B density']; #152 (t=393.5, R_eq 4.18): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
