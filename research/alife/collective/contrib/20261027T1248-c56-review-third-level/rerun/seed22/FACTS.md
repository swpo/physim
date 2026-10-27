# Evidence pack: digestion-food-chain-3 (seed 22)

- world: `../../../collective/contrib/20261027T0407-c52-third-level-negative/world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 629s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0407-c52-third-level-negative/world3.py --out c56work/t3/s22 --seeds 22 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1554, 2.5884], min area 6 px

## Measurements
- components: final 42, mean 41.3, max 51; occupancy final 0.24
- tracks: 91; persistent (alive >= 50% of run): 43; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.0037/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.833, nucleations 56
- channel total drift (end/start - 1): [-0.025, None, -0.6382, -0.5927, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 62: holes 0, rim-vs-core 0.83, rim-vs-outside 0.25, heterogeneity 0.20; core [0.786, 0.21, 0.064, 0.795, 0.288, 0.496, 0.327] rim [0.405, 0.098, 0.125, 0.417, 0.049, 0.012, 0.033]
  - track 12 at frame 62: holes 0, rim-vs-core 0.82, rim-vs-outside 0.25, heterogeneity 0.20; core [0.802, 0.206, 0.044, 0.787, 0.273, 0.497, 0.306] rim [0.42, 0.099, 0.112, 0.419, 0.046, 0.006, 0.027]
  - track 13 at frame 62: holes 0, rim-vs-core 0.81, rim-vs-outside 0.24, heterogeneity 0.20; core [0.763, 0.215, 0.061, 0.759, 0.286, 0.477, 0.325] rim [0.388, 0.103, 0.118, 0.389, 0.05, 0.009, 0.033]
  - track 52 at frame 77: holes 0, rim-vs-core 0.81, rim-vs-outside 0.24, heterogeneity 0.20; core [0.789, 0.207, 0.048, 0.777, 0.279, 0.469, 0.308] rim [0.405, 0.098, 0.115, 0.405, 0.045, 0.001, 0.026]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 261 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 11.9 (aggregate of 261 individuals; 6/261 membrane-like individually; rim level 0.681)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.466, rim/outside 2.66 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.185)
  - radial fuel F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 4, rim/outside 0.794 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.173)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 11.8 (aggregate of 261 individuals; 4/261 membrane-like individually; rim level 0.669)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.313, rim/outside 14.1 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.179)
  - radial top c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.33, rim/outside 21.1 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.208)
  - radial top product s2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.175, rim/outside 9.82 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.0935)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=6200, R_eq 5.01): none; #12 (t=6200, R_eq 5.5): none; #13 (t=6200, R_eq 5.01): none; #52 (t=7700, R_eq 5.44): none
- species `prey` (channels ['prey a'], own threshold): components final 42, mean 41.5, max 49; tracks 80, persistent 42; splits 7, persistent splits 5 (K=20), max generation 1, merges 1, merge/split 0.143; moving tracks 28
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 6.9, max 45; tracks 65, persistent 0; splits 4, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 24
- species `top` (channels ['top c'], own threshold): components final 42, mean 28.0, max 45; tracks 51, persistent 41; splits 0, persistent splits 0 (K=20), max generation 0, merges 1, merge/split n/a; moving tracks 7

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
