# Evidence pack: reacting-thermals (seed 1)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack_fork --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.42 of robust range [0.0, 0.6017], min area 6 px

## Measurements
- components: final 0, mean 7.2, max 47; occupancy final 0.00
- tracks: 262; persistent (alive >= 50% of run): 0; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 1.5/time; max body lengths 20.3
- replication (lineage window K = 20 frames = time 20, default): splits 78, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 5, merges 17, merge/split ratio 0.218, nucleations 61
- channel total drift (end/start - 1): [-1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 127 at frame 192: holes 0, rim-vs-core 0.24, rim-vs-outside 0.73, heterogeneity 0.15; core [1.0, 0.34, 0.359, 1.0] rim [0.831, 0.38, 0.467, 0.881]
  - track 132 at frame 197: holes 0, rim-vs-core 0.20, rim-vs-outside 0.50, heterogeneity 0.15; core [0.924, 0.334, 0.429, 0.936] rim [0.766, 0.37, 0.466, 0.82]
  - track 142 at frame 257: holes 0, rim-vs-core 0.21, rim-vs-outside 0.61, heterogeneity 0.15; core [0.967, 0.357, 0.415, 0.994] rim [0.804, 0.388, 0.408, 0.871]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [101, 202, 303, 398]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 4.71 (aggregate of 35 individuals; 2/35 membrane-like individually; rim level 0.628)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.832 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.478)
  - radial vorticity: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.1 (aggregate of 35 individuals; 6/35 membrane-like individually; rim level 0.497)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 5.1 (aggregate of 35 individuals; 6/35 membrane-like individually; rim level 0.621)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #127 (t=192, R_eq 3.39): none; #132 (t=197, R_eq 3.24): ['burn r']; #142 (t=257, R_eq 3.04): none; #175 (t=313, R_eq 2.19): ['vorticity']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
