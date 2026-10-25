# Evidence pack: fch-pchemoton (seed 8)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 301 frames x 300 steps x dt 0.01 = time 900; grid [192, 192]; wall 539s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1240-c13-review-fch-chemoton/world.py --out collective/contrib/20261025T1240-c13-review-fch-chemoton/rerun/seed8 --seeds 8 --frames 300 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.0195, 1.5331], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 6; occupancy final 0.12
- tracks: 7; persistent (alive >= 50% of run): 5; longest 300 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.96 (1 = constant size)
- enclosures: components with a hole mean 0.96, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 10, 5], H1 [3, 2, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [0.4839, -0.1432, -0.5729]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 151: holes 0, rim-vs-core 0.24, rim-vs-outside 0.41, heterogeneity 0.06; core [0.902, 0.917, 0.0] rim [0.661, 0.917, 0.001]
  - track 3 at frame 151: holes 0, rim-vs-core 0.48, rim-vs-outside 0.59, heterogeneity 0.16; core [0.917, 0.009, 0.77] rim [0.708, 0.058, 0.343]
  - track 4 at frame 151: holes 0, rim-vs-core 0.55, rim-vs-outside 0.49, heterogeneity 0.17; core [0.912, 0.013, 0.766] rim [0.673, 0.065, 0.278]
  - track 5 at frame 151: holes 0, rim-vs-core 0.39, rim-vs-outside 0.47, heterogeneity 0.17; core [0.881, 0.03, 0.596] rim [0.666, 0.071, 0.27]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.54, rim/outside 3.24 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.331)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.8 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.395)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.469, rim/outside 2.06 (aggregate of 30 individuals; 6/30 membrane-like individually; rim level 0.0944)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=453, R_eq 11.62): none; #3 (t=453, R_eq 15.85, ring): none; #4 (t=453, R_eq 13.55): none; #5 (t=453, R_eq 13.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
