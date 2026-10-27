# Evidence pack: digestion-driven-predators (seed 8)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1393s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/py/twin256_s8 --seeds 8 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1413, 0.8773], min area 6 px

## Measurements
- components: final 147, mean 141.1, max 148; occupancy final 0.19
- tracks: 150; persistent (alive >= 50% of run): 147; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [148, 147, 147], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00093/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 149
- channel total drift (end/start - 1): [0.0, None, -0.6441, -0.584, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.06; core [0.888, 0.0, 0.032, 0.849, 0.0] rim [0.612, 0.0, 0.097, 0.595, 0.0]
  - track 1 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.07; core [0.889, 0.0, 0.044, 0.873, 0.0] rim [0.604, 0.0, 0.101, 0.593, 0.0]
  - track 2 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.07; core [0.888, 0.0, 0.042, 0.868, 0.0] rim [0.602, 0.0, 0.101, 0.589, 0.0]
  - track 3 at frame 61: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.06; core [0.902, 0.0, 0.034, 0.874, 0.0] rim [0.64, 0.0, 0.096, 0.627, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 882 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 23.2 (aggregate of 882 individuals; 0/882 membrane-like individually; rim level 0.86)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 882 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 8.77, rim/outside 0.702 (aggregate of 882 individuals; 0/882 membrane-like individually; rim level 0.169)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 21.5 (aggregate of 882 individuals; 0/882 membrane-like individually; rim level 0.843)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 882 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 5.56): none; #1 (t=6100, R_eq 4.98): none; #2 (t=6100, R_eq 5.05): none; #3 (t=6100, R_eq 5.29): none
- species `prey` (channels ['prey a'], own threshold): components final 147, mean 144.5, max 149; tracks 162, persistent 147; splits 0, persistent splits 0 (K=20), max generation 0, merges 4, merge/split n/a; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
