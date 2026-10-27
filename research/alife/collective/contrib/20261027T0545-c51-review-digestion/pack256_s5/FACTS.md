# Evidence pack: digestion-driven-predators (seed 5)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1510s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/20261027T0545-c51-review-digestion/pack256_s5 --seeds 5 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1563, 1.7952], min area 6 px

## Measurements
- components: final 193, mean 177.7, max 204; occupancy final 0.21
- tracks: 774; persistent (alive >= 50% of run): 78; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [200, 192, 167], H1 [0, 0, 0]
- motion: 321 long-lived tracks moved >= 1 body length; max speed 0.00841/time; max body lengths 9.7
- replication (lineage window K = 20 frames = time 2000, default): splits 143, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 4, merges 157, merge/split ratio 1.1, nucleations 332
- channel total drift (end/start - 1): [-0.0548, None, -0.6148, -0.6033, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 62: holes 0, rim-vs-core 0.45, rim-vs-outside 0.19, heterogeneity 0.25; core [0.576, 0.377, 0.111, 0.62, 0.319] rim [0.379, 0.143, 0.144, 0.407, 0.073]
  - track 41 at frame 62: holes 0, rim-vs-core 0.46, rim-vs-outside 0.19, heterogeneity 0.27; core [0.567, 0.404, 0.103, 0.613, 0.368] rim [0.401, 0.149, 0.137, 0.428, 0.075]
  - track 67 at frame 63: holes 0, rim-vs-core 0.51, rim-vs-outside 0.13, heterogeneity 0.24; core [0.383, 0.542, 0.156, 0.428, 0.394] rim [0.311, 0.164, 0.18, 0.334, 0.076]
  - track 603 at frame 106: holes 0, rim-vs-core 0.47, rim-vs-outside 0.14, heterogeneity 0.25; core [0.412, 0.494, 0.14, 0.45, 0.362] rim [0.317, 0.16, 0.161, 0.336, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1123 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 3.97 (aggregate of 1123 individuals; 135/1123 membrane-like individually; rim level 0.461)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.345, rim/outside 6.01 (aggregate of 1123 individuals; 17/1123 membrane-like individually; rim level 0.23)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.852 (aggregate of 1123 individuals; 0/1123 membrane-like individually; rim level 0.172)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 4.05 (aggregate of 1123 individuals; 81/1123 membrane-like individually; rim level 0.477)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.29, rim/outside 12.3 (aggregate of 1123 individuals; 20/1123 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=6200, R_eq 4.48): none; #41 (t=6200, R_eq 4.75): none; #67 (t=6300, R_eq 4.82): none; #603 (t=10600, R_eq 4.65): none
- species `prey` (channels ['prey a'], own threshold): components final 187, mean 176.9, max 197; tracks 733, persistent 104; splits 142, persistent splits 67 (K=20), max generation 4, merges 57, merge/split 0.401; moving tracks 320
- species `predator` (channels ['predator b'], own threshold): components final 187, mean 147.0, max 193; tracks 589, persistent 87; splits 69, persistent splits 40 (K=20), max generation 3, merges 14, merge/split 0.203; moving tracks 309

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
