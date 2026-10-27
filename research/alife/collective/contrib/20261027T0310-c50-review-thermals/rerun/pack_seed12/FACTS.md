# Evidence pack: reacting-thermals (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out /tmp/claude-0/th/pack --seeds 11 12 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.32 of robust range [0.0, 0.7798], min area 6 px

## Measurements
- components: final 24, mean 14.6, max 49; occupancy final 0.02
- tracks: 389; persistent (alive >= 50% of run): 0; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 36, 28], H1 [0, 0, 0]
- motion: 138 long-lived tracks moved >= 1 body length; max speed 0.976/time; max body lengths 25.2
- replication (lineage window K = 20 frames = time 20, default): splits 96, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 8, merges 19, merge/split ratio 0.198, nucleations 137
- channel total drift (end/start - 1): [-0.8755, -0.3624, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 261 at frame 524: holes 0, rim-vs-core 0.30, rim-vs-outside 0.59, heterogeneity 0.16; core [0.911, 0.113, 0.313, 0.946] rim [0.676, 0.176, 0.336, 0.776]
  - track 217 at frame 444: holes 0, rim-vs-core 0.32, rim-vs-outside 0.60, heterogeneity 0.15; core [0.959, 0.133, 0.266, 0.977] rim [0.718, 0.165, 0.401, 0.811]
  - track 193 at frame 393: holes 0, rim-vs-core 0.16, rim-vs-outside 0.53, heterogeneity 0.13; core [0.816, 0.098, 0.492, 0.85] rim [0.696, 0.137, 0.505, 0.753]
  - track 312 at frame 565: holes 0, rim-vs-core 0.31, rim-vs-outside 0.58, heterogeneity 0.14; core [0.936, 0.128, 0.556, 0.99] rim [0.694, 0.175, 0.548, 0.799]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 5.04 (aggregate of 67 individuals; 2/67 membrane-like individually; rim level 0.607)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.39, rim/outside 0.696 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.272)
  - radial vorticity: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.03 (aggregate of 67 individuals; 13/67 membrane-like individually; rim level 0.451)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 5.94 (aggregate of 67 individuals; 3/67 membrane-like individually; rim level 0.631)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #261 (t=524, R_eq 2.52): none; #217 (t=444, R_eq 2.71): none; #193 (t=393, R_eq 3.52, ring): none; #312 (t=565, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
