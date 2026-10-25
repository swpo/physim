# Evidence pack: fch-pchemoton (seed 31)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 502s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1033-c10-review-chemoton/world_ctl.py --out collective/contrib/20261025T1033-c10-review-chemoton/nogate_lowD --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0197, 1.9267], min area 6 px

## Measurements
- components: final 5, mean 4.6, max 5; occupancy final 0.12
- tracks: 6; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.81 (1 = constant size)
- enclosures: components with a hole mean 2.77, final 3; holes at thresholds 0.2/0.35/0.5 final [9, 9, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 8, 4], H1 [10, 10, 3]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0405/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.2845, -0.7014, -0.346]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 3, rim-vs-core 0.14, rim-vs-outside 0.46, heterogeneity 0.15; core [0.836, 0.23, 0.119] rim [0.694, 0.23, 0.126]
  - track 1 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.30, heterogeneity 0.17; core [0.898, 0.183, 0.193] rim [0.615, 0.192, 0.194]
  - track 2 at frame 101: holes 4, rim-vs-core 0.15, rim-vs-outside 0.47, heterogeneity 0.17; core [0.821, 0.245, 0.11] rim [0.696, 0.21, 0.187]
  - track 4 at frame 134: holes 0, rim-vs-core 0.19, rim-vs-outside 0.41, heterogeneity 0.15; core [0.848, 0.269, 0.019] rim [0.7, 0.229, 0.134]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 4.58 (aggregate of 28 individuals; 5/28 membrane-like individually; rim level 0.566)
  - radial precursor P: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.02 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.231)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 1.23 (aggregate of 28 individuals; 12/28 membrane-like individually; rim level 0.173)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 20.4): none; #1 (t=303, R_eq 9.95): ['catalyst K']; #2 (t=303, R_eq 20.01): ['catalyst K']; #4 (t=402, R_eq 19.2, ring): ['amphiphile u+1', 'catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
