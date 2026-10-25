# Evidence pack: fch-pchemoton (seed 8)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 382s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out /tmp/claude-0/c28fch/fed --seeds 7 8 --frames 200 --no-movie`
- segmentation: matter > 0.36 of robust range [-0.0196, 1.7088], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 6; occupancy final 0.12
- tracks: 7; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.96 (1 = constant size)
- enclosures: components with a hole mean 0.95, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 3, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 10, 5], H1 [3, 2, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [0.4241, -0.0939, -0.591]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.40, heterogeneity 0.06; core [0.892, 0.933, 0.0] rim [0.652, 0.932, 0.001]
  - track 3 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.60, heterogeneity 0.17; core [0.918, 0.006, 0.823] rim [0.701, 0.057, 0.366]
  - track 4 at frame 101: holes 0, rim-vs-core 0.55, rim-vs-outside 0.49, heterogeneity 0.17; core [0.898, 0.011, 0.786] rim [0.656, 0.064, 0.296]
  - track 5 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.42, heterogeneity 0.20; core [0.868, 0.029, 0.639] rim [0.649, 0.124, 0.201]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.537, rim/outside 3.22 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.325)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.816 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.434)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.414, rim/outside 2.12 (aggregate of 30 individuals; 5/30 membrane-like individually; rim level 0.0946)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=303, R_eq 11.58): none; #3 (t=303, R_eq 15.14, ring): ['catalyst K']; #4 (t=303, R_eq 13.39): none; #5 (t=303, R_eq 13.16): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
