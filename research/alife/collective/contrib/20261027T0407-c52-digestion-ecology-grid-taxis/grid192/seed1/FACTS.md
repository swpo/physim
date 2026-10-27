# Evidence pack: digestion-driven-predators (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [192, 192]; wall 972s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/grid192/seed1 --seeds 1 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1517, 1.81], min area 6 px

## Measurements
- components: final 48, mean 43.8, max 52; occupancy final 0.20
- tracks: 157; persistent (alive >= 50% of run): 28; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 33.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 50, 42], H1 [0, 0, 0]
- motion: 80 long-lived tracks moved >= 1 body length; max speed 0.0119/time; max body lengths 7.4
- replication (lineage window K = 20 frames = time 2000, default): splits 20, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 31, merge/split ratio 1.55, nucleations 87
- channel total drift (end/start - 1): [-0.0541, None, -0.6056, -0.5934, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 62: holes 0, rim-vs-core 0.21, rim-vs-outside 0.44, heterogeneity 0.25; core [0.477, 0.456, 0.166, 0.541, 0.344] rim [0.351, 0.389, 0.183, 0.399, 0.275]
  - track 20 at frame 59: holes 0, rim-vs-core 0.50, rim-vs-outside 0.23, heterogeneity 0.26; core [0.447, 0.563, 0.158, 0.51, 0.436] rim [0.337, 0.219, 0.182, 0.376, 0.112]
  - track 8 at frame 56: holes 0, rim-vs-core 0.41, rim-vs-outside 0.20, heterogeneity 0.21; core [0.337, 0.575, 0.158, 0.36, 0.292] rim [0.322, 0.222, 0.164, 0.334, 0.09]
  - track 84 at frame 92: holes 0, rim-vs-core 0.55, rim-vs-outside 0.22, heterogeneity 0.26; core [0.539, 0.488, 0.103, 0.576, 0.478] rim [0.391, 0.162, 0.137, 0.406, 0.106]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 276 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 3.86 (aggregate of 276 individuals; 16/276 membrane-like individually; rim level 0.456)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 6.2 (aggregate of 276 individuals; 2/276 membrane-like individually; rim level 0.24)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.849 (aggregate of 276 individuals; 0/276 membrane-like individually; rim level 0.173)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 3.95 (aggregate of 276 individuals; 9/276 membrane-like individually; rim level 0.473)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.308, rim/outside 12.7 (aggregate of 276 individuals; 3/276 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=6200, R_eq 6.15): none; #20 (t=5900, R_eq 6.56): none; #8 (t=5600, R_eq 7.07): none; #84 (t=9200, R_eq 7.02): none
- species `prey` (channels ['prey a'], own threshold): components final 47, mean 43.7, max 51; tracks 167, persistent 32; splits 26, persistent splits 6 (K=20), max generation 1, merges 12, merge/split 0.462; moving tracks 79
- species `predator` (channels ['predator b'], own threshold): components final 50, mean 36.4, max 50; tracks 129, persistent 29; splits 10, persistent splits 3 (K=20), max generation 1, merges 8, merge/split 0.8; moving tracks 74

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
