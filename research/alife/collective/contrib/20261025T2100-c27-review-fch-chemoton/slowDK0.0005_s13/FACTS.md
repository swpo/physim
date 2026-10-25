# Evidence pack: fch-pchemoton-slowDK0.0005 (seed 13)

- world: `../world_slowDK0.0005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 354s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27c/world_slowDK0.0005.py --out collective/contrib/wip-c27c/slowDK0.0005_s13 --seeds 13 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0202, 1.9953], min area 6 px

## Measurements
- components: final 4, mean 2.8, max 6; occupancy final 0.13
- tracks: 31; persistent (alive >= 50% of run): 2; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.22 (1 = constant size)
- enclosures: components with a hole mean 1.77, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 2], H1 [6, 5, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 10, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.9, nucleations 2
- channel total drift (end/start - 1): [0.2959, -0.6994, -0.3452]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 138: holes 2, rim-vs-core 0.13, rim-vs-outside 0.13, heterogeneity 0.13; core [0.556, 0.193, 0.211] rim [0.507, 0.234, 0.095]
  - track 23 at frame 52: holes 6, rim-vs-core 0.09, rim-vs-outside 0.41, heterogeneity 0.16; core [0.49, 0.241, 0.142] rim [0.574, 0.236, 0.157]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 10.8 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.541)
  - radial precursor P: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 0.966 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.226)
  - radial catalyst K: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.2 (aggregate of 17 individuals; 1/17 membrane-like individually; rim level 0.163)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=414, R_eq 22, ring): none; #25 (t=414, R_eq 19.97): none; #28 (t=378, R_eq 26.4): none; #23 (t=156, R_eq 27.73): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 17 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
