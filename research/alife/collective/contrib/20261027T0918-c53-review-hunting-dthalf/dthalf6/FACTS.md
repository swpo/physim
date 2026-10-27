# Evidence pack: driven-condensate-prey-predator (seed 6)

- world: `../../20261026T2119-c46-hunting-ecology-dthalf/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [128, 128]; wall 876s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2119-c46-hunting-ecology-dthalf/world.py --out collective/contrib/c53-rev-hd/dthalf6 --seeds 6 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1358, 1.1639], min area 6 px

## Measurements
- components: final 11, mean 15.7, max 28; occupancy final 0.06
- tracks: 50; persistent (alive >= 50% of run): 2; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.12 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 5], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 34
- channel total drift (end/start - 1): [-0.1185, None, -0.4766, -0.579]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 86: holes 0, rim-vs-core 0.27, rim-vs-outside 0.51, heterogeneity 0.08; core [0.938, 0.0, 0.013, 0.848] rim [0.731, 0.0, 0.088, 0.7]
  - track 25 at frame 87: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.08; core [0.946, 0.0, 0.015, 0.862] rim [0.724, 0.0, 0.093, 0.698]
  - track 32 at frame 91: holes 0, rim-vs-core 0.30, rim-vs-outside 0.27, heterogeneity 0.18; core [0.78, 0.192, 0.099, 0.825] rim [0.617, 0.019, 0.171, 0.657]
  - track 36 at frame 105: holes 0, rim-vs-core 0.29, rim-vs-outside 0.26, heterogeneity 0.04; core [0.007, 0.904, 0.543, 0.008] rim [0.017, 0.614, 0.54, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 5.85 (aggregate of 90 individuals; 5/90 membrane-like individually; rim level 0.479)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 7.97 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.345)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.62, rim/outside 0.857 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.349)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 6.85 (aggregate of 90 individuals; 6/90 membrane-like individually; rim level 0.474)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=8600, R_eq 7.55): none; #25 (t=8700, R_eq 7.31): none; #32 (t=9100, R_eq 5.92): none; #36 (t=10500, R_eq 2.82): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 9.3, max 21; tracks 75, persistent 2; splits 20, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 7, mean 8.5, max 15; tracks 46, persistent 0; splits 6, persistent splits 6 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
