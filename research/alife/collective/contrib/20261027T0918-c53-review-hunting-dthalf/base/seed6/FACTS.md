# Evidence pack: driven-condensate-prey-predator (seed 6)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 399s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c53-rev-hd/base --seeds 4 6 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1358, 1.169], min area 6 px

## Measurements
- components: final 9, mean 15.8, max 28; occupancy final 0.06
- tracks: 50; persistent (alive >= 50% of run): 2; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 33.60 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 5], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 34
- channel total drift (end/start - 1): [-0.1184, None, -0.4764, -0.579]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 86: holes 0, rim-vs-core 0.26, rim-vs-outside 0.51, heterogeneity 0.08; core [0.939, 0.0, 0.013, 0.849] rim [0.734, 0.0, 0.087, 0.703]
  - track 25 at frame 87: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.08; core [0.947, 0.0, 0.015, 0.864] rim [0.719, 0.0, 0.096, 0.695]
  - track 2 at frame 33: holes 0, rim-vs-core 0.33, rim-vs-outside 0.25, heterogeneity 0.05; core [0.001, 0.903, 0.549, 0.001] rim [0.009, 0.572, 0.543, 0.007]
  - track 38 at frame 104: holes 0, rim-vs-core 0.30, rim-vs-outside 0.27, heterogeneity 0.05; core [0.008, 0.909, 0.544, 0.009] rim [0.018, 0.608, 0.541, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 6.17 (aggregate of 88 individuals; 7/88 membrane-like individually; rim level 0.494)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 7.93 (aggregate of 88 individuals; 2/88 membrane-like individually; rim level 0.327)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.67, rim/outside 0.854 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.347)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 7.34 (aggregate of 88 individuals; 7/88 membrane-like individually; rim level 0.49)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=8600, R_eq 7.53): none; #25 (t=8700, R_eq 7.31): none; #2 (t=3300, R_eq 4.18): none; #38 (t=10400, R_eq 2.82): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 9.3, max 21; tracks 70, persistent 2; splits 17, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 8, mean 8.5, max 15; tracks 48, persistent 0; splits 7, persistent splits 5 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
