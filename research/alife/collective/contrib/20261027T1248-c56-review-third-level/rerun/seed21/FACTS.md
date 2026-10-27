# Evidence pack: digestion-food-chain-3 (seed 21)

- world: `../../../collective/contrib/20261027T0407-c52-third-level-negative/world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 624s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0407-c52-third-level-negative/world3.py --out c56work/t3/s21 --seeds 21 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1594, 2.5991], min area 6 px

## Measurements
- components: final 43, mean 41.2, max 51; occupancy final 0.24
- tracks: 84; persistent (alive >= 50% of run): 44; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.00384/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.5, nucleations 49
- channel total drift (end/start - 1): [-0.0251, None, -0.6372, -0.5896, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.77, rim-vs-outside 0.34, heterogeneity 0.20; core [0.831, 0.22, 0.043, 0.818, 0.307, 0.489, 0.355] rim [0.482, 0.103, 0.103, 0.475, 0.061, 0.06, 0.045]
  - track 4 at frame 62: holes 0, rim-vs-core 0.83, rim-vs-outside 0.25, heterogeneity 0.19; core [0.782, 0.202, 0.061, 0.777, 0.256, 0.536, 0.322] rim [0.401, 0.094, 0.12, 0.403, 0.045, 0.021, 0.035]
  - track 8 at frame 62: holes 0, rim-vs-core 0.84, rim-vs-outside 0.26, heterogeneity 0.20; core [0.781, 0.214, 0.067, 0.786, 0.281, 0.508, 0.348] rim [0.401, 0.1, 0.126, 0.409, 0.05, 0.006, 0.038]
  - track 43 at frame 77: holes 0, rim-vs-core 0.74, rim-vs-outside 0.39, heterogeneity 0.20; core [0.822, 0.224, 0.04, 0.805, 0.305, 0.536, 0.371] rim [0.503, 0.121, 0.103, 0.499, 0.08, 0.096, 0.063]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 261 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 14 (aggregate of 261 individuals; 10/261 membrane-like individually; rim level 0.682)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.448, rim/outside 2.53 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.176)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.9, rim/outside 0.796 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.175)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 13.4 (aggregate of 261 individuals; 6/261 membrane-like individually; rim level 0.668)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.316, rim/outside 14 (aggregate of 261 individuals; 1/261 membrane-like individually; rim level 0.175)
  - radial top c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.316, rim/outside 21.5 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.206)
  - radial top product s2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.172, rim/outside 10.1 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.0956)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 5.41): none; #4 (t=6200, R_eq 4.95): none; #8 (t=6200, R_eq 4.92): none; #43 (t=7700, R_eq 5.78): none
- species `prey` (channels ['prey a'], own threshold): components final 43, mean 41.6, max 48; tracks 80, persistent 44; splits 11, persistent splits 8 (K=20), max generation 1, merges 2, merge/split 0.182; moving tracks 28
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 6.6, max 45; tracks 63, persistent 0; splits 7, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 18
- species `top` (channels ['top c'], own threshold): components final 43, mean 29.0, max 45; tracks 47, persistent 44; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 7

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
