# Evidence pack: fch-pchemoton-slowDK0.005 (seed 0)

- world: `../world_slowDK0.005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 360s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27c/world_slowDK0.005.py --out collective/contrib/wip-c27c/slowDK_s0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0253, 1.8958], min area 6 px

## Measurements
- components: final 3, mean 3.1, max 6; occupancy final 0.01
- tracks: 13; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.47 (1 = constant size)
- enclosures: components with a hole mean 1.68, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 2, nucleations 4
- channel total drift (end/start - 1): [-0.9904, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.18, rim-vs-outside 0.42, heterogeneity 0.05; core [0.883, 1.0, 0.0] rim [0.702, 1.0, 0.0]
  - track 3 at frame 101: holes 1, rim-vs-core 0.20, rim-vs-outside 0.40, heterogeneity 0.05; core [0.886, 1.0, 0.0] rim [0.688, 1.0, 0.0]
  - track 12 at frame 138: holes 0, rim-vs-core 0.18, rim-vs-outside 0.29, heterogeneity 0.06; core [0.801, 1.0, 0.0] rim [0.62, 1.0, 0.0]
  - track 9 at frame 45: holes 7, rim-vs-core 0.01, rim-vs-outside 0.50, heterogeneity 0.04; core [0.677, 0.971, 0.0] rim [0.688, 0.971, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 13.2 (aggregate of 18 individuals; 6/18 membrane-like individually; rim level 0.698)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.982)
  - radial catalyst K: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.0006)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 10.88, ring): ['amphiphile u+1']; #3 (t=303, R_eq 10.85, ring): ['amphiphile u+1']; #12 (t=414, R_eq 9.39): none; #9 (t=135, R_eq 28.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
