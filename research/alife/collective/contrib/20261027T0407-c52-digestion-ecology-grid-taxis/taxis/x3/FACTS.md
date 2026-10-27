# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 261s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/lks/x3 --seeds 0 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1508, 1.7686], min area 6 px

## Measurements
- components: final 51, mean 42.1, max 52; occupancy final 0.18
- tracks: 159; persistent (alive >= 50% of run): 24; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 47, 40], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.00847/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 2000, default): splits 24, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 33, merge/split ratio 1.38, nucleations 78
- channel total drift (end/start - 1): [-0.0491, None, -0.6161, -0.6043, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 43: holes 0, rim-vs-core 0.48, rim-vs-outside 0.15, heterogeneity 0.24; core [0.435, 0.495, 0.14, 0.485, 0.385] rim [0.347, 0.149, 0.159, 0.378, 0.083]
  - track 13 at frame 39: holes 0, rim-vs-core 0.46, rim-vs-outside 0.14, heterogeneity 0.23; core [0.337, 0.558, 0.183, 0.388, 0.339] rim [0.293, 0.186, 0.193, 0.328, 0.084]
  - track 0 at frame 37: holes 0, rim-vs-core 0.51, rim-vs-outside 0.11, heterogeneity 0.23; core [0.307, 0.571, 0.163, 0.339, 0.368] rim [0.321, 0.155, 0.169, 0.342, 0.077]
  - track 42 at frame 55: holes 0, rim-vs-core 0.34, rim-vs-outside 0.12, heterogeneity 0.16; core [0.311, 0.501, 0.181, 0.342, 0.211] rim [0.278, 0.196, 0.189, 0.3, 0.063]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 272 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 2.75 (aggregate of 272 individuals; 46/272 membrane-like individually; rim level 0.406)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.413, rim/outside 8.42 (aggregate of 272 individuals; 2/272 membrane-like individually; rim level 0.281)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.886 (aggregate of 272 individuals; 0/272 membrane-like individually; rim level 0.18)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 2.83 (aggregate of 272 individuals; 35/272 membrane-like individually; rim level 0.432)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.349, rim/outside 13.6 (aggregate of 272 individuals; 2/272 membrane-like individually; rim level 0.161)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=4300, R_eq 4.48): none; #13 (t=3900, R_eq 4.55): none; #0 (t=3700, R_eq 5.05): ['prey a', 'product p']; #42 (t=5500, R_eq 4.22): none
- species `prey` (channels ['prey a'], own threshold): components final 46, mean 41.2, max 50; tracks 129, persistent 30; splits 9, persistent splits 5 (K=20), max generation 1, merges 7, merge/split 0.778; moving tracks 53
- species `predator` (channels ['predator b'], own threshold): components final 45, mean 31.9, max 50; tracks 114, persistent 26; splits 6, persistent splits 4 (K=20), max generation 1, merges 1, merge/split 0.167; moving tracks 51

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
