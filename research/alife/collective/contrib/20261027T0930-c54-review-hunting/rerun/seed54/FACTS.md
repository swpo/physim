# Evidence pack: driven-condensate-prey-predator (seed 54)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1985s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0930-c54-review-hunting/rerun/seed54 --seeds 54 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.143, 1.1919], min area 6 px

## Measurements
- components: final 68, mean 74.5, max 126; occupancy final 0.05
- tracks: 291; persistent (alive >= 50% of run): 18; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 53.44 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [86, 69, 50], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 47, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 193
- channel total drift (end/start - 1): [-0.0872, None, -0.4933, -0.5614]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 40: holes 0, rim-vs-core 0.36, rim-vs-outside 0.26, heterogeneity 0.05; core [0.005, 0.9, 0.493, 0.003] rim [0.021, 0.541, 0.488, 0.015]
  - track 45 at frame 45: holes 0, rim-vs-core 0.36, rim-vs-outside 0.26, heterogeneity 0.05; core [0.01, 0.874, 0.504, 0.008] rim [0.024, 0.515, 0.499, 0.019]
  - track 89 at frame 77: holes 0, rim-vs-core 0.34, rim-vs-outside 0.31, heterogeneity 0.05; core [0.014, 0.932, 0.487, 0.013] rim [0.029, 0.595, 0.483, 0.024]
  - track 245 at frame 113: holes 0, rim-vs-core 0.22, rim-vs-outside 0.24, heterogeneity 0.04; core [0.006, 0.778, 0.547, 0.006] rim [0.017, 0.555, 0.543, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 429 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 4.17 (aggregate of 429 individuals; 22/429 membrane-like individually; rim level 0.354)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 9.47 (aggregate of 429 individuals; 3/429 membrane-like individually; rim level 0.464)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.919 (aggregate of 429 individuals; 0/429 membrane-like individually; rim level 0.385)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 4.83 (aggregate of 429 individuals; 24/429 membrane-like individually; rim level 0.355)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=4000, R_eq 3.39): none; #45 (t=4500, R_eq 3.24): none; #89 (t=7700, R_eq 2.88): none; #245 (t=11300, R_eq 3.43): none
- species `prey` (channels ['prey a'], own threshold): components final 27, mean 31.1, max 65; tracks 350, persistent 2; splits 75, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 14
- species `predator` (channels ['predator b'], own threshold): components final 48, mean 52.2, max 81; tracks 280, persistent 0; splits 43, persistent splits 22 (K=5), max generation 2, merges 7, merge/split 0.163; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 429 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
