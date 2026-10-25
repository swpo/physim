# Evidence pack: fch-pchemoton (seed 13)

- world: `../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 357s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27c/world.py --out collective/contrib/wip-c27c/rerun_s13 --seeds 13 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0209, 1.9958], min area 6 px

## Measurements
- components: final 4, mean 3.3, max 5; occupancy final 0.07
- tracks: 26; persistent (alive >= 50% of run): 2; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.11 (1 = constant size)
- enclosures: components with a hole mean 1.27, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 2], H1 [3, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 9, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.667, nucleations 2
- channel total drift (end/start - 1): [-0.3584, 0.6483, -0.872]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 129: holes 0, rim-vs-core 0.35, rim-vs-outside 0.60, heterogeneity 0.15; core [0.73, 0.0, 0.914] rim [0.605, 0.03, 0.591]
  - track 20 at frame 129: holes 1, rim-vs-core 0.16, rim-vs-outside 0.18, heterogeneity 0.05; core [0.661, 0.109, 0.041] rim [0.505, 0.096, 0.084]
  - track 24 at frame 151: holes 0, rim-vs-core 0.14, rim-vs-outside 0.37, heterogeneity 0.04; core [0.742, 0.993, 0.0] rim [0.605, 0.99, 0.0]
  - track 25 at frame 151: holes 0, rim-vs-core 0.23, rim-vs-outside 0.08, heterogeneity 0.05; core [0.663, 0.992, 0.0] rim [0.435, 0.992, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.5 (aggregate of 20 individuals; 5/20 membrane-like individually; rim level 0.533)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 0.799 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.5)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 6.53, rim/outside 1.91 (aggregate of 20 individuals; 5/20 membrane-like individually; rim level 0.285)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #19 (t=387, R_eq 19.24, ring): ['amphiphile u+1', 'catalyst K']; #20 (t=387, R_eq 12.93, ring): none; #24 (t=453, R_eq 14.99, ring): none; #25 (t=453, R_eq 5.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
