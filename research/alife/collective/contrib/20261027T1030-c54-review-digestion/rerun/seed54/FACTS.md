# Evidence pack: digestion-driven-predators (seed 54)

- world: `../../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1898s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/20261027T1030-c54-review-digestion/rerun/seed54 --seeds 54 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1586, 1.7938], min area 6 px

## Measurements
- components: final 193, mean 174.0, max 201; occupancy final 0.20
- tracks: 788; persistent (alive >= 50% of run): 75; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [200, 190, 162], H1 [0, 0, 0]
- motion: 315 long-lived tracks moved >= 1 body length; max speed 0.00836/time; max body lengths 8.6
- replication (lineage window K = 20 frames = time 2000, default): splits 149, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 3, merges 159, merge/split ratio 1.07, nucleations 334
- channel total drift (end/start - 1): [-0.0514, None, -0.6126, -0.5997, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 61: holes 0, rim-vs-core 0.48, rim-vs-outside 0.16, heterogeneity 0.26; core [0.459, 0.495, 0.133, 0.5, 0.386] rim [0.344, 0.166, 0.156, 0.365, 0.08]
  - track 20 at frame 62: holes 0, rim-vs-core 0.43, rim-vs-outside 0.15, heterogeneity 0.27; core [0.446, 0.458, 0.139, 0.491, 0.321] rim [0.334, 0.164, 0.169, 0.36, 0.06]
  - track 84 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 0.15, heterogeneity 0.27; core [0.464, 0.453, 0.123, 0.5, 0.368] rim [0.354, 0.146, 0.153, 0.368, 0.065]
  - track 532 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.14, heterogeneity 0.24; core [0.418, 0.484, 0.154, 0.465, 0.337] rim [0.33, 0.154, 0.173, 0.357, 0.069]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1111 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 3.97 (aggregate of 1111 individuals; 153/1111 membrane-like individually; rim level 0.453)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 6.01 (aggregate of 1111 individuals; 13/1111 membrane-like individually; rim level 0.234)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.856 (aggregate of 1111 individuals; 0/1111 membrane-like individually; rim level 0.176)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 4.02 (aggregate of 1111 individuals; 92/1111 membrane-like individually; rim level 0.472)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.3, rim/outside 12.3 (aggregate of 1111 individuals; 18/1111 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=6100, R_eq 4.65): none; #20 (t=6200, R_eq 5.29): none; #84 (t=6300, R_eq 5.11): none; #532 (t=10100, R_eq 4.44): none
- species `prey` (channels ['prey a'], own threshold): components final 189, mean 173.5, max 196; tracks 747, persistent 88; splits 156, persistent splits 59 (K=20), max generation 3, merges 60, merge/split 0.385; moving tracks 319
- species `predator` (channels ['predator b'], own threshold): components final 182, mean 144.5, max 192; tracks 598, persistent 81; splits 71, persistent splits 42 (K=20), max generation 3, merges 25, merge/split 0.352; moving tracks 299

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 1111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
