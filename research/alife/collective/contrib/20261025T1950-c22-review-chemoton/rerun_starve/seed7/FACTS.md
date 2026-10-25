# Evidence pack: fch-pchemoton-starve (seed 7)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 366s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T1950-c22-review-chemoton/rerun_starve/seed7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.36 of robust range [-0.0259, 1.7288], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 8; occupancy final 0.02
- tracks: 11; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.62 (1 = constant size)
- enclosures: components with a hole mean 2.24, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 5], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 2, nucleations 6
- channel total drift (end/start - 1): [-0.9073, -0.2999, -0.9998]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 1, rim-vs-core 0.19, rim-vs-outside 0.38, heterogeneity 0.06; core [0.849, 0.949, 0.001] rim [0.656, 0.947, 0.002]
  - track 3 at frame 101: holes 1, rim-vs-core 0.16, rim-vs-outside 0.47, heterogeneity 0.06; core [0.858, 0.88, 0.001] rim [0.697, 0.877, 0.004]
  - track 4 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.53, heterogeneity 0.18; core [0.884, 0.001, 0.742] rim [0.659, 0.012, 0.494]
  - track 9 at frame 106: holes 2, rim-vs-core 0.15, rim-vs-outside 0.56, heterogeneity 0.14; core [0.813, 0.03, 0.22] rim [0.708, 0.033, 0.322]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 11.7 (aggregate of 30 individuals; 7/30 membrane-like individually; rim level 0.597)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.909 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.489)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 2.99 (aggregate of 30 individuals; 5/30 membrane-like individually; rim level 0.0715)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 13.95, ring): ['amphiphile u+1']; #3 (t=303, R_eq 14.43, ring): ['amphiphile u+1']; #4 (t=303, R_eq 12.96): none; #9 (t=318, R_eq 18.42): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
