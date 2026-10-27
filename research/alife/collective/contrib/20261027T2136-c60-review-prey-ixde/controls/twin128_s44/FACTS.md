# Evidence pack: digestion-driven-predators (seed 44)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 202s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/rev/twin128_s44 --seeds 44 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1398, 0.8776], min area 6 px

## Measurements
- components: final 38, mean 35.6, max 38; occupancy final 0.19
- tracks: 38; persistent (alive >= 50% of run): 38; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 38
- channel total drift (end/start - 1): [0.0, None, -0.6439, -0.5833, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 41: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.07; core [0.897, 0.0, 0.038, 0.873, 0.0] rim [0.627, 0.0, 0.093, 0.607, 0.0]
  - track 1 at frame 41: holes 0, rim-vs-core 0.37, rim-vs-outside 0.29, heterogeneity 0.06; core [0.891, 0.0, 0.032, 0.854, 0.0] rim [0.623, 0.0, 0.091, 0.6, 0.0]
  - track 2 at frame 41: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.07; core [0.894, 0.0, 0.04, 0.872, 0.0] rim [0.621, 0.0, 0.096, 0.604, 0.0]
  - track 3 at frame 41: holes 0, rim-vs-core 0.37, rim-vs-outside 0.29, heterogeneity 0.06; core [0.891, 0.0, 0.03, 0.847, 0.0] rim [0.623, 0.0, 0.09, 0.597, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 19.5 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.855)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 227 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 7.98, rim/outside 0.705 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.164)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 19 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.837)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 227 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=4100, R_eq 4.85): none; #1 (t=4100, R_eq 5.17): none; #2 (t=4100, R_eq 4.92): none; #3 (t=4100, R_eq 5.32): none
- species `prey` (channels ['prey a'], own threshold): components final 38, mean 36.9, max 38; tracks 40, persistent 38; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
