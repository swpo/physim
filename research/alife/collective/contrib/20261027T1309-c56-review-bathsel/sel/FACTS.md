# Evidence pack: digestion-predators-bath-mutation (seed 24)

- world: `../../../collective/contrib/20261027T0519-c52-bath-mutation-selection/world2m.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 598s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0519-c52-bath-mutation-selection/world2m.py --out c56work/bs/sel --seeds 24 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1586, 1.8149], min area 6 px

## Measurements
- components: final 47, mean 44.1, max 53; occupancy final 0.20
- tracks: 192; persistent (alive >= 50% of run): 25; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 46, 39], H1 [0, 0, 0]
- motion: 69 long-lived tracks moved >= 1 body length; max speed 0.00806/time; max body lengths 7.7
- replication (lineage window K = 20 frames = time 2000, default): splits 38, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 4, merges 37, merge/split ratio 0.974, nucleations 79
- channel total drift (end/start - 1): [-0.0408, None, -0.6179, -0.6016, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 63: holes 0, rim-vs-core 0.53, rim-vs-outside 0.17, heterogeneity 0.18; core [0.378, 0.183, 0.18, 0.426, 0.03, 0.561, 0.401] rim [0.33, 0.205, 0.191, 0.361, 0.035, 0.146, 0.089]
  - track 24 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 0.37, heterogeneity 0.16; core [0.418, 0.069, 0.145, 0.459, 0.005, 0.511, 0.33] rim [0.509, 0.067, 0.14, 0.553, 0.006, 0.116, 0.102]
  - track 31 at frame 64: holes 0, rim-vs-core 0.49, rim-vs-outside 0.18, heterogeneity 0.16; core [0.337, 0.0, 0.212, 0.399, 0.0, 0.595, 0.347] rim [0.318, 0.007, 0.219, 0.368, 0.0, 0.181, 0.094]
  - track 149 at frame 103: holes 0, rim-vs-core 0.33, rim-vs-outside 0.35, heterogeneity 0.15; core [0.651, 0.0, 0.038, 0.629, 0.0, 0.324, 0.241] rim [0.553, 0.016, 0.072, 0.533, 0.001, 0.093, 0.048]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 276 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 4.65 (aggregate of 276 individuals; 25/276 membrane-like individually; rim level 0.484)
  - radial predator b: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.867 (aggregate of 276 individuals; 3/276 membrane-like individually; rim level 0.179)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.849 (aggregate of 276 individuals; 0/276 membrane-like individually; rim level 0.182)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 4.72 (aggregate of 276 individuals; 14/276 membrane-like individually; rim level 0.502)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 2.44 (aggregate of 276 individuals; 6/276 membrane-like individually; rim level 0.0771)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 7.33 (aggregate of 276 individuals; 6/276 membrane-like individually; rim level 0.212)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.286, rim/outside 12.5 (aggregate of 276 individuals; 5/276 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=6300, R_eq 4.37): none; #24 (t=6300, R_eq 3.95): none; #31 (t=6400, R_eq 4.07): none; #149 (t=10300, R_eq 6.26): none
- species `prey` (channels ['prey a'], own threshold): components final 42, mean 44.2, max 53; tracks 193, persistent 24; splits 39, persistent splits 19 (K=20), max generation 4, merges 21, merge/split 0.538; moving tracks 77
- species `predator` (channels ['predator b'], own threshold): components final 16, mean 12.0, max 24; tracks 205, persistent 0; splits 36, persistent splits 0 (K=20), max generation 0, merges 17, merge/split 0.472; moving tracks 8
- species `predator_e` (channels ['predator e'], own threshold): components final 38, mean 34.9, max 49; tracks 142, persistent 21; splits 16, persistent splits 8 (K=20), max generation 2, merges 4, merge/split 0.25; moving tracks 79

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
