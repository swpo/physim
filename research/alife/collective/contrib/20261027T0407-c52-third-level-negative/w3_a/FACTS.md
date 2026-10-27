# Evidence pack: digestion-food-chain-3 (seed 0)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 575s; status ok
- command: `python -m labkit.run c52work/world3.py --out c52work/w3/a --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1559, 2.6067], min area 6 px

## Measurements
- components: final 46, mean 42.6, max 54; occupancy final 0.24
- tracks: 85; persistent (alive >= 50% of run): 46; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 46, 46], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.00286/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.538, nucleations 52
- channel total drift (end/start - 1): [-0.0252, None, -0.6397, -0.5891, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 62: holes 0, rim-vs-core 0.32, rim-vs-outside 0.58, heterogeneity 0.20; core [0.761, 0.195, 0.052, 0.74, 0.247, 0.4, 0.263] rim [0.577, 0.158, 0.081, 0.566, 0.169, 0.24, 0.184]
  - track 5 at frame 62: holes 0, rim-vs-core 0.80, rim-vs-outside 0.26, heterogeneity 0.19; core [0.765, 0.219, 0.071, 0.769, 0.29, 0.481, 0.33] rim [0.404, 0.096, 0.122, 0.409, 0.054, 0.014, 0.04]
  - track 9 at frame 62: holes 0, rim-vs-core 0.83, rim-vs-outside 0.25, heterogeneity 0.20; core [0.772, 0.22, 0.064, 0.769, 0.291, 0.513, 0.34] rim [0.4, 0.101, 0.119, 0.402, 0.053, 0.012, 0.039]
  - track 38 at frame 77: holes 0, rim-vs-core 0.83, rim-vs-outside 0.26, heterogeneity 0.20; core [0.8, 0.217, 0.048, 0.789, 0.296, 0.491, 0.332] rim [0.421, 0.104, 0.114, 0.422, 0.052, 0.005, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 273 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 13.2 (aggregate of 273 individuals; 10/273 membrane-like individually; rim level 0.679)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.431, rim/outside 2.51 (aggregate of 273 individuals; 0/273 membrane-like individually; rim level 0.177)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.7, rim/outside 0.796 (aggregate of 273 individuals; 0/273 membrane-like individually; rim level 0.17)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 13.1 (aggregate of 273 individuals; 10/273 membrane-like individually; rim level 0.664)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.312, rim/outside 14.5 (aggregate of 273 individuals; 1/273 membrane-like individually; rim level 0.181)
  - radial top c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.326, rim/outside 21.7 (aggregate of 273 individuals; 0/273 membrane-like individually; rim level 0.208)
  - radial top product s2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.177, rim/outside 10.2 (aggregate of 273 individuals; 0/273 membrane-like individually; rim level 0.0958)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6200, R_eq 5.14): none; #5 (t=6200, R_eq 4.62): none; #9 (t=6200, R_eq 4.79): none; #38 (t=7700, R_eq 5.29): none
- species `prey` (channels ['prey a'], own threshold): components final 46, mean 43.1, max 51; tracks 86, persistent 46; splits 9, persistent splits 6 (K=20), max generation 1, merges 4, merge/split 0.444; moving tracks 23
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 6.6, max 45; tracks 58, persistent 0; splits 3, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 23
- species `top` (channels ['top c'], own threshold): components final 46, mean 30.5, max 48; tracks 50, persistent 45; splits 0, persistent splits 0 (K=20), max generation 0, merges 1, merge/split n/a; moving tracks 6

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
