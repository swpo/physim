# Evidence pack: fch-pchemoton-dthalf (seed 2)

- world: `../world_dthalf.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 600 steps x dt 0.005 = time 600; grid [192, 192]; wall 604s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0005-c32-review-fch-chemoton/world_dthalf.py --out collective/contrib/20261026T0005-c32-review-fch-chemoton/rerun_dthalf_s2 --seeds 2 --frames 200 --no-movie`
- segmentation: matter > 0.37 of robust range [-0.0248, 1.65], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 7; occupancy final 0.02
- tracks: 9; persistent (alive >= 50% of run): 5; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.27 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 5], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 7
- channel total drift (end/start - 1): [-0.9904, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 103: holes 0, rim-vs-core 0.28, rim-vs-outside 0.31, heterogeneity 0.06; core [0.905, 1.0, 0.0] rim [0.625, 1.0, 0.0]
  - track 4 at frame 103: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.901, 1.0, 0.0] rim [0.615, 1.0, 0.0]
  - track 6 at frame 103: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.06; core [0.887, 1.0, 0.0] rim [0.598, 1.0, 0.0]
  - track 7 at frame 109: holes 0, rim-vs-core 0.18, rim-vs-outside 0.28, heterogeneity 0.06; core [0.78, 1.0, 0.0] rim [0.6, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 10.7 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.633)
  - radial precursor P: flat profile (no radial structure; level 0.982; aggregate of 30 individuals)
  - radial catalyst K: flat profile (no radial structure; level 0.0006; aggregate of 30 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=309, R_eq 7.4): none; #4 (t=309, R_eq 7.48): none; #6 (t=309, R_eq 7.55): none; #7 (t=327, R_eq 9.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
