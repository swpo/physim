# Evidence pack: phoretic-colloids (seed 4)

- world: `../../20261026T0441-c33-phoretic-no-wall/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 107s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0441-c33-phoretic-no-wall/world.py --out collective/contrib/20261026T0503-c30-review-phoretic-nowall/nucleus --seeds 4 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8934], min area 6 px

## Measurements
- components: final 10, mean 12.4, max 21; occupancy final 0.05
- tracks: 218; persistent (alive >= 50% of run): 3; longest 537 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 8], H1 [0, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.468/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 10, default): splits 18, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 4, merges 32, merge/split ratio 1.78, nucleations 150
- channel total drift (end/start - 1): [0.6386, -0.39, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 410: holes 0, rim-vs-core 0.10, rim-vs-outside 0.18, heterogeneity 0.05; core [0.682, 0.01, 0.327] rim [0.601, 0.054, 0.301]
  - track 94 at frame 424: holes 0, rim-vs-core 0.30, rim-vs-outside 0.29, heterogeneity 0.11; core [0.887, 0.036, 0.561] rim [0.611, 0.075, 0.461]
  - track 25 at frame 309: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.16; core [0.667, 0.518, 0.506] rim [0.552, 0.335, 0.434]
  - track 211 at frame 753: holes 0, rim-vs-core 0.15, rim-vs-outside 0.29, heterogeneity 0.04; core [0.835, 0.0, 0.438] rim [0.683, 0.0, 0.411]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 15.6 (aggregate of 71 individuals; 3/71 membrane-like individually; rim level 0.704)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.662, rim/outside 9.02 (aggregate of 71 individuals; 33/71 membrane-like individually; rim level 0.228)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 2.33 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.518)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #79 (t=205, R_eq 2.19): ['B density']; #94 (t=212, R_eq 3.99): ['B density']; #25 (t=154.5, R_eq 3.66): none; #211 (t=376.5, R_eq 2.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
