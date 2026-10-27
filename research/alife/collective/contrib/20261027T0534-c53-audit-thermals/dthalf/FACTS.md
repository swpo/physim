# Evidence pack: reacting-thermals (seed 33)

- world: `../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 50 steps x dt 0.02 (--dt; world META dt 0.04) = time 600; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/dthalf --seeds 33 --frames 600 --spf 50 --dt 0.02 --no-movie`
- segmentation: matter > 0.37 of robust range [0.0, 0.6759], min area 6 px

## Measurements
- components: final 23, mean 22.3, max 35; occupancy final 0.02
- tracks: 531; persistent (alive >= 50% of run): 0; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 33, 26], H1 [0, 0, 0]
- motion: 209 long-lived tracks moved >= 1 body length; max speed 0.992/time; max body lengths 26.0
- replication (lineage window K = 20 frames = time 20, default): splits 93, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 6, merges 8, merge/split ratio 0.086, nucleations 309
- channel total drift (end/start - 1): [-0.8547, -0.342, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 160 at frame 292: holes 0, rim-vs-core 0.31, rim-vs-outside 0.61, heterogeneity 0.16; core [0.962, 0.087, 0.343, 0.978] rim [0.725, 0.146, 0.346, 0.792]
  - track 242 at frame 363: holes 0, rim-vs-core 0.30, rim-vs-outside 0.59, heterogeneity 0.15; core [0.95, 0.114, 0.489, 0.979] rim [0.706, 0.162, 0.497, 0.808]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 5.5 (aggregate of 90 individuals; 2/90 membrane-like individually; rim level 0.673)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.06, rim/outside 0.664 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.234)
  - radial vorticity: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.03 (aggregate of 90 individuals; 17/90 membrane-like individually; rim level 0.478)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 6.77 (aggregate of 90 individuals; 4/90 membrane-like individually; rim level 0.685)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #160 (t=292, R_eq 2.59): none; #270 (t=403, R_eq 2.33): none; #242 (t=363, R_eq 1.95): none; #341 (t=474, R_eq 1.78): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.02 only relabels time (world META dt 0.04): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 5 of 90 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
