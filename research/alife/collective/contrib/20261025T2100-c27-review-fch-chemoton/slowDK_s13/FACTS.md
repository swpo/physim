# Evidence pack: fch-pchemoton-slowDK0.005 (seed 13)

- world: `../world_slowDK0.005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 357s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27c/world_slowDK0.005.py --out collective/contrib/wip-c27c/slowDK_s13 --seeds 13 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0233, 1.9953], min area 6 px

## Measurements
- components: final 2, mean 2.1, max 5; occupancy final 0.02
- tracks: 17; persistent (alive >= 50% of run): 2; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.09 (1 = constant size)
- enclosures: components with a hole mean 1.65, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [2, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 1, nucleations 2
- channel total drift (end/start - 1): [-0.9904, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 111: holes 1, rim-vs-core 0.17, rim-vs-outside 0.36, heterogeneity 0.04; core [0.763, 1.0, 0.0] rim [0.591, 1.0, 0.0]
  - track 16 at frame 148: holes 1, rim-vs-core 0.17, rim-vs-outside 0.33, heterogeneity 0.04; core [0.742, 1.0, 0.0] rim [0.574, 1.0, 0.0]
  - track 13 at frame 45: holes 4, rim-vs-core 0.07, rim-vs-outside 0.41, heterogeneity 0.04; core [0.517, 0.971, 0.0] rim [0.588, 0.971, 0.0]
  - track 14 at frame 81: holes 0, rim-vs-core 0.14, rim-vs-outside 0.35, heterogeneity 0.04; core [0.729, 0.999, 0.0] rim [0.587, 0.999, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.01, rim/outside 45.1 (aggregate of 12 individuals; 8/12 membrane-like individually; rim level 0.676)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.982)
  - radial catalyst K: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.999 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.0006)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1
- membrane-like channels per top track at mid-life: #10 (t=333, R_eq 12.49, ring): ['amphiphile u+1']; #16 (t=444, R_eq 10.84, ring): ['amphiphile u+1']; #13 (t=135, R_eq 22.74): none; #14 (t=243, R_eq 14.53, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
