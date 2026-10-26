# Evidence pack: fch-pchemoton (seed 4)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 394s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261026T0430-c34-review-chemoton/rerun/seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0212, 1.8384], min area 6 px

## Measurements
- components: final 5, mean 4.5, max 9; occupancy final 0.06
- tracks: 16; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.78 (1 = constant size)
- enclosures: components with a hole mean 1.48, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 4], H1 [2, 2, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1, nucleations 5
- channel total drift (end/start - 1): [-0.4415, 0.742, -0.9081]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.59, heterogeneity 0.18; core [0.906, 0.009, 0.87] rim [0.687, 0.039, 0.589]
  - track 1 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.905, 0.972, 0.0] rim [0.611, 0.972, 0.001]
  - track 13 at frame 106: holes 1, rim-vs-core 0.21, rim-vs-outside 0.39, heterogeneity 0.05; core [0.868, 0.986, 0.0] rim [0.658, 0.986, 0.0]
  - track 14 at frame 161: holes 0, rim-vs-core 0.16, rim-vs-outside 0.41, heterogeneity 0.04; core [0.844, 0.995, 0.0] rim [0.682, 0.995, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 4.72 (aggregate of 27 individuals; 5/27 membrane-like individually; rim level 0.538)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.952 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.81)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.461, rim/outside 1.74 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.0622)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.93): none; #1 (t=303, R_eq 8.04): none; #13 (t=318, R_eq 12.33, ring): ['amphiphile u+1']; #14 (t=483, R_eq 15.01, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
