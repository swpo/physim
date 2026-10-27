# Evidence pack: reacting-thermals (seed 32)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 38s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/fork --seeds 31 32 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.795], min area 6 px

## Measurements
- components: final 0, mean 6.1, max 46; occupancy final 0.00
- tracks: 258; persistent (alive >= 50% of run): 0; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 64 long-lived tracks moved >= 1 body length; max speed 0.976/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 20, default): splits 69, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 5, merges 13, merge/split ratio 0.188, nucleations 76
- channel total drift (end/start - 1): [-1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 169 at frame 308: holes 0, rim-vs-core 0.35, rim-vs-outside 0.61, heterogeneity 0.16; core [0.988, 0.349, 0.731, 1.0] rim [0.731, 0.388, 0.54, 0.876]
  - track 197 at frame 353: holes 0, rim-vs-core 0.17, rim-vs-outside 0.54, heterogeneity 0.15; core [0.88, 0.319, 0.603, 0.888] rim [0.743, 0.365, 0.525, 0.855]
  - track 162 at frame 287: holes 0, rim-vs-core 0.26, rim-vs-outside 0.67, heterogeneity 0.19; core [0.966, 0.335, 0.49, 0.98] rim [0.744, 0.388, 0.468, 0.847]
  - track 226 at frame 383: holes 0, rim-vs-core 0.18, rim-vs-outside 0.57, heterogeneity 0.15; core [0.875, 0.345, 0.464, 0.98] rim [0.747, 0.377, 0.499, 0.861]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [101, 202, 303, 398]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 4.37 (aggregate of 29 individuals; 2/29 membrane-like individually; rim level 0.588)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.834 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.476)
  - radial vorticity: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 1.09 (aggregate of 29 individuals; 7/29 membrane-like individually; rim level 0.466)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.84 (aggregate of 29 individuals; 7/29 membrane-like individually; rim level 0.633)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #169 (t=308, R_eq 2.93): none; #197 (t=353, R_eq 2.76): none; #162 (t=287, R_eq 3.66): none; #226 (t=383, R_eq 3.43): ['vorticity']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
