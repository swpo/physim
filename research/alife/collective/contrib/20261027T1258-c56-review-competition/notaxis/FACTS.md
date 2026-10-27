# Evidence pack: digestion-predators-competition (seed 23)

- world: `../../../collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 483s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out c56work/cp/notaxis --seeds 23 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1527, 1.8407], min area 6 px

## Measurements
- components: final 34, mean 35.8, max 46; occupancy final 0.20
- tracks: 130; persistent (alive >= 50% of run): 13; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 91.86 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 36, 30], H1 [1, 1, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.00725/time; max body lengths 5.4
- replication (lineage window K = 20 frames = time 2000, default): splits 38, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.211, nucleations 45
- channel total drift (end/start - 1): [-0.0351, None, -0.6041, -0.5986, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 53: holes 0, rim-vs-core 0.48, rim-vs-outside 0.19, heterogeneity 0.20; core [0.541, 0.397, 0.185, 0.595, 0.349, 0.414, 0.164] rim [0.353, 0.134, 0.218, 0.386, 0.072, 0.399, 0.098]
  - track 4 at frame 49: holes 0, rim-vs-core 0.44, rim-vs-outside 0.38, heterogeneity 0.19; core [0.367, 0.466, 0.229, 0.409, 0.257, 0.9, 0.472] rim [0.402, 0.087, 0.226, 0.442, 0.049, 0.84, 0.45]
  - track 7 at frame 45: holes 0, rim-vs-core 0.52, rim-vs-outside 0.19, heterogeneity 0.21; core [0.488, 0.423, 0.203, 0.544, 0.361, 0.639, 0.33] rim [0.31, 0.119, 0.233, 0.341, 0.071, 0.595, 0.182]
  - track 103 at frame 89: holes 0, rim-vs-core 0.50, rim-vs-outside 0.20, heterogeneity 0.20; core [0.43, 0.5, 0.258, 0.519, 0.369, 0.601, 0.259] rim [0.297, 0.167, 0.281, 0.357, 0.083, 0.578, 0.167]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 220 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 4.95 (aggregate of 220 individuals; 28/220 membrane-like individually; rim level 0.478)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.332, rim/outside 7.45 (aggregate of 220 individuals; 3/220 membrane-like individually; rim level 0.189)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.87 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.245)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 4.92 (aggregate of 220 individuals; 24/220 membrane-like individually; rim level 0.492)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.27, rim/outside 10.4 (aggregate of 220 individuals; 9/220 membrane-like individually; rim level 0.118)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 1.07 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.447)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 3.73 (aggregate of 220 individuals; 22/220 membrane-like individually; rim level 0.174)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=5300, R_eq 4.65): none; #4 (t=4900, R_eq 4.33): none; #7 (t=4500, R_eq 4.75): none; #103 (t=8900, R_eq 4.37): none
- species `prey` (channels ['prey a'], own threshold): components final 34, mean 34.9, max 46; tracks 142, persistent 13; splits 43, persistent splits 22 (K=20), max generation 4, merges 5, merge/split 0.116; moving tracks 50
- species `predator` (channels ['predator b'], own threshold): components final 32, mean 25.8, max 42; tracks 118, persistent 10; splits 26, persistent splits 16 (K=20), max generation 2, merges 1, merge/split 0.038; moving tracks 52
- species `predator_e` (channels ['predator e'], own threshold): components final 2, mean 1.3, max 12; tracks 23, persistent 1; splits 4, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 1; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 220 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
