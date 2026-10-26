# Evidence pack: phoretic-colloids (seed 7)

- world: `../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0424-c29-review-phoretic/world.py --out collective/contrib/20261026T0424-c29-review-phoretic/rerun --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6104], min area 6 px

## Measurements
- components: final 18, mean 22.5, max 38; occupancy final 0.08
- tracks: 208; persistent (alive >= 50% of run): 7; longest 355 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 19, 16], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.372/time; max body lengths 6.7
- replication (lineage window K = 20 frames = time 10, default): splits 7, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 35, merge/split ratio 5, nucleations 159
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 198: holes 0, rim-vs-core 0.10, rim-vs-outside 0.44, heterogeneity 0.15; core [0.677, 0.496, 0.584] rim [0.591, 0.533, 0.536]
  - track 73 at frame 198: holes 0, rim-vs-core 0.33, rim-vs-outside 0.30, heterogeneity 0.15; core [0.87, 0.281, 0.652] rim [0.573, 0.262, 0.521]
  - track 204 at frame 390: holes 0, rim-vs-core 0.38, rim-vs-outside 0.26, heterogeneity 0.27; core [0.68, 0.56, 0.823] rim [0.399, 0.413, 0.621]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 117 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 14.5 (aggregate of 117 individuals; 2/117 membrane-like individually; rim level 0.662)
  - radial B density: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 12.4 (aggregate of 117 individuals; 46/117 membrane-like individually; rim level 0.415)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 2.65 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.568)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #35 (t=112.5, R_eq 2.33): ['B density']; #14 (t=99, R_eq 3.91): none; #73 (t=99, R_eq 4.15): none; #204 (t=195, R_eq 5.81): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
