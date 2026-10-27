# Evidence pack: reacting-thermals (seed 7)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0328-c52-review-thermals/fork/seed7 --seeds 7 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.36 of robust range [0.0, 0.7024], min area 6 px

## Measurements
- components: final 0, mean 10.0, max 44; occupancy final 0.00
- tracks: 291; persistent (alive >= 50% of run): 0; longest 236 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 88 long-lived tracks moved >= 1 body length; max speed 1.18/time; max body lengths 29.6
- replication (lineage window K = 20 frames = time 20, default): splits 75, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 16, merge/split ratio 0.213, nucleations 92
- channel total drift (end/start - 1): [-1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 147 at frame 272: holes 0, rim-vs-core 0.29, rim-vs-outside 0.57, heterogeneity 0.15; core [0.941, 0.366, 0.518, 0.994] rim [0.734, 0.395, 0.472, 0.797]
  - track 131 at frame 192: holes 0, rim-vs-core 0.24, rim-vs-outside 0.58, heterogeneity 0.16; core [0.91, 0.336, 0.451, 0.915] rim [0.715, 0.383, 0.475, 0.781]
  - track 217 at frame 348: holes 0, rim-vs-core 0.13, rim-vs-outside 0.52, heterogeneity 0.13; core [0.864, 0.328, 0.394, 0.857] rim [0.757, 0.366, 0.409, 0.803]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [101, 202, 303, 398]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 5.03 (aggregate of 50 individuals; 2/50 membrane-like individually; rim level 0.666)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.833 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.461)
  - radial vorticity: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.12 (aggregate of 50 individuals; 13/50 membrane-like individually; rim level 0.505)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 5.95 (aggregate of 50 individuals; 4/50 membrane-like individually; rim level 0.679)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #147 (t=272, R_eq 2.33): none; #142 (t=227, R_eq 1.78): none; #131 (t=192, R_eq 3.83, ring): ['burn r']; #217 (t=348, R_eq 3.09, ring): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
