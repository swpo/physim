# Evidence pack: reacting-thermals (seed 9)

- world: `../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [256, 256]; wall 150s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0230-c51-review-thermals/res2x --seeds 9 --size 256 256 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.32 of robust range [0.0, 0.7785], min area 6 px

## Measurements
- components: final 26, mean 19.9, max 54; occupancy final 0.03
- tracks: 359; persistent (alive >= 50% of run): 0; longest 223 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 27, 25], H1 [0, 0, 0]
- motion: 178 long-lived tracks moved >= 1 body length; max speed 2.23/time; max body lengths 34.8
- replication (lineage window K = 20 frames = time 20, default): splits 151, persistent splits 73 (0 more failed only because the siblings re-merged within K), max generation 11, merges 8, merge/split ratio 0.053, nucleations 5
- channel total drift (end/start - 1): [-0.9021, -0.3209, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 228 at frame 489: holes 0, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.16; core [0.844, 0.138, 0.278, 0.91] rim [0.591, 0.193, 0.331, 0.663]
  - track 219 at frame 469: holes 0, rim-vs-core 0.31, rim-vs-outside 0.37, heterogeneity 0.16; core [0.831, 0.118, 0.404, 0.889] rim [0.615, 0.175, 0.448, 0.674]
  - track 175 at frame 353: holes 0, rim-vs-core 0.14, rim-vs-outside 0.29, heterogeneity 0.08; core [0.683, 0.235, 0.321, 0.874] rim [0.609, 0.248, 0.311, 0.758]
  - track 348 at frame 590: holes 0, rim-vs-core 0.23, rim-vs-outside 0.43, heterogeneity 0.15; core [0.8, 0.136, 0.35, 0.883] rim [0.66, 0.162, 0.412, 0.716]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 5.87 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.613)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.08, rim/outside 0.733 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.281)
  - radial vorticity: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.02 (aggregate of 122 individuals; 2/122 membrane-like individually; rim level 0.472)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 7.85 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.661)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #228 (t=489, R_eq 4.48): none; #219 (t=469, R_eq 4.82): none; #175 (t=353, R_eq 2.82): ['vorticity']; #348 (t=590, R_eq 4.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 122 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
