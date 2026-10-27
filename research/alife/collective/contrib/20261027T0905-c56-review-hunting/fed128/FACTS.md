# Evidence pack: driven-condensate-prey-predator (seed 11)

- world: `../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out c56work/rv/fed128 --seeds 11 --size 128 128 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1421, 1.1864], min area 6 px

## Measurements
- components: final 18, mean 17.0, max 31; occupancy final 0.09
- tracks: 36; persistent (alive >= 50% of run): 14; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 36.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 18, 14], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 34
- channel total drift (end/start - 1): [-0.1081, None, -0.4821, -0.5808]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 35: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.05; core [0.0, 0.942, 0.555, 0.0] rim [0.007, 0.622, 0.55, 0.008]
  - track 0 at frame 31: holes 0, rim-vs-core 0.26, rim-vs-outside 0.22, heterogeneity 0.04; core [0.001, 0.809, 0.543, 0.001] rim [0.008, 0.546, 0.537, 0.007]
  - track 10 at frame 40: holes 0, rim-vs-core 0.34, rim-vs-outside 0.24, heterogeneity 0.05; core [0.0, 0.88, 0.55, 0.0] rim [0.007, 0.54, 0.542, 0.006]
  - track 6 at frame 34: holes 0, rim-vs-core 0.32, rim-vs-outside 0.27, heterogeneity 0.05; core [0.0, 0.899, 0.545, 0.001] rim [0.008, 0.58, 0.54, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 106 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.34 (aggregate of 106 individuals; 3/106 membrane-like individually; rim level 0.379)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 11 (aggregate of 106 individuals; 1/106 membrane-like individually; rim level 0.45)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.919 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.377)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 4.96 (aggregate of 106 individuals; 4/106 membrane-like individually; rim level 0.378)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3500, R_eq 3.48): none; #0 (t=3100, R_eq 4.72): none; #10 (t=4000, R_eq 4.37): none; #6 (t=3400, R_eq 3.7): none
- species `prey` (channels ['prey a'], own threshold): components final 8, mean 9.5, max 17; tracks 52, persistent 2; splits 8, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 14, mean 9.7, max 17; tracks 32, persistent 3; splits 1, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
