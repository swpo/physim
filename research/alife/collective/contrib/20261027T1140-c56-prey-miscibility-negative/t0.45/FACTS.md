# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 325s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/ma/t0.45 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1299, 0.8825], min area 6 px

## Measurements
- components: final 29, mean 27.4, max 29; occupancy final 0.17
- tracks: 29; persistent (alive >= 50% of run): 29; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 29], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 29
- channel total drift (end/start - 1): [-0.0, None, -0.6051, -0.5513, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.06; core [0.894, 0.0, 0.037, 0.861, 0.0] rim [0.617, 0.0, 0.113, 0.613, 0.0]
  - track 1 at frame 62: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.07; core [0.903, 0.0, 0.045, 0.89, 0.0] rim [0.622, 0.0, 0.114, 0.62, 0.0]
  - track 2 at frame 62: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.06; core [0.898, 0.0, 0.038, 0.87, 0.0] rim [0.626, 0.0, 0.112, 0.622, 0.0]
  - track 3 at frame 62: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.06; core [0.902, 0.0, 0.04, 0.88, 0.0] rim [0.633, 0.0, 0.111, 0.63, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 28.9 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.876)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 174 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.9, rim/outside 0.686 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.199)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 26.9 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.872)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 174 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 5.92): none; #1 (t=6200, R_eq 5.35): none; #2 (t=6200, R_eq 5.75): none; #3 (t=6200, R_eq 5.61): none
- species `prey` (channels ['prey a'], own threshold): components final 29, mean 28.0, max 29; tracks 30, persistent 29; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
