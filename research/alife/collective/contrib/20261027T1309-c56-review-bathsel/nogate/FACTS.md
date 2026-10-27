# Evidence pack: digestion-predators-bath-mutation (seed 24)

- world: `../../../collective/contrib/20261027T0519-c52-bath-mutation-selection/world2m.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 591s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0519-c52-bath-mutation-selection/world2m.py --out c56work/bs/nogate --seeds 24 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.19 of robust range [0.1586, 1.9469], min area 6 px

## Measurements
- components: final 41, mean 42.1, max 50; occupancy final 0.20
- tracks: 143; persistent (alive >= 50% of run): 24; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 38, 33], H1 [0, 0, 0]
- motion: 67 long-lived tracks moved >= 1 body length; max speed 0.00701/time; max body lengths 8.3
- replication (lineage window K = 20 frames = time 2000, default): splits 31, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 19, merge/split ratio 0.613, nucleations 62
- channel total drift (end/start - 1): [-0.0357, None, -0.6147, -0.6037, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 63: holes 0, rim-vs-core 0.64, rim-vs-outside 0.21, heterogeneity 0.27; core [0.55, 0.478, 0.181, 0.629, 0.427, 0.421, 0.42] rim [0.357, 0.345, 0.216, 0.41, 0.154, 0.087, 0.074]
  - track 18 at frame 63: holes 0, rim-vs-core 0.72, rim-vs-outside 0.20, heterogeneity 0.24; core [0.531, 0.505, 0.156, 0.579, 0.533, 0.458, 0.491] rim [0.389, 0.316, 0.181, 0.413, 0.2, 0.054, 0.099]
  - track 20 at frame 63: holes 0, rim-vs-core 0.60, rim-vs-outside 0.20, heterogeneity 0.25; core [0.482, 0.535, 0.182, 0.542, 0.457, 0.428, 0.356] rim [0.33, 0.362, 0.208, 0.364, 0.181, 0.093, 0.067]
  - track 122 at frame 107: holes 0, rim-vs-core 0.25, rim-vs-outside 0.12, heterogeneity 0.07; core [0.305, 0.537, 0.194, 0.303, 0.336, 0.213, 0.037] rim [0.285, 0.379, 0.197, 0.281, 0.184, 0.105, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 263 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 5.4 (aggregate of 263 individuals; 7/263 membrane-like individually; rim level 0.525)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.637, rim/outside 2.4 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.353)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.6, rim/outside 0.849 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.205)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 5.47 (aggregate of 263 individuals; 7/263 membrane-like individually; rim level 0.544)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.423, rim/outside 8.44 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.265)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.265, rim/outside 7.5 (aggregate of 263 individuals; 1/263 membrane-like individually; rim level 0.156)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.237, rim/outside 11.4 (aggregate of 263 individuals; 2/263 membrane-like individually; rim level 0.124)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=6300, R_eq 4.37): none; #18 (t=6300, R_eq 4.22): none; #20 (t=6300, R_eq 4.33): none; #122 (t=10700, R_eq 3.7): none
- species `prey` (channels ['prey a'], own threshold): components final 40, mean 42.3, max 50; tracks 161, persistent 23; splits 37, persistent splits 19 (K=20), max generation 4, merges 13, merge/split 0.351; moving tracks 74
- species `predator` (channels ['predator b'], own threshold): components final 39, mean 34.6, max 49; tracks 148, persistent 22; splits 19, persistent splits 11 (K=20), max generation 2, merges 6, merge/split 0.316; moving tracks 71
- species `predator_e` (channels ['predator e'], own threshold): components final 32, mean 30.7, max 45; tracks 126, persistent 17; splits 2, persistent splits 0 (K=20), max generation 0, merges 2, merge/split 1; moving tracks 71

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
