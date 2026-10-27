# Evidence pack: digestion-driven-predators (seed 2)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1716s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/20261027T0438-c52-digestion-ecology-seed2-localcut/pack256/seed2 --seeds 2 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.158, 1.7933], min area 6 px

## Measurements
- components: final 190, mean 171.2, max 198; occupancy final 0.20
- tracks: 795; persistent (alive >= 50% of run): 71; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [193, 180, 157], H1 [0, 0, 0]
- motion: 323 long-lived tracks moved >= 1 body length; max speed 0.00823/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 2000, default): splits 141, persistent splits 38 (0 more failed only because the siblings re-merged within K), max generation 3, merges 177, merge/split ratio 1.25, nucleations 341
- channel total drift (end/start - 1): [-0.0514, None, -0.6126, -0.6003, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 0.15, heterogeneity 0.21; core [0.394, 0.475, 0.155, 0.429, 0.249] rim [0.329, 0.181, 0.169, 0.351, 0.067]
  - track 13 at frame 62: holes 0, rim-vs-core 0.30, rim-vs-outside 0.13, heterogeneity 0.20; core [0.357, 0.445, 0.172, 0.391, 0.186] rim [0.286, 0.193, 0.185, 0.308, 0.057]
  - track 41 at frame 62: holes 0, rim-vs-core 0.48, rim-vs-outside 0.16, heterogeneity 0.25; core [0.421, 0.506, 0.164, 0.48, 0.366] rim [0.325, 0.155, 0.184, 0.363, 0.074]
  - track 599 at frame 108: holes 0, rim-vs-core 0.41, rim-vs-outside 0.14, heterogeneity 0.25; core [0.414, 0.466, 0.157, 0.456, 0.292] rim [0.292, 0.18, 0.18, 0.314, 0.064]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1100 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 3.92 (aggregate of 1100 individuals; 144/1100 membrane-like individually; rim level 0.459)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.351, rim/outside 5.93 (aggregate of 1100 individuals; 22/1100 membrane-like individually; rim level 0.232)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.853 (aggregate of 1100 individuals; 0/1100 membrane-like individually; rim level 0.175)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 3.98 (aggregate of 1100 individuals; 87/1100 membrane-like individually; rim level 0.476)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.303, rim/outside 12.2 (aggregate of 1100 individuals; 24/1100 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=6200, R_eq 4.51): ['prey a']; #13 (t=6200, R_eq 4.51): none; #41 (t=6200, R_eq 4.48): none; #599 (t=10800, R_eq 4.85): none
- species `prey` (channels ['prey a'], own threshold): components final 182, mean 170.2, max 193; tracks 744, persistent 88; splits 141, persistent splits 51 (K=20), max generation 4, merges 72, merge/split 0.511; moving tracks 317
- species `predator` (channels ['predator b'], own threshold): components final 178, mean 141.7, max 188; tracks 592, persistent 80; splits 61, persistent splits 37 (K=20), max generation 3, merges 27, merge/split 0.443; moving tracks 300

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1100 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
