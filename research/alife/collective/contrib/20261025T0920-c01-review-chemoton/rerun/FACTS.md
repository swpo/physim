# Evidence pack: fch-pchemoton (seed 3)

- world: `../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 376s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261025T0920-c01-review-chemoton/rerun --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0212, 1.968], min area 6 px

## Measurements
- components: final 4, mean 3.6, max 7; occupancy final 0.06
- tracks: 20; persistent (alive >= 50% of run): 4; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.50 (1 = constant size)
- enclosures: components with a hole mean 2.20, final 2; holes at thresholds 0.2/0.35/0.5 final [5, 3, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 3], H1 [6, 6, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 60, default): splits 6, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.667, nucleations 3
- channel total drift (end/start - 1): [-0.405, 0.7094, -0.8952]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 109: holes 1, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.05; core [0.878, 0.994, 0.0] rim [0.668, 0.994, 0.0]
  - track 14 at frame 111: holes 4, rim-vs-core 0.14, rim-vs-outside 0.57, heterogeneity 0.17; core [0.825, 0.047, 0.401] rim [0.693, 0.044, 0.449]
  - track 18 at frame 148: holes 0, rim-vs-core 0.16, rim-vs-outside 0.41, heterogeneity 0.05; core [0.849, 0.962, 0.0] rim [0.686, 0.961, 0.001]
  - track 19 at frame 148: holes 0, rim-vs-core 0.25, rim-vs-outside 0.09, heterogeneity 0.05; core [0.757, 0.966, 0.0] rim [0.508, 0.965, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 5.86 (aggregate of 22 individuals; 5/22 membrane-like individually; rim level 0.692)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.898 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.777)
  - radial catalyst K: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.51, rim/outside 6.49 (aggregate of 22 individuals; 5/22 membrane-like individually; rim level 0.125)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #10 (t=327, R_eq 12.21, ring): ['amphiphile u+1']; #14 (t=333, R_eq 19.93): ['catalyst K']; #18 (t=444, R_eq 14.84, ring): none; #19 (t=444, R_eq 5.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
