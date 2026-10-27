# Evidence pack: driven-condensate-prey-predator (seed 11)

- world: `../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1821s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out c56work/rv/pack256 --seeds 11 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1411, 1.1686], min area 6 px

## Measurements
- components: final 54, mean 64.7, max 114; occupancy final 0.07
- tracks: 239; persistent (alive >= 50% of run): 15; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 51.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 54, 34], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 38, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.079, nucleations 159
- channel total drift (end/start - 1): [-0.0524, None, -0.5057, -0.5506]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 80: holes 0, rim-vs-core 0.21, rim-vs-outside 0.48, heterogeneity 0.07; core [0.905, 0.002, 0.006, 0.751] rim [0.729, 0.001, 0.076, 0.669]
  - track 68 at frame 78: holes 0, rim-vs-core 0.19, rim-vs-outside 0.48, heterogeneity 0.06; core [0.885, 0.001, 0.005, 0.718] rim [0.72, 0.0, 0.076, 0.656]
  - track 92 at frame 83: holes 0, rim-vs-core 0.36, rim-vs-outside 0.36, heterogeneity 0.07; core [0.007, 0.97, 0.525, 0.009] rim [0.035, 0.613, 0.514, 0.036]
  - track 224 at frame 117: holes 0, rim-vs-core 0.20, rim-vs-outside 0.21, heterogeneity 0.03; core [0.031, 0.747, 0.548, 0.031] rim [0.036, 0.543, 0.547, 0.036]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 358 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 5.41 (aggregate of 358 individuals; 9/358 membrane-like individually; rim level 0.456)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 8.8 (aggregate of 358 individuals; 2/358 membrane-like individually; rim level 0.375)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.59, rim/outside 0.881 (aggregate of 358 individuals; 0/358 membrane-like individually; rim level 0.365)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 6.31 (aggregate of 358 individuals; 9/358 membrane-like individually; rim level 0.445)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #67 (t=8000, R_eq 8.72): none; #68 (t=7800, R_eq 9.1): none; #92 (t=8300, R_eq 5.01): none; #224 (t=11700, R_eq 2.11): none
- species `prey` (channels ['prey a'], own threshold): components final 25, mean 35.0, max 67; tracks 321, persistent 10; splits 79, persistent splits 2 (K=5), max generation 1, merges 1, merge/split 0.013; moving tracks 25
- species `predator` (channels ['predator b'], own threshold): components final 35, mean 38.4, max 57; tracks 221, persistent 0; splits 34, persistent splits 23 (K=5), max generation 2, merges 6, merge/split 0.176; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 358 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
