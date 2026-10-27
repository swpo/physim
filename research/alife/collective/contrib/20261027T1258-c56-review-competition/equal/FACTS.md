# Evidence pack: digestion-predators-competition (seed 23)

- world: `../../../collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 527s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out c56work/cp/equal --seeds 23 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.18 of robust range [0.1526, 2.0659], min area 6 px

## Measurements
- components: final 43, mean 39.1, max 50; occupancy final 0.18
- tracks: 132; persistent (alive >= 50% of run): 21; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 38, 25], H1 [1, 1, 0]
- motion: 64 long-lived tracks moved >= 1 body length; max speed 0.00734/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 2000, default): splits 25, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 1, merges 17, merge/split ratio 0.68, nucleations 65
- channel total drift (end/start - 1): [-0.0374, None, -0.6076, -0.5962, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 54: holes 0, rim-vs-core 0.11, rim-vs-outside 0.33, heterogeneity 0.11; core [0.298, 0.432, 0.204, 0.317, 0.208, 0.129, 0.022] rim [0.273, 0.343, 0.209, 0.289, 0.172, 0.106, 0.016]
  - track 24 at frame 54: holes 0, rim-vs-core 0.60, rim-vs-outside 0.18, heterogeneity 0.19; core [0.431, 0.595, 0.185, 0.487, 0.536, 0.016, 0.001] rim [0.344, 0.181, 0.204, 0.378, 0.13, 0.01, 0.0]
  - track 13 at frame 50: holes 0, rim-vs-core 0.66, rim-vs-outside 0.15, heterogeneity 0.19; core [0.444, 0.135, 0.155, 0.48, 0.03, 0.54, 0.575] rim [0.378, 0.06, 0.172, 0.395, 0.008, 0.086, 0.115]
  - track 43 at frame 67: holes 0, rim-vs-core 0.56, rim-vs-outside 0.18, heterogeneity 0.21; core [0.527, 0.424, 0.143, 0.577, 0.457, 0.124, 0.062] rim [0.383, 0.094, 0.174, 0.41, 0.071, 0.047, 0.011]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 3.65 (aggregate of 242 individuals; 22/242 membrane-like individually; rim level 0.452)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.386, rim/outside 5.46 (aggregate of 242 individuals; 6/242 membrane-like individually; rim level 0.155)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.876 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.212)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 3.74 (aggregate of 242 individuals; 19/242 membrane-like individually; rim level 0.476)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.351, rim/outside 9.44 (aggregate of 242 individuals; 10/242 membrane-like individually; rim level 0.101)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.39, rim/outside 5.38 (aggregate of 242 individuals; 6/242 membrane-like individually; rim level 0.159)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.365, rim/outside 10.3 (aggregate of 242 individuals; 8/242 membrane-like individually; rim level 0.113)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=5400, R_eq 4.58): none; #24 (t=5400, R_eq 4.3): none; #13 (t=5000, R_eq 4.48): none; #43 (t=6700, R_eq 5.05): none
- species `prey` (channels ['prey a'], own threshold): components final 37, mean 37.0, max 47; tracks 142, persistent 17; splits 25, persistent splits 11 (K=20), max generation 1, merges 4, merge/split 0.16; moving tracks 63
- species `predator` (channels ['predator b'], own threshold): components final 24, mean 17.2, max 31; tracks 123, persistent 1; splits 1, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 29
- species `predator_e` (channels ['predator e'], own threshold): components final 21, mean 17.1, max 26; tracks 128, persistent 1; splits 1, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 25

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 242 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
