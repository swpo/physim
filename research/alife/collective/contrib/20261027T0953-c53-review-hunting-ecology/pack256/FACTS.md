# Evidence pack: driven-condensate-prey-predator (seed 8)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1983s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c53-rev-hc/pack256 --seeds 8 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1418, 1.1923], min area 6 px

## Measurements
- components: final 56, mean 72.9, max 119; occupancy final 0.04
- tracks: 260; persistent (alive >= 50% of run): 27; longest 113 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 81.89 (1 = constant size)
- enclosures: components with a hole mean 0.88, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [72, 59, 30], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 36, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 185
- channel total drift (end/start - 1): [-0.0992, None, -0.4929, -0.5683]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 57 at frame 65: holes 1, rim-vs-core 0.17, rim-vs-outside 0.61, heterogeneity 0.07; core [0.911, 0.001, 0.0, 0.739] rim [0.773, 0.001, 0.024, 0.644]
  - track 7 at frame 44: holes 0, rim-vs-core 0.35, rim-vs-outside 0.28, heterogeneity 0.06; core [0.006, 0.911, 0.532, 0.007] rim [0.021, 0.561, 0.528, 0.019]
  - track 28 at frame 44: holes 0, rim-vs-core 0.36, rim-vs-outside 0.25, heterogeneity 0.05; core [0.011, 0.896, 0.48, 0.007] rim [0.026, 0.538, 0.476, 0.018]
  - track 153 at frame 80: holes 0, rim-vs-core 0.31, rim-vs-outside 0.25, heterogeneity 0.05; core [0.032, 0.822, 0.503, 0.029] rim [0.041, 0.513, 0.501, 0.037]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 410 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 4.25 (aggregate of 410 individuals; 18/410 membrane-like individually; rim level 0.365)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 9.21 (aggregate of 410 individuals; 7/410 membrane-like individually; rim level 0.458)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.92 (aggregate of 410 individuals; 0/410 membrane-like individually; rim level 0.392)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 4.85 (aggregate of 410 individuals; 17/410 membrane-like individually; rim level 0.361)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #57 (t=6500, R_eq 11.71, ring): ['prey a', 'product p']; #7 (t=4400, R_eq 3.24): none; #28 (t=4400, R_eq 3.09): none; #153 (t=8000, R_eq 2.46): none
- species `prey` (channels ['prey a'], own threshold): components final 24, mean 31.6, max 69; tracks 319, persistent 3; splits 64, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 19
- species `predator` (channels ['predator b'], own threshold): components final 40, mean 50.0, max 82; tracks 248, persistent 2; splits 36, persistent splits 17 (K=5), max generation 2, merges 3, merge/split 0.083; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 410 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
