# Evidence pack: fed-thinfilm (seed 0)

- world: `../../world.py`, family `thin-film`
- parent: collective/contrib/20261025T1915-c24-thinfilm-sighting; mutation: non-conserved film: condensation from a consumed, regrowing vapour along the film's own chemical potential, and decay of liquid inside drops
- run: 61 frames x 200 steps x dt 0.25 = time 3000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/c57-w3/world.py --out collective/contrib/c57-w3/pack_h2 --seeds 0 1 --size 128 128 --frames 60 --no-movie`
- segmentation: matter > 0.19 of robust range [0.1162, 2.0996], min area 6 px

## Measurements
- components: final 9, mean 10.9, max 19; occupancy final 0.12
- tracks: 51; persistent (alive >= 50% of run): 8; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.69 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0332/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 1000, default): splits 14, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 14, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [-0.6856, 8.3823, 3993.8406, -36.0332, -0.0627]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 34: holes 0, rim-vs-core 0.44, rim-vs-outside 0.27, heterogeneity 0.13; core [0.744, 0.911, 0.038, 0.321, 0.135] rim [0.326, 0.817, 0.1, 0.34, 0.23]
  - track 9 at frame 34: holes 0, rim-vs-core 0.35, rim-vs-outside 0.22, heterogeneity 0.10; core [0.64, 0.914, 0.772, 0.106, 0.209] rim [0.306, 0.835, 0.746, 0.156, 0.272]
  - track 12 at frame 34: holes 0, rim-vs-core 0.31, rim-vs-outside 0.20, heterogeneity 0.09; core [0.595, 0.915, 0.589, 0.03, 0.233] rim [0.302, 0.849, 0.583, 0.074, 0.282]
  - track 20 at frame 35: holes 0, rim-vs-core 0.25, rim-vs-outside 0.18, heterogeneity 0.07; core [0.543, 0.91, 0.782, 0.106, 0.28] rim [0.306, 0.852, 0.758, 0.135, 0.322]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.669, rim/outside 7.11 (aggregate of 75 individuals; 1/75 membrane-like individually; rim level 0.532)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 1.71 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.893)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 1.07 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.61)
  - radial p_y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.96 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.431)
  - radial vapour V: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.12, rim/outside 0.809 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.329)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=1700, R_eq 8.78): none; #9 (t=1700, R_eq 7.78): none; #12 (t=1700, R_eq 7.33): none; #20 (t=1750, R_eq 6.75): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
