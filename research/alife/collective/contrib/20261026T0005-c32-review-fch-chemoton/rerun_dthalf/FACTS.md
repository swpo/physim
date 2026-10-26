# Evidence pack: fch-pchemoton-dthalf (seed 5)

- world: `../world_dthalf.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 600 steps x dt 0.005 = time 600; grid [192, 192]; wall 624s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0005-c32-review-fch-chemoton/world_dthalf.py --out collective/contrib/20261026T0005-c32-review-fch-chemoton/rerun_dthalf --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0254, 1.8677], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 7; occupancy final 0.01
- tracks: 15; persistent (alive >= 50% of run): 4; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.41 (1 = constant size)
- enclosures: components with a hole mean 1.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1, nucleations 4
- channel total drift (end/start - 1): [-0.9903, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 103: holes 0, rim-vs-core 0.33, rim-vs-outside 0.18, heterogeneity 0.06; core [0.909, 1.0, 0.0] rim [0.581, 1.0, 0.0]
  - track 9 at frame 108: holes 1, rim-vs-core 0.19, rim-vs-outside 0.39, heterogeneity 0.04; core [0.875, 1.0, 0.0] rim [0.687, 1.0, 0.0]
  - track 10 at frame 126: holes 0, rim-vs-core 0.18, rim-vs-outside 0.29, heterogeneity 0.06; core [0.804, 1.0, 0.0] rim [0.622, 1.0, 0.0]
  - track 14 at frame 138: holes 0, rim-vs-core 0.28, rim-vs-outside 0.31, heterogeneity 0.06; core [0.923, 1.0, 0.0] rim [0.642, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.23 (aggregate of 26 individuals; 5/26 membrane-like individually; rim level 0.71)
  - radial precursor P: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.983)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.0006)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=309, R_eq 5.23): none; #9 (t=324, R_eq 10.08, ring): ['amphiphile u+1']; #10 (t=378, R_eq 9.34): none; #14 (t=414, R_eq 7.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 26 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
