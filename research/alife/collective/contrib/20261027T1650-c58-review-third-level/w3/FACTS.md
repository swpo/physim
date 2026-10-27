# Evidence pack: digestion-food-chain-3 (seed 5)

- world: `../../20261027T0407-c52-third-level-negative/world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 475s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0407-c52-third-level-negative/world3.py --out collective/contrib/20261027T1650-c58-review-third-level/w3 --seeds 5 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1514, 2.5883], min area 6 px

## Measurements
- components: final 44, mean 42.7, max 51; occupancy final 0.24
- tracks: 82; persistent (alive >= 50% of run): 45; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 44, 44], H1 [0, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.00364/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.875, nucleations 59
- channel total drift (end/start - 1): [-0.0248, None, -0.6413, -0.5939, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.83, rim-vs-outside 0.24, heterogeneity 0.20; core [0.748, 0.21, 0.071, 0.751, 0.265, 0.506, 0.364] rim [0.377, 0.102, 0.126, 0.382, 0.049, 0.011, 0.041]
  - track 2 at frame 51: holes 0, rim-vs-core 0.80, rim-vs-outside 0.25, heterogeneity 0.20; core [0.749, 0.221, 0.092, 0.78, 0.287, 0.459, 0.377] rim [0.394, 0.098, 0.142, 0.415, 0.055, 0.003, 0.047]
  - track 4 at frame 51: holes 0, rim-vs-core 0.74, rim-vs-outside 0.26, heterogeneity 0.20; core [0.798, 0.213, 0.059, 0.799, 0.298, 0.383, 0.347] rim [0.464, 0.091, 0.113, 0.464, 0.054, 0.001, 0.038]
  - track 53 at frame 67: holes 0, rim-vs-core 0.81, rim-vs-outside 0.31, heterogeneity 0.19; core [0.808, 0.199, 0.058, 0.811, 0.262, 0.519, 0.346] rim [0.45, 0.092, 0.118, 0.457, 0.05, 0.021, 0.04]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 266 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 11.4 (aggregate of 266 individuals; 8/266 membrane-like individually; rim level 0.683)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.426, rim/outside 2.17 (aggregate of 266 individuals; 1/266 membrane-like individually; rim level 0.149)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.77, rim/outside 0.8 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.169)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.769, rim/outside 11.4 (aggregate of 266 individuals; 5/266 membrane-like individually; rim level 0.669)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.293, rim/outside 11.3 (aggregate of 266 individuals; 3/266 membrane-like individually; rim level 0.142)
  - radial top c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.299, rim/outside 18.7 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.189)
  - radial top product s2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.177, rim/outside 10.1 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.0967)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 4.95): none; #2 (t=5100, R_eq 4.48): none; #4 (t=5100, R_eq 4.72): none; #53 (t=6700, R_eq 5.08): none
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 43.0, max 51; tracks 88, persistent 46; splits 8, persistent splits 4 (K=20), max generation 1, merges 3, merge/split 0.375; moving tracks 30
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 8.4, max 48; tracks 72, persistent 0; splits 5, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.2; moving tracks 19
- species `top` (channels ['top c'], own threshold): components final 44, mean 26.2, max 46; tracks 52, persistent 44; splits 0, persistent splits 0 (K=20), max generation 0, merges 1, merge/split n/a; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 266 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
