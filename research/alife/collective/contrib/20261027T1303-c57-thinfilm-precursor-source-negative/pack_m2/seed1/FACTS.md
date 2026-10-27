# Evidence pack: fed-thinfilm (seed 1)

- world: `../../world.py`, family `thin-film`
- parent: collective/contrib/20261025T1915-c24-thinfilm-sighting; mutation: non-conserved film: condensation from a consumed, regrowing vapour along the film's own chemical potential, and decay of liquid inside drops
- run: 161 frames x 200 steps x dt 0.25 = time 8000; grid [128, 128]; wall 237s; status ok
- command: `python -m labkit.run collective/contrib/c57-w4/world.py --out collective/contrib/c57-w4/pack_m2/seed1 --seeds 1 --size 128 128 --frames 160 --no-movie`
- segmentation: matter > 0.08 of robust range [0.1428, 4.8721], min area 6 px

## Measurements
- components: final 6, mean 4.7, max 9; occupancy final 0.46
- tracks: 204; persistent (alive >= 50% of run): 0; longest 26 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 5, 4], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0582/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 1000, default): splits 67, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 61, merge/split ratio 0.91, nucleations 20
- channel total drift (end/start - 1): [-0.06, 12.4833, -1184.2726, 576.33, -0.0498]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 151 at frame 112: holes 0, rim-vs-core 0.21, rim-vs-outside 0.22, heterogeneity 0.08; core [0.394, 0.893, 0.065, 0.372, 0.624] rim [0.198, 0.9, 0.065, 0.377, 0.557]
  - track 123 at frame 85: holes 0, rim-vs-core 0.37, rim-vs-outside 0.35, heterogeneity 0.12; core [0.592, 0.936, 0.142, 0.202, 0.683] rim [0.247, 0.9, 0.185, 0.22, 0.565]
  - track 103 at frame 56: holes 0, rim-vs-core 0.11, rim-vs-outside 0.09, heterogeneity 0.04; core [0.196, 0.888, 0.685, 0.047, 0.604] rim [0.118, 0.845, 0.673, 0.07, 0.545]
  - track 141 at frame 102: holes 0, rim-vs-core 0.09, rim-vs-outside 0.06, heterogeneity 0.03; core [0.156, 0.878, 0.116, 0.259, 0.639] rim [0.104, 0.846, 0.133, 0.265, 0.581]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.566, rim/outside 1.68 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.201)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 1.09 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.838)
  - radial p_x: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.01 (aggregate of 26 individuals; 1/26 membrane-like individually; rim level 0.243)
  - radial p_y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.975 (aggregate of 26 individuals; 1/26 membrane-like individually; rim level 0.404)
  - radial vapour V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 1.23 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.512)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #151 (t=5600, R_eq 11.13): none; #123 (t=4250, R_eq 21.21): none; #103 (t=2800, R_eq 8.94): none; #141 (t=5100, R_eq 9.61): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 26 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 26 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
