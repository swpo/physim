# Evidence pack: fch-pchemoton (seed 5)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 361s; status ok
- command: `python -m labkit.run collective/contrib/c17-chemoton-wip/world.py --out collective/contrib/c17-chemoton-wip/rerun/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [-0.0201, 1.7267], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 6; occupancy final 0.05
- tracks: 6; persistent (alive >= 50% of run): 6; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.57 (1 = constant size)
- enclosures: components with a hole mean 0.94, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 8], H1 [1, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [-0.4551, 0.7817, -0.9249]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.15, rim-vs-outside 0.39, heterogeneity 0.07; core [0.789, 0.975, 0.0] rim [0.64, 0.976, 0.001]
  - track 1 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.28, heterogeneity 0.06; core [0.865, 0.999, 0.0] rim [0.585, 0.999, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.06; core [0.869, 0.974, 0.0] rim [0.579, 0.973, 0.001]
  - track 3 at frame 101: holes 1, rim-vs-core 0.15, rim-vs-outside 0.46, heterogeneity 0.07; core [0.819, 0.9, 0.002] rim [0.673, 0.89, 0.005]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 6.33 (aggregate of 36 individuals; 6/36 membrane-like individually; rim level 0.486)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.979 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.833)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.541, rim/outside 1.72 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.071)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 10.63): none; #1 (t=303, R_eq 8.02): none; #2 (t=303, R_eq 8.08): none; #3 (t=303, R_eq 14.21, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
