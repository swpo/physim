# Evidence pack: pps (seed 1)

- world: `../../world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 110s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0230-c29-pps-sighting/world.py --out collective/contrib/20261026T0230-c29-pps-sighting/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 7.8125], min area 6 px

## Measurements
- components: final 28, mean 14.9, max 90; occupancy final 0.18
- tracks: 1211; persistent (alive >= 50% of run): 0; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.67, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 51, 36], H1 [2, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00274/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 3000, default): splits 428, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 393, merge/split ratio 0.918, nucleations 3
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 470 at frame 151: holes 0, rim-vs-core 0.37, rim-vs-outside 0.02, heterogeneity 0.27; core [0.283, 0.15, 0.225] rim [0.02, 0.0, 0.02]
  - track 374 at frame 119: holes 0, rim-vs-core 0.46, rim-vs-outside 0.02, heterogeneity 0.19; core [0.367, 0.0, 0.3] rim [0.024, 0.0, 0.0]
  - track 673 at frame 168: holes 0, rim-vs-core 0.40, rim-vs-outside 0.02, heterogeneity 0.21; core [0.295, 0.045, 0.273] rim [0.0, 0.0, 0.0]
  - track 767 at frame 175: holes 0, rim-vs-core 0.28, rim-vs-outside 0.01, heterogeneity 0.19; core [0.217, 0.0, 0.217] rim [0.026, 0.0, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 104 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.625, rim/outside 2.96 (aggregate of 104 individuals; 27/104 membrane-like individually; rim level 0.149)
  - radial cell N>35: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.181, rim/outside 1.38 (aggregate of 104 individuals; 25/104 membrane-like individually; rim level 0.0065)
  - radial ring 15<N<=35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.646, rim/outside 4.89 (aggregate of 104 individuals; 36/104 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #470 (t=22650, R_eq 3.43): ['ring 15<N<=35']; #374 (t=17850, R_eq 2.76): none; #673 (t=25200, R_eq 3.57): none; #767 (t=26250, R_eq 2.71): none

## Warnings
- radial: 5 of 104 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
