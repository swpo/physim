# Evidence pack: digestion-food-chain-3 (seed 0)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 479s; status ok
- command: `python -m labkit.run c52work/world3.py --out c52work/w3/c --seeds 0 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.11 of robust range [0.152, 3.1929], min area 6 px

## Measurements
- components: final 43, mean 41.1, max 54; occupancy final 0.21
- tracks: 95; persistent (alive >= 50% of run): 43; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.00479/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.625, nucleations 53
- channel total drift (end/start - 1): [-0.037, None, -0.6295, -0.5957, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 52: holes 0, rim-vs-core 0.26, rim-vs-outside 0.59, heterogeneity 0.21; core [0.775, 0.111, 0.062, 0.776, 0.193, 0.375, 0.177] rim [0.616, 0.147, 0.086, 0.62, 0.187, 0.247, 0.18]
  - track 9 at frame 52: holes 0, rim-vs-core 0.80, rim-vs-outside 0.24, heterogeneity 0.21; core [0.738, 0.26, 0.089, 0.764, 0.329, 0.547, 0.323] rim [0.441, 0.038, 0.129, 0.454, 0.046, 0.051, 0.039]
  - track 13 at frame 52: holes 0, rim-vs-core 0.67, rim-vs-outside 0.26, heterogeneity 0.20; core [0.816, 0.16, 0.041, 0.804, 0.235, 0.384, 0.217] rim [0.493, 0.051, 0.1, 0.487, 0.02, 0.013, 0.014]
  - track 38 at frame 66: holes 0, rim-vs-core 0.73, rim-vs-outside 0.26, heterogeneity 0.21; core [0.807, 0.179, 0.046, 0.801, 0.251, 0.451, 0.243] rim [0.475, 0.06, 0.105, 0.473, 0.024, 0.009, 0.017]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 256 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 10.1 (aggregate of 256 individuals; 13/256 membrane-like individually; rim level 0.679)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.172, rim/outside 1.24 (aggregate of 256 individuals; 0/256 membrane-like individually; rim level 0.088)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 3.22, rim/outside 0.786 (aggregate of 256 individuals; 0/256 membrane-like individually; rim level 0.167)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 10.4 (aggregate of 256 individuals; 13/256 membrane-like individually; rim level 0.673)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.16, rim/outside 8.42 (aggregate of 256 individuals; 4/256 membrane-like individually; rim level 0.0902)
  - radial top c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.31, rim/outside 19.9 (aggregate of 256 individuals; 1/256 membrane-like individually; rim level 0.195)
  - radial top product s2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.115, rim/outside 6.23 (aggregate of 256 individuals; 0/256 membrane-like individually; rim level 0.0544)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=5200, R_eq 4.65): none; #9 (t=5200, R_eq 4.15): none; #13 (t=5200, R_eq 5.14): none; #38 (t=6600, R_eq 5.11): none
- species `prey` (channels ['prey a'], own threshold): components final 42, mean 41.3, max 51; tracks 86, persistent 44; splits 9, persistent splits 6 (K=20), max generation 1, merges 4, merge/split 0.444; moving tracks 26
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 8.7, max 45; tracks 74, persistent 0; splits 4, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.25; moving tracks 23
- species `top` (channels ['top c'], own threshold): components final 43, mean 25.8, max 48; tracks 50, persistent 43; splits 0, persistent splits 0 (K=20), max generation 0, merges 1, merge/split n/a; moving tracks 15

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
