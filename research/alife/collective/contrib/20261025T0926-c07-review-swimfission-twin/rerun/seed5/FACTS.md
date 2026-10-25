# Evidence pack: swimfission-rd-twin (seed 5)

- world: `../../../20261025T0658-c01-swimfission-rd-twin/twin_sf.py`, family `chemotaxis`
- parent: toxforage; mutation: shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 66s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0658-c01-swimfission-rd-twin/twin_sf.py --out collective/contrib/_c07rev10/rerun/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9999], min area 6 px

## Measurements
- components: final 6, mean 4.8, max 24; occupancy final 0.08
- tracks: 114; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 6], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.634/time; max body lengths 13.4
- replication (lineage window K = 20 frames = time 120, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.667, nucleations 98
- channel total drift (end/start - 1): [0.535, 0.522, 0.4568, -0.0902]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 86: holes 0, rim-vs-core 0.35, rim-vs-outside 1.05, heterogeneity 0.23; core [0.998, 0.942, 0.763, 0.018] rim [0.838, 0.751, 0.598, 0.195]
  - track 101 at frame 163: holes 0, rim-vs-core 0.52, rim-vs-outside 0.57, heterogeneity 0.23; core [0.974, 0.749, 0.576, 0.133] rim [0.616, 0.528, 0.427, 0.399]
  - track 102 at frame 173: holes 0, rim-vs-core 0.47, rim-vs-outside 0.74, heterogeneity 0.24; core [0.994, 0.831, 0.644, 0.088] rim [0.697, 0.595, 0.501, 0.325]
  - track 103 at frame 173: holes 0, rim-vs-core 0.49, rim-vs-outside 0.74, heterogeneity 0.24; core [0.993, 0.844, 0.661, 0.083] rim [0.684, 0.596, 0.5, 0.331]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.691, rim/outside 11 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.601)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 4.48 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.5)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 3.89 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.419)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.67, rim/outside 0.878 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.829)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #79 (t=516, R_eq 23.19): none; #101 (t=978, R_eq 9.51): none; #102 (t=1038, R_eq 10.19): none; #103 (t=1038, R_eq 10.54): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
