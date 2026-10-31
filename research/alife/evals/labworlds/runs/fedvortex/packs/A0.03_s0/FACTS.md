# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 159s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0.03_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.25 of robust range [0.0006, 0.2356], min area 6 px

## Measurements
- components: final 75, mean 70.4, max 86; occupancy final 0.21
- tracks: 6394; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [118, 72, 39], H1 [7, 0, 0]
- motion: 263 long-lived tracks moved >= 1 body length; max speed 0.615/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 60, default): splits 1708, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1659, merge/split ratio 0.971, nucleations 1419
- channel total drift (end/start - 1): [-0.0716, -0.0572, -3337.1299, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2094 at frame 185: holes 0, rim-vs-core 0.68, rim-vs-outside 0.28, heterogeneity 0.22; core [0.754, 0.132, 0.08, 0.573] rim [0.363, 0.357, 0.276, 0.1]
  - track 932 at frame 97: holes 0, rim-vs-core 0.37, rim-vs-outside 0.22, heterogeneity 0.16; core [0.579, 0.174, 0.816, 0.303] rim [0.349, 0.344, 0.686, 0.099]
  - track 5193 at frame 366: holes 0, rim-vs-core 0.80, rim-vs-outside 0.31, heterogeneity 0.22; core [0.806, 0.199, 0.934, 0.679] rim [0.359, 0.434, 0.692, 0.114]
  - track 4323 at frame 309: holes 0, rim-vs-core 0.50, rim-vs-outside 0.53, heterogeneity 0.23; core [0.785, 0.128, 0.919, 0.599] rim [0.483, 0.32, 0.756, 0.286]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 360 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.698, rim/outside 2.76 (aggregate of 360 individuals; 13/360 membrane-like individually; rim level 0.455)
  - radial fuel Y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.5, rim/outside 0.875 (aggregate of 360 individuals; 0/360 membrane-like individually; rim level 0.571)
  - radial vorticity (signed): peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.988 (aggregate of 360 individuals; 0/360 membrane-like individually; rim level 0.474)
  - radial eating: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.523, rim/outside 5.91 (aggregate of 360 individuals; 41/360 membrane-like individually; rim level 0.232)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2094 (t=555, R_eq 3.7): none; #932 (t=291, R_eq 4.75): none; #5193 (t=1098, R_eq 3.87): none; #4323 (t=927, R_eq 3.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 360 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
