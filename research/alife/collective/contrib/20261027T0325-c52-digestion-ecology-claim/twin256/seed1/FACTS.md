# Evidence pack: digestion-driven-predators (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1234s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/twin256/seed1 --seeds 1 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1395, 0.8792], min area 6 px

## Measurements
- components: final 146, mean 139.8, max 146; occupancy final 0.18
- tracks: 150; persistent (alive >= 50% of run): 146; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [146, 146, 146], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000838/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 148
- channel total drift (end/start - 1): [0.0, None, -0.6391, -0.5783, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.37, rim-vs-outside 0.29, heterogeneity 0.06; core [0.887, 0.0, 0.031, 0.845, 0.0] rim [0.614, 0.0, 0.095, 0.596, 0.0]
  - track 1 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.07; core [0.885, 0.0, 0.036, 0.855, 0.0] rim [0.599, 0.0, 0.099, 0.584, 0.0]
  - track 2 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.07; core [0.891, 0.0, 0.041, 0.873, 0.0] rim [0.605, 0.0, 0.101, 0.593, 0.0]
  - track 3 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.07; core [0.893, 0.0, 0.034, 0.864, 0.0] rim [0.614, 0.0, 0.099, 0.601, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 876 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 24.4 (aggregate of 876 individuals; 0/876 membrane-like individually; rim level 0.864)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 876 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 9.31, rim/outside 0.698 (aggregate of 876 individuals; 0/876 membrane-like individually; rim level 0.171)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 22.3 (aggregate of 876 individuals; 0/876 membrane-like individually; rim level 0.85)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 876 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 5.59): none; #1 (t=6100, R_eq 5.32): none; #2 (t=6100, R_eq 5.01): none; #3 (t=6100, R_eq 5.38): none
- species `prey` (channels ['prey a'], own threshold): components final 146, mean 143.1, max 148; tracks 161, persistent 146; splits 0, persistent splits 0 (K=20), max generation 0, merges 3, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
