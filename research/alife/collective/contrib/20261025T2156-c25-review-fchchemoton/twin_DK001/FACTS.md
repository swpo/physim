# Evidence pack: fch-pchemoton-c25 (seed 7)

- world: `../world_c25.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 524s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2156-c25-review-fchchemoton/world_c25.py --out collective/contrib/20261025T2156-c25-review-fchchemoton/twin_DK001 --seeds 7 --no-movie`
- segmentation: matter > 0.36 of robust range [-0.0205, 1.7186], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 8; occupancy final 0.13
- tracks: 15; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.60 (1 = constant size)
- enclosures: components with a hole mean 2.81, final 3; holes at thresholds 0.2/0.35/0.5 final [4, 4, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 8, 5], H1 [4, 4, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 2, nucleations 6
- channel total drift (end/start - 1): [0.5997, -0.5998, -0.3899]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 1, rim-vs-core 0.17, rim-vs-outside 0.48, heterogeneity 0.14; core [0.866, 0.169, 0.183] rim [0.699, 0.192, 0.155]
  - track 4 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.40, heterogeneity 0.17; core [0.915, 0.15, 0.263] rim [0.661, 0.153, 0.226]
  - track 12 at frame 106: holes 2, rim-vs-core 0.08, rim-vs-outside 0.50, heterogeneity 0.15; core [0.734, 0.167, 0.265] rim [0.705, 0.177, 0.189]
  - track 13 at frame 106: holes 1, rim-vs-core 0.12, rim-vs-outside 0.53, heterogeneity 0.15; core [0.813, 0.14, 0.266] rim [0.721, 0.155, 0.186]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 4.58 (aggregate of 30 individuals; 9/30 membrane-like individually; rim level 0.411)
  - radial precursor P: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 1.11 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.323)
  - radial catalyst K: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.72, rim/outside 0.91 (aggregate of 30 individuals; 4/30 membrane-like individually; rim level 0.157)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 17.35, ring): ['amphiphile u+1']; #4 (t=303, R_eq 10.63): none; #12 (t=318, R_eq 19.07): none; #13 (t=318, R_eq 18, ring): ['amphiphile u+1', 'catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
