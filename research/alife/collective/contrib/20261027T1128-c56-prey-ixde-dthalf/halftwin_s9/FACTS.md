# Evidence pack: digestion-driven-predators (seed 9)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 1000 steps x dt 0.2 = time 24000; grid [128, 128]; wall 645s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/dh/halftwin_s9 --seeds 9 --size 128 128 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1406, 0.8797], min area 6 px

## Measurements
- components: final 39, mean 37.5, max 39; occupancy final 0.18
- tracks: 40; persistent (alive >= 50% of run): 39; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 4000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 40
- channel total drift (end/start - 1): [0.0, None, -0.6435, -0.5798, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.07; core [0.894, 0.0, 0.036, 0.867, 0.0] rim [0.621, 0.0, 0.095, 0.604, 0.0]
  - track 1 at frame 62: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.06; core [0.894, 0.0, 0.038, 0.871, 0.0] rim [0.627, 0.0, 0.095, 0.61, 0.0]
  - track 2 at frame 62: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.07; core [0.892, 0.0, 0.043, 0.876, 0.0] rim [0.619, 0.0, 0.097, 0.604, 0.0]
  - track 3 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.06; core [0.903, 0.0, 0.046, 0.894, 0.0] rim [0.654, 0.0, 0.094, 0.64, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 234 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 22.3 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.858)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 234 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 7.93, rim/outside 0.703 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.165)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 20.7 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.84)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 234 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=12400, R_eq 5.05): none; #1 (t=12400, R_eq 4.89): none; #2 (t=12400, R_eq 4.75): none; #3 (t=12400, R_eq 4.37): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 38.4, max 39; tracks 41, persistent 39; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
