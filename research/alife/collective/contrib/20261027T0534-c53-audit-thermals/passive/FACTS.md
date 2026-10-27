# Evidence pack: reacting-thermals (seed 32)

- world: `../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 451 frames x 25 steps x dt 0.04 = time 450; grid [128, 128]; wall 29s; status ok
- command: `python -m labkit.run collective/contrib/c53-audit-work/world.py --out collective/contrib/c53-audit-work/passive --seeds 32 --frames 450 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.7988], min area 6 px

## Measurements
- components: final 0, mean 4.7, max 46; occupancy final 0.00
- tracks: 193; persistent (alive >= 50% of run): 0; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 6, 2], H1 [1, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.976/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 20, default): splits 56, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 12, merge/split ratio 0.214, nucleations 38
- channel total drift (end/start - 1): [-0.9129, -0.0106, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 162 at frame 280: holes 0, rim-vs-core 0.24, rim-vs-outside 0.71, heterogeneity 0.19; core [0.96, 0.133, 0.488, 0.98] rim [0.752, 0.211, 0.496, 0.891]
  - track 107 at frame 91: holes 0, rim-vs-core 0.26, rim-vs-outside 0.62, heterogeneity 0.17; core [0.94, 0.139, 0.47, 0.997] rim [0.726, 0.201, 0.497, 0.877]
  - track 112 at frame 163: holes 0, rim-vs-core 0.32, rim-vs-outside 0.63, heterogeneity 0.14; core [0.951, 0.174, 0.615, 0.999] rim [0.701, 0.197, 0.471, 0.853]
  - track 182 at frame 284: holes 0, rim-vs-core 0.31, rim-vs-outside 0.65, heterogeneity 0.17; core [0.937, 0.162, 0.617, 0.992] rim [0.685, 0.221, 0.546, 0.835]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [76, 151, 227, 299]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 3.84 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.548)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.17, rim/outside 0.715 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.328)
  - radial vorticity: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 1.07 (aggregate of 18 individuals; 3/18 membrane-like individually; rim level 0.476)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 4.04 (aggregate of 18 individuals; 2/18 membrane-like individually; rim level 0.614)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #162 (t=280, R_eq 3.29): none; #107 (t=91, R_eq 3.14): ['burn r']; #112 (t=163, R_eq 4.03, ring): none; #182 (t=284, R_eq 2.99): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
