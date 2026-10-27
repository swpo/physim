# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 327s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/ma/t0.5 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1191, 0.8766], min area 6 px

## Measurements
- components: final 20, mean 16.3, max 20; occupancy final 0.16
- tracks: 23; persistent (alive >= 50% of run): 17; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 22, 20], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 17
- channel total drift (end/start - 1): [0.0, None, -0.5546, -0.5173, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.30, rim-vs-outside 0.55, heterogeneity 0.06; core [0.956, 0.0, 0.024, 0.896, 0.0] rim [0.728, 0.0, 0.104, 0.711, 0.0]
  - track 1 at frame 62: holes 0, rim-vs-core 0.32, rim-vs-outside 0.55, heterogeneity 0.06; core [0.961, 0.0, 0.026, 0.908, 0.0] rim [0.722, 0.0, 0.109, 0.71, 0.0]
  - track 2 at frame 63: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.06; core [0.926, 0.0, 0.043, 0.886, 0.0] rim [0.664, 0.0, 0.124, 0.657, 0.0]
  - track 17 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.07; core [0.925, 0.0, 0.059, 0.924, 0.0] rim [0.746, 0.0, 0.112, 0.756, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 106 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 20 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.834)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 106 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.7, rim/outside 0.665 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.231)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 19.9 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.809)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 106 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 6.26): none; #1 (t=6200, R_eq 6.13): none; #2 (t=6300, R_eq 5.94): none; #17 (t=10100, R_eq 5.53): none
- species `prey` (channels ['prey a'], own threshold): components final 19, mean 16.6, max 19; tracks 21, persistent 17; splits 2, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
