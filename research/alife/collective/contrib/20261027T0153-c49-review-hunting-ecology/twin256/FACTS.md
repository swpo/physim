# Evidence pack: driven-condensate-prey-predator (seed 9)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1545s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c49rev4/twin256 --seeds 9 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1168, 0.8794], min area 6 px

## Measurements
- components: final 85, mean 63.5, max 85; occupancy final 0.15
- tracks: 106; persistent (alive >= 50% of run): 64; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 34.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [95, 88, 85], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00111/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 21, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 64
- channel total drift (end/start - 1): [0.0, None, -0.556, -0.5154]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.55, heterogeneity 0.07; core [0.944, 0.0, 0.023, 0.876] rim [0.728, 0.0, 0.103, 0.709]
  - track 3 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.54, heterogeneity 0.08; core [0.926, 0.0, 0.024, 0.851] rim [0.705, 0.0, 0.101, 0.678]
  - track 7 at frame 62: holes 0, rim-vs-core 0.26, rim-vs-outside 0.54, heterogeneity 0.07; core [0.917, 0.0, 0.017, 0.819] rim [0.713, 0.0, 0.107, 0.693]
  - track 64 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.08; core [0.927, 0.0, 0.064, 0.93] rim [0.654, 0.0, 0.137, 0.662]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 415 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 17.8 (aggregate of 415 individuals; 0/415 membrane-like individually; rim level 0.819)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 415 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.55, rim/outside 0.664 (aggregate of 415 individuals; 0/415 membrane-like individually; rim level 0.231)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 18.4 (aggregate of 415 individuals; 0/415 membrane-like individually; rim level 0.792)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 6.51): none; #3 (t=6200, R_eq 7.48): none; #7 (t=6200, R_eq 7.33): none; #64 (t=10100, R_eq 5.29): none
- species `prey` (channels ['prey a'], own threshold): components final 85, mean 64.5, max 85; tracks 108, persistent 64; splits 21, persistent splits 21 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
