# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 259s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/lks/x2 --seeds 0 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1508, 1.8138], min area 6 px

## Measurements
- components: final 48, mean 40.7, max 51; occupancy final 0.21
- tracks: 102; persistent (alive >= 50% of run): 33; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 48, 41], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.0075/time; max body lengths 5.1
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 15, merge/split ratio 0.938, nucleations 55
- channel total drift (end/start - 1): [-0.0495, None, -0.6191, -0.6023, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 41: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.24; core [0.263, 0.484, 0.2, 0.291, 0.215] rim [0.384, 0.243, 0.179, 0.417, 0.172]
  - track 5 at frame 42: holes 0, rim-vs-core 0.36, rim-vs-outside 0.13, heterogeneity 0.22; core [0.251, 0.541, 0.211, 0.274, 0.217] rim [0.256, 0.217, 0.211, 0.274, 0.062]
  - track 9 at frame 42: holes 0, rim-vs-core 0.37, rim-vs-outside 0.14, heterogeneity 0.20; core [0.34, 0.495, 0.177, 0.366, 0.241] rim [0.27, 0.187, 0.19, 0.286, 0.064]
  - track 76 at frame 69: holes 0, rim-vs-core 0.43, rim-vs-outside 0.17, heterogeneity 0.26; core [0.43, 0.481, 0.175, 0.49, 0.347] rim [0.314, 0.199, 0.2, 0.353, 0.079]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 267 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 4.3 (aggregate of 267 individuals; 36/267 membrane-like individually; rim level 0.469)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.342, rim/outside 5.26 (aggregate of 267 individuals; 3/267 membrane-like individually; rim level 0.224)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.853 (aggregate of 267 individuals; 0/267 membrane-like individually; rim level 0.188)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 4.38 (aggregate of 267 individuals; 21/267 membrane-like individually; rim level 0.488)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.276, rim/outside 12 (aggregate of 267 individuals; 5/267 membrane-like individually; rim level 0.14)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=4100, R_eq 5.26): ['prey a', 'product p']; #5 (t=4200, R_eq 5.23): none; #9 (t=4200, R_eq 4.33): none; #76 (t=6900, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 48, mean 41.1, max 50; tracks 119, persistent 31; splits 23, persistent splits 13 (K=20), max generation 2, merges 6, merge/split 0.261; moving tracks 54
- species `predator` (channels ['predator b'], own threshold): components final 44, mean 30.6, max 48; tracks 98, persistent 23; splits 14, persistent splits 10 (K=20), max generation 2, merges 2, merge/split 0.143; moving tracks 51

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
