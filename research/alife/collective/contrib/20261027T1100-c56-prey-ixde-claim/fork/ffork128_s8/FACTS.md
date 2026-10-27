# Evidence pack: digestion-driven-predators (seed 8)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 286s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/py/ffork128_s8 --seeds 8 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1527, 1.7661], min area 6 px

## Measurements
- components: final 30, mean 38.0, max 51; occupancy final 0.06
- tracks: 117; persistent (alive >= 50% of run): 17; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 26, 14], H1 [0, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.00543/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 2000, default): splits 25, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 16, merge/split ratio 0.64, nucleations 51
- channel total drift (end/start - 1): [-0.0091, None, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.14, heterogeneity 0.20; core [0.324, 0.565, 0.378, 0.427, 0.326] rim [0.276, 0.195, 0.387, 0.37, 0.085]
  - track 15 at frame 43: holes 0, rim-vs-core 0.50, rim-vs-outside 0.17, heterogeneity 0.27; core [0.48, 0.488, 0.333, 0.579, 0.434] rim [0.353, 0.169, 0.355, 0.44, 0.096]
  - track 5 at frame 40: holes 0, rim-vs-core 0.45, rim-vs-outside 0.14, heterogeneity 0.25; core [0.39, 0.502, 0.357, 0.491, 0.353] rim [0.319, 0.164, 0.37, 0.409, 0.077]
  - track 73 at frame 62: holes 0, rim-vs-core 0.44, rim-vs-outside 0.15, heterogeneity 0.08; core [0.177, 0.641, 0.0, 0.0, 0.226] rim [0.192, 0.23, 0.0, 0.0, 0.075]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 237 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 2.43 (aggregate of 237 individuals; 44/237 membrane-like individually; rim level 0.374)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.453, rim/outside 5.87 (aggregate of 237 individuals; 3/237 membrane-like individually; rim level 0.285)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.942 (aggregate of 237 individuals; 0/237 membrane-like individually; rim level 0.254)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 2.49 (aggregate of 237 individuals; 15/237 membrane-like individually; rim level 0.362)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.365, rim/outside 10.6 (aggregate of 237 individuals; 2/237 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=4200, R_eq 4.37): ['prey a']; #15 (t=4300, R_eq 4.79): none; #5 (t=4000, R_eq 4.98): none; #73 (t=6200, R_eq 4.07): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 28.6, max 47; tracks 107, persistent 11; splits 21, persistent splits 7 (K=20), max generation 2, merges 3, merge/split 0.143; moving tracks 40
- species `predator` (channels ['predator b'], own threshold): components final 9, mean 26.5, max 45; tracks 88, persistent 15; splits 10, persistent splits 7 (K=20), max generation 2, merges 2, merge/split 0.2; moving tracks 44

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 237 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
