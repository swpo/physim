# Evidence pack: phoretic-colloids (seed 3)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 71s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0422-c32-review-phor-divide/world.py --out collective/contrib/20261026T0422-c32-review-phor-divide/tpack --seeds 2 3 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5402], min area 6 px

## Measurements
- components: final 19, mean 17.0, max 26; occupancy final 0.06
- tracks: 411; persistent (alive >= 50% of run): 4; longest 735 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 21, 12], H1 [0, 0, 0]
- motion: 64 long-lived tracks moved >= 1 body length; max speed 0.527/time; max body lengths 9.8
- replication (lineage window K = 20 frames = time 10, default): splits 36, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 49, merge/split ratio 1.36, nucleations 290
- channel total drift (end/start - 1): [0.5071, 0.28, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 437: holes 0, rim-vs-core 0.35, rim-vs-outside 0.31, heterogeneity 0.19; core [0.87, 0.166, 0.696] rim [0.545, 0.184, 0.563]
  - track 7 at frame 323: holes 0, rim-vs-core 0.35, rim-vs-outside 0.31, heterogeneity 0.21; core [0.847, 0.236, 0.714] rim [0.536, 0.275, 0.561]
  - track 2 at frame 309: holes 0, rim-vs-core 0.17, rim-vs-outside 0.25, heterogeneity 0.22; core [0.363, 0.688, 0.397] rim [0.328, 0.521, 0.36]
  - track 350 at frame 746: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.24; core [0.823, 0.285, 0.844] rim [0.526, 0.161, 0.64]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 14.8 (aggregate of 96 individuals; 3/96 membrane-like individually; rim level 0.646)
  - radial B density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 11 (aggregate of 96 individuals; 46/96 membrane-like individually; rim level 0.336)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 2.59 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.592)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=218.5, R_eq 4.03): ['B density']; #7 (t=161.5, R_eq 4.33): ['B density']; #2 (t=154.5, R_eq 2.39): none; #350 (t=373, R_eq 5.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
