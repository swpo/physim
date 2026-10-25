# Evidence pack: fch-pchemoton-starve (seed 24)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 744s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T1755-c24-review-chemoton/rerun_starve/seed24 --seeds 24 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0229, 1.9534], min area 6 px

## Measurements
- components: final 3, mean 3.7, max 5; occupancy final 0.02
- tracks: 12; persistent (alive >= 50% of run): 1; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.31 (1 = constant size)
- enclosures: components with a hole mean 1.29, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 3], H1 [2, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1, nucleations 3
- channel total drift (end/start - 1): [-0.902, -0.3272, -0.9881]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.64, heterogeneity 0.16; core [0.932, 0.0, 0.919] rim [0.712, 0.01, 0.634]
  - track 1 at frame 50: holes 8, rim-vs-core 0.12, rim-vs-outside 0.47, heterogeneity 0.22; core [0.595, 0.697, 0.001] rim [0.671, 0.717, 0.095]
  - track 6 at frame 111: holes 0, rim-vs-core 0.17, rim-vs-outside 0.42, heterogeneity 0.07; core [0.862, 0.667, 0.001] rim [0.695, 0.664, 0.002]
  - track 7 at frame 111: holes 0, rim-vs-core 0.26, rim-vs-outside 0.09, heterogeneity 0.06; core [0.772, 0.674, 0.0] rim [0.509, 0.673, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 4.21 (aggregate of 22 individuals; 7/22 membrane-like individually; rim level 0.634)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.875 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.39)
  - radial catalyst K: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 2.36 (aggregate of 22 individuals; 8/22 membrane-like individually; rim level 0.132)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.85): none; #1 (t=150, R_eq 28.05): ['catalyst K']; #6 (t=333, R_eq 15.03, ring): none; #7 (t=333, R_eq 5.56): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
