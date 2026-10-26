# Evidence pack: fch-pchemoton (seed 11)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 360s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/wip-c31/chem/rerun --seeds 11 --frames 200 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0218, 1.8764], min area 6 px

## Measurements
- components: final 1, mean 1.6, max 3; occupancy final 0.01
- tracks: 14; persistent (alive >= 50% of run): 0; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.53, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [1, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 1.67, nucleations 3
- channel total drift (end/start - 1): [-0.9903, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 153: holes 0, rim-vs-core 0.18, rim-vs-outside 0.47, heterogeneity 0.05; core [0.972, 1.0, 0.0] rim [0.795, 1.0, 0.0]
  - track 12 at frame 153: holes 0, rim-vs-core 0.25, rim-vs-outside 0.08, heterogeneity 0.05; core [0.824, 1.0, 0.0] rim [0.578, 1.0, 0.0]
  - track 4 at frame 50: holes 8, rim-vs-core 0.08, rim-vs-outside 0.56, heterogeneity 0.04; core [0.68, 0.984, 0.0] rim [0.758, 0.984, 0.0]
  - track 5 at frame 94: holes 0, rim-vs-core 0.19, rim-vs-outside 0.42, heterogeneity 0.05; core [0.961, 1.0, 0.0] rim [0.773, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.89 (aggregate of 9 individuals; 1/9 membrane-like individually; rim level 0.769)
  - radial precursor P: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.988)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 1 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.0004)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=459, R_eq 14.35, ring): none; #12 (t=459, R_eq 5.23): none; #4 (t=150, R_eq 34.79): none; #5 (t=282, R_eq 17.89, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 9 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
