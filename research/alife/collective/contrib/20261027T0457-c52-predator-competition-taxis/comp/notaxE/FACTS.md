# Evidence pack: digestion-predators-competition (seed 0)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 453s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/notaxE --seeds 0 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.21 of robust range [0.152, 1.8256], min area 6 px

## Measurements
- components: final 33, mean 37.4, max 50; occupancy final 0.21
- tracks: 134; persistent (alive >= 50% of run): 19; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 41.00 (1 = constant size)
- enclosures: components with a hole mean 0.34, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 34, 27], H1 [1, 1, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.0074/time; max body lengths 6.5
- replication (lineage window K = 20 frames = time 2000, default): splits 35, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 12, merge/split ratio 0.343, nucleations 52
- channel total drift (end/start - 1): [-0.0323, None, -0.6124, -0.6067, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 52: holes 0, rim-vs-core 0.54, rim-vs-outside 0.20, heterogeneity 0.22; core [0.459, 0.467, 0.23, 0.538, 0.405, 0.603, 0.341] rim [0.327, 0.125, 0.254, 0.378, 0.075, 0.563, 0.215]
  - track 17 at frame 43: holes 0, rim-vs-core 0.50, rim-vs-outside 0.16, heterogeneity 0.19; core [0.432, 0.481, 0.215, 0.478, 0.362, 0.418, 0.151] rim [0.304, 0.135, 0.237, 0.328, 0.07, 0.417, 0.104]
  - track 30 at frame 46: holes 0, rim-vs-core 0.51, rim-vs-outside 0.18, heterogeneity 0.20; core [0.488, 0.434, 0.211, 0.55, 0.362, 0.527, 0.231] rim [0.319, 0.118, 0.237, 0.355, 0.075, 0.508, 0.137]
  - track 85 at frame 77: holes 0, rim-vs-core 0.28, rim-vs-outside 0.35, heterogeneity 0.17; core [0.25, 0.542, 0.272, 0.287, 0.238, 0.565, 0.153] rim [0.32, 0.283, 0.258, 0.357, 0.214, 0.566, 0.18]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 223 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 5.38 (aggregate of 223 individuals; 26/223 membrane-like individually; rim level 0.503)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.348, rim/outside 7.38 (aggregate of 223 individuals; 6/223 membrane-like individually; rim level 0.185)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.874 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.244)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 5.25 (aggregate of 223 individuals; 25/223 membrane-like individually; rim level 0.516)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.288, rim/outside 10.6 (aggregate of 223 individuals; 12/223 membrane-like individually; rim level 0.121)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 1.06 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.428)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 3.87 (aggregate of 223 individuals; 24/223 membrane-like individually; rim level 0.194)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=5200, R_eq 4.58): none; #17 (t=4300, R_eq 4.58): none; #30 (t=4600, R_eq 4.33): none; #85 (t=7700, R_eq 4.72): none
- species `prey` (channels ['prey a'], own threshold): components final 30, mean 36.5, max 49; tracks 142, persistent 17; splits 39, persistent splits 17 (K=20), max generation 2, merges 4, merge/split 0.103; moving tracks 52
- species `predator` (channels ['predator b'], own threshold): components final 30, mean 26.4, max 46; tracks 126, persistent 13; splits 23, persistent splits 11 (K=20), max generation 1, merges 1, merge/split 0.043; moving tracks 48
- species `predator_e` (channels ['predator e'], own threshold): components final 7, mean 3.1, max 12; tracks 51, persistent 0; splits 11, persistent splits 0 (K=20), max generation 0, merges 9, merge/split 0.818; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 223 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
