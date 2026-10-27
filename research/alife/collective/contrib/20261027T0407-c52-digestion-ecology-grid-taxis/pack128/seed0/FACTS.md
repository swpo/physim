# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 402s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/pack128/seed0 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1559, 1.797], min area 6 px

## Measurements
- components: final 45, mean 44.0, max 53; occupancy final 0.20
- tracks: 175; persistent (alive >= 50% of run): 24; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 43, 37], H1 [0, 0, 0]
- motion: 74 long-lived tracks moved >= 1 body length; max speed 0.00828/time; max body lengths 8.0
- replication (lineage window K = 20 frames = time 2000, default): splits 35, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 34, merge/split ratio 0.971, nucleations 72
- channel total drift (end/start - 1): [-0.0484, None, -0.6174, -0.6034, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.26; core [0.535, 0.386, 0.122, 0.582, 0.357] rim [0.325, 0.321, 0.157, 0.352, 0.199]
  - track 16 at frame 63: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.23; core [0.405, 0.505, 0.129, 0.429, 0.329] rim [0.395, 0.138, 0.138, 0.406, 0.077]
  - track 4 at frame 55: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.23; core [0.515, 0.437, 0.132, 0.555, 0.366] rim [0.272, 0.341, 0.176, 0.288, 0.161]
  - track 113 at frame 99: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.24; core [0.271, 0.492, 0.188, 0.3, 0.202] rim [0.395, 0.289, 0.164, 0.434, 0.184]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 278 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 3.77 (aggregate of 278 individuals; 35/278 membrane-like individually; rim level 0.448)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 6.27 (aggregate of 278 individuals; 5/278 membrane-like individually; rim level 0.231)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.855 (aggregate of 278 individuals; 0/278 membrane-like individually; rim level 0.174)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 3.84 (aggregate of 278 individuals; 25/278 membrane-like individually; rim level 0.467)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.293, rim/outside 12.2 (aggregate of 278 individuals; 5/278 membrane-like individually; rim level 0.143)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=6200, R_eq 4.92): none; #16 (t=6300, R_eq 4.95): none; #4 (t=5500, R_eq 4.48): none; #113 (t=9900, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 43.9, max 52; tracks 184, persistent 26; splits 38, persistent splits 17 (K=20), max generation 2, merges 18, merge/split 0.474; moving tracks 78
- species `predator` (channels ['predator b'], own threshold): components final 43, mean 36.9, max 52; tracks 134, persistent 23; splits 13, persistent splits 5 (K=20), max generation 1, merges 6, merge/split 0.462; moving tracks 76

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
