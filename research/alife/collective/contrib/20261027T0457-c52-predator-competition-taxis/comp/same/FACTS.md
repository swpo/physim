# Evidence pack: digestion-predators-competition (seed 0)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 494s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/same --seeds 0 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.18 of robust range [0.152, 2.0911], min area 6 px

## Measurements
- components: final 50, mean 41.2, max 51; occupancy final 0.20
- tracks: 155; persistent (alive >= 50% of run): 21; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 50, 39], H1 [0, 0, 0]
- motion: 67 long-lived tracks moved >= 1 body length; max speed 0.00718/time; max body lengths 6.0
- replication (lineage window K = 20 frames = time 2000, default): splits 36, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 18, merge/split ratio 0.5, nucleations 65
- channel total drift (end/start - 1): [-0.0521, None, -0.6161, -0.6043, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 52: holes 0, rim-vs-core 0.56, rim-vs-outside 0.14, heterogeneity 0.25; core [0.461, 0.378, 0.137, 0.51, 0.302, 0.343, 0.269] rim [0.374, 0.081, 0.164, 0.4, 0.044, 0.063, 0.033]
  - track 9 at frame 52: holes 0, rim-vs-core 0.15, rim-vs-outside 0.06, heterogeneity 0.06; core [0.236, 0.295, 0.2, 0.241, 0.058, 0.078, 0.004] rim [0.263, 0.15, 0.196, 0.267, 0.024, 0.069, 0.004]
  - track 31 at frame 54: holes 0, rim-vs-core 0.58, rim-vs-outside 0.18, heterogeneity 0.24; core [0.482, 0.41, 0.164, 0.545, 0.291, 0.274, 0.394] rim [0.313, 0.175, 0.191, 0.35, 0.074, 0.027, 0.064]
  - track 95 at frame 81: holes 0, rim-vs-core 0.58, rim-vs-outside 0.18, heterogeneity 0.20; core [0.451, 0.538, 0.161, 0.508, 0.507, 0.085, 0.015] rim [0.324, 0.175, 0.188, 0.354, 0.108, 0.046, 0.004]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 263 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 3.89 (aggregate of 263 individuals; 18/263 membrane-like individually; rim level 0.467)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.357, rim/outside 5.47 (aggregate of 263 individuals; 6/263 membrane-like individually; rim level 0.149)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.857 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.185)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 3.99 (aggregate of 263 individuals; 16/263 membrane-like individually; rim level 0.487)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.317, rim/outside 9.6 (aggregate of 263 individuals; 7/263 membrane-like individually; rim level 0.103)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.376, rim/outside 5.34 (aggregate of 263 individuals; 4/263 membrane-like individually; rim level 0.147)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.336, rim/outside 9.77 (aggregate of 263 individuals; 6/263 membrane-like individually; rim level 0.105)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=5200, R_eq 4.98): none; #9 (t=5200, R_eq 3.99): none; #31 (t=5400, R_eq 4.3): none; #95 (t=8100, R_eq 4.65): none
- species `prey` (channels ['prey a'], own threshold): components final 47, mean 40.5, max 52; tracks 172, persistent 17; splits 42, persistent splits 14 (K=20), max generation 3, merges 3, merge/split 0.071; moving tracks 65
- species `predator` (channels ['predator b'], own threshold): components final 28, mean 19.2, max 30; tracks 132, persistent 0; splits 3, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 37
- species `predator_e` (channels ['predator e'], own threshold): components final 24, mean 17.7, max 29; tracks 126, persistent 1; splits 3, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 29

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 263 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
