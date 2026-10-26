# Evidence pack: phoretic-colloids (seed 7)

- world: `../../../20261026T0529-c33-phoretic-swimdivide-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 372s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0529-c33-phoretic-swimdivide-claim/world.py --out collective/contrib/20261026T0640-c38-review-phoretic-swimdivide/rerun/seed7 --seeds 7 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.588], min area 6 px

## Measurements
- components: final 12, mean 16.7, max 26; occupancy final 0.06
- tracks: 634; persistent (alive >= 50% of run): 0; longest 603 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 15, 9], H1 [0, 0, 0]
- motion: 115 long-lived tracks moved >= 1 body length; max speed 0.591/time; max body lengths 8.4
- replication (lineage window K = 20 frames = time 10, default): splits 58, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 8, merges 83, merge/split ratio 1.43, nucleations 435
- channel total drift (end/start - 1): [0.5186, 0.21, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 298 at frame 861: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.09; core [0.832, 0.041, 0.349] rim [0.606, 0.075, 0.307]
  - track 150 at frame 484: holes 0, rim-vs-core 0.29, rim-vs-outside 0.30, heterogeneity 0.18; core [0.809, 0.251, 0.623] rim [0.546, 0.235, 0.5]
  - track 50 at frame 350: holes 0, rim-vs-core 0.23, rim-vs-outside 0.26, heterogeneity 0.18; core [0.537, 0.52, 0.513] rim [0.469, 0.316, 0.432]
  - track 589 at frame 1546: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.24; core [0.731, 0.363, 0.642] rim [0.454, 0.32, 0.503]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 19.7 (aggregate of 75 individuals; 2/75 membrane-like individually; rim level 0.643)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 16.9 (aggregate of 75 individuals; 22/75 membrane-like individually; rim level 0.298)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 3.04 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.595)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #298 (t=430.5, R_eq 2.33): ['B density']; #150 (t=242, R_eq 3.99): ['B density']; #50 (t=175, R_eq 3.83): ['A density']; #589 (t=773, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
