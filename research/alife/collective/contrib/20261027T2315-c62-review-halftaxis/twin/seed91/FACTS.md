# Evidence pack: digestion-predators-half-taxis (seed 91)

- world: `../../../20261027T2013-c60-halftaxis-ecology/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1286s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2013-c60-halftaxis-ecology/world.py --out collective/contrib/20261027T2315-c62-review-halftaxis/twin/seed91 --seeds 91 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1405, 0.8783], min area 6 px

## Measurements
- components: final 152, mean 145.1, max 152; occupancy final 0.19
- tracks: 156; persistent (alive >= 50% of run): 152; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [152, 152, 152], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 154
- channel total drift (end/start - 1): [-0.0, None, -0.6441, -0.582, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.28, rim-vs-outside 0.52, heterogeneity 0.06; core [0.908, 0.0, 0.019, 0.857, 0.0] rim [0.699, 0.0, 0.072, 0.672, 0.0]
  - track 1 at frame 61: holes 0, rim-vs-core 0.36, rim-vs-outside 0.29, heterogeneity 0.06; core [0.894, 0.0, 0.031, 0.855, 0.0] rim [0.633, 0.0, 0.089, 0.609, 0.0]
  - track 2 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.06; core [0.891, 0.0, 0.035, 0.859, 0.0] rim [0.618, 0.0, 0.094, 0.598, 0.0]
  - track 3 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.39, heterogeneity 0.06; core [0.903, 0.0, 0.027, 0.863, 0.0] rim [0.699, 0.0, 0.081, 0.68, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 912 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 22.5 (aggregate of 912 individuals; 0/912 membrane-like individually; rim level 0.859)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 912 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 8.23, rim/outside 0.703 (aggregate of 912 individuals; 0/912 membrane-like individually; rim level 0.167)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 21.1 (aggregate of 912 individuals; 0/912 membrane-like individually; rim level 0.842)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 912 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 6.41): none; #1 (t=6100, R_eq 5.17): none; #2 (t=6100, R_eq 5.08): none; #3 (t=6200, R_eq 5.84): none
- species `prey` (channels ['prey a'], own threshold): components final 152, mean 148.8, max 154; tracks 176, persistent 152; splits 0, persistent splits 0 (K=20), max generation 0, merges 6, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
