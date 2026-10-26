# Evidence pack: fch-pchemoton-dthalf (seed 0)

- world: `../world_dthalf.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 600 steps x dt 0.005 = time 600; grid [192, 192]; wall 612s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0005-c32-review-fch-chemoton/world_dthalf.py --out collective/contrib/20261026T0005-c32-review-fch-chemoton/rerun_dthalf_s0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.022, 1.9511], min area 6 px

## Measurements
- components: final 5, mean 4.8, max 6; occupancy final 0.05
- tracks: 25; persistent (alive >= 50% of run): 4; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.32 (1 = constant size)
- enclosures: components with a hole mean 1.07, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 3], H1 [3, 3, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 8, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.75, nucleations 3
- channel total drift (end/start - 1): [-0.505, 0.7525, -0.9107]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 138: holes 0, rim-vs-core 0.39, rim-vs-outside 0.66, heterogeneity 0.16; core [0.944, 0.0, 0.951] rim [0.761, 0.03, 0.607]
  - track 14 at frame 138: holes 0, rim-vs-core 0.28, rim-vs-outside 0.10, heterogeneity 0.07; core [0.837, 0.03, 0.094] rim [0.559, 0.023, 0.15]
  - track 11 at frame 109: holes 0, rim-vs-core 0.18, rim-vs-outside 0.45, heterogeneity 0.05; core [0.936, 0.986, 0.0] rim [0.758, 0.985, 0.0]
  - track 12 at frame 109: holes 0, rim-vs-core 0.26, rim-vs-outside 0.09, heterogeneity 0.05; core [0.82, 0.987, 0.0] rim [0.56, 0.987, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 2.72 (aggregate of 31 individuals; 2/31 membrane-like individually; rim level 0.742)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.924 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.703)
  - radial catalyst K: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.02, rim/outside 3.1 (aggregate of 31 individuals; 5/31 membrane-like individually; rim level 0.177)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #13 (t=414, R_eq 15.1, ring): ['catalyst K']; #14 (t=414, R_eq 5.59): none; #11 (t=327, R_eq 14.71, ring): none; #12 (t=327, R_eq 5.35): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
