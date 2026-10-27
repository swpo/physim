# Evidence pack: driven-condensate-prey-predator (seed 71)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 76 frames x 500 steps x dt 0.2 = time 7500; grid [128, 128]; wall 264s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c57-w11/efork128 --seeds 71 --frames 75 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1442, 1.1801], min area 6 px

## Measurements
- components: final 9, mean 14.4, max 29; occupancy final 0.03
- tracks: 37; persistent (alive >= 50% of run): 13; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.67 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 31
- channel total drift (end/start - 1): [-0.0544, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 39: holes 0, rim-vs-core 0.30, rim-vs-outside 0.26, heterogeneity 0.05; core [0.001, 0.882, 0.618, 0.07] rim [0.008, 0.587, 0.616, 0.079]
  - track 2 at frame 39: holes 0, rim-vs-core 0.30, rim-vs-outside 0.28, heterogeneity 0.05; core [0.0, 0.914, 0.615, 0.066] rim [0.006, 0.61, 0.612, 0.076]
  - track 4 at frame 41: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.05; core [0.0, 0.937, 0.621, 0.068] rim [0.007, 0.599, 0.617, 0.078]
  - track 5 at frame 41: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.05; core [0.001, 0.944, 0.595, 0.069] rim [0.01, 0.619, 0.591, 0.078]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 2.55 (aggregate of 85 individuals; 2/85 membrane-like individually; rim level 0.273)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 13.8 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.577)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.98 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.393)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 2.36 (aggregate of 85 individuals; 2/85 membrane-like individually; rim level 0.272)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3900, R_eq 3.29): none; #2 (t=3900, R_eq 3.29): none; #4 (t=4100, R_eq 3.19): none; #5 (t=4100, R_eq 2.93): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 7.5, max 16; tracks 42, persistent 0; splits 4, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 9, mean 9.1, max 17; tracks 24, persistent 8; splits 3, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
