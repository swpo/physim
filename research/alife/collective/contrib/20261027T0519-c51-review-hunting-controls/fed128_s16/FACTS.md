# Evidence pack: driven-condensate-prey-predator (seed 16)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 235s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0519-c51-review-hunting-controls/fed128_s16 --seeds 16 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1435, 1.1517], min area 6 px

## Measurements
- components: final 15, mean 15.6, max 28; occupancy final 0.10
- tracks: 39; persistent (alive >= 50% of run): 13; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 17, 11], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 31
- channel total drift (end/start - 1): [-0.0721, None, -0.4907, -0.5622]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 35: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.05; core [0.0, 0.94, 0.53, 0.0] rim [0.007, 0.646, 0.524, 0.006]
  - track 7 at frame 36: holes 0, rim-vs-core 0.22, rim-vs-outside 0.36, heterogeneity 0.05; core [0.002, 0.883, 0.52, 0.001] rim [0.007, 0.665, 0.519, 0.005]
  - track 5 at frame 35: holes 0, rim-vs-core 0.31, rim-vs-outside 0.26, heterogeneity 0.05; core [0.001, 0.893, 0.521, 0.001] rim [0.008, 0.585, 0.515, 0.006]
  - track 8 at frame 36: holes 0, rim-vs-core 0.34, rim-vs-outside 0.26, heterogeneity 0.05; core [0.001, 0.915, 0.514, 0.001] rim [0.011, 0.579, 0.509, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 4.52 (aggregate of 96 individuals; 2/96 membrane-like individually; rim level 0.417)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 11 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.419)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.903 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.366)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 5.09 (aggregate of 96 individuals; 2/96 membrane-like individually; rim level 0.412)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3500, R_eq 3.91): none; #7 (t=3600, R_eq 4.11): none; #5 (t=3500, R_eq 3.78): none; #8 (t=3600, R_eq 3.57): none
- species `prey` (channels ['prey a'], own threshold): components final 8, mean 9.2, max 15; tracks 55, persistent 2; splits 12, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 8, mean 8.6, max 16; tracks 35, persistent 5; splits 3, persistent splits 0 (K=5), max generation 0, merges 2, merge/split 0.667; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
