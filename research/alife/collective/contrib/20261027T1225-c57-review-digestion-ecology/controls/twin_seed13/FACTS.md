# Evidence pack: digestion-driven-predators (seed 13)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1310s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-work/twin --seeds 13 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1413, 0.8773], min area 6 px

## Measurements
- components: final 144, mean 137.8, max 147; occupancy final 0.19
- tracks: 149; persistent (alive >= 50% of run): 144; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [145, 144, 144], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 148
- channel total drift (end/start - 1): [0.0, None, -0.6417, -0.5827, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.07; core [0.893, 0.0, 0.043, 0.88, 0.0] rim [0.617, 0.0, 0.101, 0.608, 0.0]
  - track 1 at frame 61: holes 0, rim-vs-core 0.29, rim-vs-outside 0.58, heterogeneity 0.06; core [0.938, 0.0, 0.012, 0.878, 0.0] rim [0.724, 0.0, 0.071, 0.696, 0.0]
  - track 2 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.07; core [0.888, 0.0, 0.045, 0.874, 0.0] rim [0.607, 0.0, 0.101, 0.596, 0.0]
  - track 3 at frame 61: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.06; core [0.916, 0.0, 0.012, 0.846, 0.0] rim [0.696, 0.0, 0.076, 0.67, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 865 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 24.3 (aggregate of 865 individuals; 0/865 membrane-like individually; rim level 0.863)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 865 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 8.9, rim/outside 0.701 (aggregate of 865 individuals; 0/865 membrane-like individually; rim level 0.171)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 22.2 (aggregate of 865 individuals; 0/865 membrane-like individually; rim level 0.848)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 865 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 4.98): none; #1 (t=6100, R_eq 6.02): none; #2 (t=6100, R_eq 4.92): none; #3 (t=6100, R_eq 6.43): none
- species `prey` (channels ['prey a'], own threshold): components final 144, mean 141.4, max 151; tracks 164, persistent 144; splits 1, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 4; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
