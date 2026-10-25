# Evidence pack: fch-pchemoton (seed 24)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 746s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261025T1755-c24-review-chemoton/rerun/seed24 --seeds 24 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0204, 1.9534], min area 6 px

## Measurements
- components: final 5, mean 4.1, max 5; occupancy final 0.09
- tracks: 10; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.84 (1 = constant size)
- enclosures: components with a hole mean 1.17, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 3], H1 [3, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.333, nucleations 3
- channel total drift (end/start - 1): [-0.0124, 0.3907, -0.7759]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.58, heterogeneity 0.18; core [0.924, 0.006, 0.851] rim [0.702, 0.039, 0.476]
  - track 6 at frame 138: holes 0, rim-vs-core 0.17, rim-vs-outside 0.42, heterogeneity 0.07; core [0.862, 0.849, 0.002] rim [0.694, 0.853, 0.004]
  - track 7 at frame 138: holes 0, rim-vs-core 0.28, rim-vs-outside 0.10, heterogeneity 0.06; core [0.787, 0.869, 0.0] rim [0.508, 0.868, 0.0]
  - track 1 at frame 52: holes 8, rim-vs-core 0.14, rim-vs-outside 0.46, heterogeneity 0.21; core [0.567, 0.631, 0.001] rim [0.664, 0.698, 0.079]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 2.67 (aggregate of 25 individuals; 6/25 membrane-like individually; rim level 0.552)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.839 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.489)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 1.75 (aggregate of 25 individuals; 7/25 membrane-like individually; rim level 0.157)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.87): none; #6 (t=414, R_eq 15.39, ring): none; #7 (t=414, R_eq 5.75): none; #1 (t=156, R_eq 27.67): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 25 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
