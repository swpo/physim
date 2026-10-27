# Evidence pack: reacting-thermals (seed 11)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out /tmp/claude-0/th/pack --seeds 11 12 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7598], min area 6 px

## Measurements
- components: final 28, mean 12.8, max 39; occupancy final 0.02
- tracks: 367; persistent (alive >= 50% of run): 0; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 35, 29], H1 [0, 0, 0]
- motion: 120 long-lived tracks moved >= 1 body length; max speed 1.01/time; max body lengths 19.3
- replication (lineage window K = 20 frames = time 20, default): splits 98, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 7, merges 17, merge/split ratio 0.173, nucleations 122
- channel total drift (end/start - 1): [-0.8607, -0.348, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 191 at frame 504: holes 0, rim-vs-core 0.28, rim-vs-outside 0.59, heterogeneity 0.15; core [0.943, 0.088, 0.589, 0.98] rim [0.748, 0.133, 0.468, 0.833]
  - track 213 at frame 509: holes 0, rim-vs-core 0.23, rim-vs-outside 0.51, heterogeneity 0.13; core [0.883, 0.116, 0.354, 0.959] rim [0.714, 0.155, 0.397, 0.816]
  - track 157 at frame 413: holes 0, rim-vs-core 0.24, rim-vs-outside 0.55, heterogeneity 0.15; core [0.917, 0.064, 0.431, 0.925] rim [0.738, 0.116, 0.405, 0.775]
  - track 153 at frame 403: holes 0, rim-vs-core 0.31, rim-vs-outside 0.65, heterogeneity 0.16; core [0.959, 0.109, 0.442, 0.996] rim [0.714, 0.164, 0.413, 0.817]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 63 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 4.87 (aggregate of 63 individuals; 2/63 membrane-like individually; rim level 0.619)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.94, rim/outside 0.663 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.246)
  - radial vorticity: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.05 (aggregate of 63 individuals; 10/63 membrane-like individually; rim level 0.478)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 5.74 (aggregate of 63 individuals; 4/63 membrane-like individually; rim level 0.631)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #191 (t=504, R_eq 2.33): none; #213 (t=509, R_eq 2.03): none; #157 (t=413, R_eq 3.34, ring): ['burn r']; #153 (t=403, R_eq 2.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 63 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
