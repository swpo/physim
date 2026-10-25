# Evidence pack: fch-pchemoton (seed 9)

- world: `../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 514s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261025T1820-c21-review-fch-chemoton/rerun --seeds 9 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0204, 1.9614], min area 6 px

## Measurements
- components: final 4, mean 3.7, max 7; occupancy final 0.13
- tracks: 19; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.44 (1 = constant size)
- enclosures: components with a hole mean 2.74, final 3; holes at thresholds 0.2/0.35/0.5 final [9, 8, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 8, 3], H1 [11, 10, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 60, default): splits 6, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.833, nucleations 3
- channel total drift (end/start - 1): [0.436, 0.0589, -0.6507]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 109: holes 4, rim-vs-core 0.18, rim-vs-outside 0.58, heterogeneity 0.17; core [0.896, 0.096, 0.227] rim [0.757, 0.077, 0.34]
  - track 17 at frame 133: holes 0, rim-vs-core 0.35, rim-vs-outside 0.59, heterogeneity 0.15; core [0.919, 0.019, 0.728] rim [0.757, 0.057, 0.425]
  - track 18 at frame 133: holes 1, rim-vs-core 0.21, rim-vs-outside 0.24, heterogeneity 0.06; core [0.841, 0.147, 0.032] rim [0.638, 0.134, 0.064]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 4.53 (aggregate of 23 individuals; 5/23 membrane-like individually; rim level 0.691)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.468 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.217)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 3.61, rim/outside 2.69 (aggregate of 23 individuals; 15/23 membrane-like individually; rim level 0.279)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #2 (t=303, R_eq 22.33): ['catalyst K']; #12 (t=327, R_eq 20.45): ['catalyst K']; #17 (t=399, R_eq 19.79, ring): ['amphiphile u+1', 'catalyst K']; #18 (t=399, R_eq 13.6, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 23 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
