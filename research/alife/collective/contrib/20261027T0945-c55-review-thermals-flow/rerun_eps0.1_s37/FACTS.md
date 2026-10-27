# Evidence pack: reacting-thermals (seed 37)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0209-c49-thermals-flow-heredity/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 801 frames x 25 steps x dt 0.04 = time 800; grid [128, 128]; wall 98s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0209-c49-thermals-flow-heredity/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/flow/pack_eps0.1 --seeds 37 --frames 800 --spf 25 --no-movie`
- segmentation: matter > 0.41 of robust range [0.0, 0.6095], min area 6 px

## Measurements
- components: final 32, mean 21.7, max 41; occupancy final 0.03
- tracks: 728; persistent (alive >= 50% of run): 0; longest 211 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 38, 33], H1 [0, 0, 0]
- motion: 271 long-lived tracks moved >= 1 body length; max speed 1.12/time; max body lengths 32.5
- replication (lineage window K = 20 frames = time 20, default): splits 164, persistent splits 46 (0 more failed only because the siblings re-merged within K), max generation 6, merges 21, merge/split ratio 0.128, nucleations 350
- channel total drift (end/start - 1): [-0.7448, -0.3959, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 325 at frame 484: holes 0, rim-vs-core 0.18, rim-vs-outside 0.56, heterogeneity 0.08; core [0.902, 0.009, 0.997, 0.077] rim [0.762, 0.041, 0.886, 0.067]
  - track 269 at frame 403: holes 0, rim-vs-core 0.28, rim-vs-outside 0.48, heterogeneity 0.08; core [0.955, 0.033, 0.823, 0.596] rim [0.743, 0.072, 0.683, 0.497]
  - track 520 at frame 666: holes 0, rim-vs-core 0.15, rim-vs-outside 0.51, heterogeneity 0.07; core [0.878, 0.009, 1.0, 0.083] rim [0.759, 0.038, 0.91, 0.069]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 6.12 (aggregate of 100 individuals; 2/100 membrane-like individually; rim level 0.725)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.56, rim/outside 0.595 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.176)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 4.96 (aggregate of 100 individuals; 2/100 membrane-like individually; rim level 0.651)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 4.07 (aggregate of 100 individuals; 2/100 membrane-like individually; rim level 0.199)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #325 (t=484, R_eq 2.76): none; #463 (t=645, R_eq 1.69): none; #269 (t=403, R_eq 2.46): none; #520 (t=666, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 100 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
