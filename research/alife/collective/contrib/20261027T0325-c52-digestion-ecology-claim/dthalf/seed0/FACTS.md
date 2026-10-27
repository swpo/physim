# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 161 frames x 500 steps x dt 0.2 = time 16000; grid [128, 128]; wall 528s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/dthalf/seed0 --seeds 0 --size 128 128 --frames 160 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1507, 1.7949], min area 6 px

## Measurements
- components: final 49, mean 42.1, max 54; occupancy final 0.21
- tracks: 128; persistent (alive >= 50% of run): 34; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 48, 41], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.00449/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 2000, default): splits 22, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 1, merges 21, merge/split ratio 0.955, nucleations 63
- channel total drift (end/start - 1): [-0.0492, None, -0.6192, -0.6023, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 83: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.25; core [0.319, 0.557, 0.177, 0.359, 0.327] rim [0.4, 0.242, 0.165, 0.439, 0.184]
  - track 14 at frame 83: holes 0, rim-vs-core 0.48, rim-vs-outside 0.14, heterogeneity 0.25; core [0.374, 0.535, 0.171, 0.425, 0.363] rim [0.334, 0.157, 0.185, 0.367, 0.074]
  - track 17 at frame 83: holes 0, rim-vs-core 0.27, rim-vs-outside 0.10, heterogeneity 0.15; core [0.337, 0.408, 0.149, 0.35, 0.136] rim [0.309, 0.164, 0.157, 0.313, 0.04]
  - track 39 at frame 113: holes 0, rim-vs-core 0.50, rim-vs-outside 0.17, heterogeneity 0.24; core [0.423, 0.535, 0.167, 0.48, 0.407] rim [0.324, 0.181, 0.186, 0.358, 0.088]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 268 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 3.51 (aggregate of 268 individuals; 44/268 membrane-like individually; rim level 0.438)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.378, rim/outside 6.89 (aggregate of 268 individuals; 6/268 membrane-like individually; rim level 0.251)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.866 (aggregate of 268 individuals; 0/268 membrane-like individually; rim level 0.182)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 3.59 (aggregate of 268 individuals; 31/268 membrane-like individually; rim level 0.463)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.313, rim/outside 12.4 (aggregate of 268 individuals; 4/268 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=8300, R_eq 4.72): ['prey a']; #14 (t=8300, R_eq 4.75): none; #17 (t=8300, R_eq 4.75): none; #39 (t=11300, R_eq 4.15): none
- species `prey` (channels ['prey a'], own threshold): components final 47, mean 42.5, max 51; tracks 135, persistent 35; splits 21, persistent splits 12 (K=20), max generation 1, merges 10, merge/split 0.476; moving tracks 63
- species `predator` (channels ['predator b'], own threshold): components final 45, mean 32.1, max 51; tracks 104, persistent 28; splits 8, persistent splits 6 (K=20), max generation 1, merges 5, merge/split 0.625; moving tracks 63

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
