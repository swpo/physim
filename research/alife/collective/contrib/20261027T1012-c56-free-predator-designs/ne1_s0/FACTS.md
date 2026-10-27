# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 422s; status ok
- command: `python -m labkit.run c56work/world.py --out c56work/ne/p128_s0 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.24 of robust range [0.1425, 1.6569], min area 6 px

## Measurements
- components: final 49, mean 46.3, max 73; occupancy final 0.28
- tracks: 655; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 48, 29], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.00865/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 2000, default): splits 230, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 132, merge/split ratio 0.574, nucleations 66
- channel total drift (end/start - 1): [-0.083, None, -0.6111, -0.6075, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 127 at frame 71: holes 0, rim-vs-core 0.38, rim-vs-outside 0.20, heterogeneity 0.28; core [0.441, 0.441, 0.195, 0.458, 0.379] rim [0.301, 0.227, 0.229, 0.297, 0.154]
  - track 17 at frame 28: holes 0, rim-vs-core 0.48, rim-vs-outside 0.29, heterogeneity 0.08; core [0.016, 0.828, 0.312, 0.013, 0.447] rim [0.049, 0.417, 0.302, 0.036, 0.206]
  - track 250 at frame 84: holes 0, rim-vs-core 0.30, rim-vs-outside 0.19, heterogeneity 0.25; core [0.383, 0.441, 0.242, 0.412, 0.273] rim [0.306, 0.208, 0.257, 0.322, 0.12]
  - track 14 at frame 26: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.10; core [0.03, 0.865, 0.312, 0.025, 0.532] rim [0.071, 0.405, 0.302, 0.053, 0.232]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 285 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 3.01 (aggregate of 285 individuals; 76/285 membrane-like individually; rim level 0.391)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.512, rim/outside 4.93 (aggregate of 285 individuals; 17/285 membrane-like individually; rim level 0.249)
  - radial fuel F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.904 (aggregate of 285 individuals; 0/285 membrane-like individually; rim level 0.237)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 3.35 (aggregate of 285 individuals; 63/285 membrane-like individually; rim level 0.37)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.409, rim/outside 5.59 (aggregate of 285 individuals; 8/285 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #127 (t=7100, R_eq 5.11): ['prey a', 'product p']; #17 (t=2800, R_eq 3.78): none; #250 (t=8400, R_eq 4.79): ['prey a', 'product p']; #14 (t=2600, R_eq 3.83): none
- species `prey` (channels ['prey a'], own threshold): components final 43, mean 38.1, max 51; tracks 367, persistent 2; splits 110, persistent splits 9 (K=20), max generation 1, merges 68, merge/split 0.618; moving tracks 58
- species `predator` (channels ['predator b'], own threshold): components final 48, mean 42.1, max 68; tracks 307, persistent 2; splits 70, persistent splits 3 (K=20), max generation 1, merges 11, merge/split 0.157; moving tracks 72

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 285 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
