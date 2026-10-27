# Evidence pack: driven-condensate-prey-predator (seed 13)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1446s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0217-c51-review-hunting/pack256 --seeds 13 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1416, 1.1685], min area 6 px

## Measurements
- components: final 44, mean 62.6, max 103; occupancy final 0.07
- tracks: 212; persistent (alive >= 50% of run): 20; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 71.00 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 46, 35], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 34, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 144
- channel total drift (end/start - 1): [-0.0665, None, -0.4991, -0.5589]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 68 at frame 78: holes 0, rim-vs-core 0.19, rim-vs-outside 0.44, heterogeneity 0.06; core [0.885, 0.0, 0.005, 0.715] rim [0.722, 0.001, 0.063, 0.639]
  - track 80 at frame 82: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.07; core [0.908, 0.002, 0.008, 0.766] rim [0.713, 0.001, 0.075, 0.652]
  - track 62 at frame 71: holes 0, rim-vs-core 0.25, rim-vs-outside 0.50, heterogeneity 0.07; core [0.927, 0.0, 0.008, 0.787] rim [0.725, 0.0, 0.074, 0.661]
  - track 187 at frame 112: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.05; core [0.007, 0.914, 0.572, 0.01] rim [0.014, 0.627, 0.57, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 353 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 5.54 (aggregate of 353 individuals; 12/353 membrane-like individually; rim level 0.455)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 7.88 (aggregate of 353 individuals; 5/353 membrane-like individually; rim level 0.364)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.66, rim/outside 0.882 (aggregate of 353 individuals; 0/353 membrane-like individually; rim level 0.362)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 6.46 (aggregate of 353 individuals; 12/353 membrane-like individually; rim level 0.442)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #68 (t=7800, R_eq 8.96): none; #80 (t=8200, R_eq 9.36): none; #62 (t=7100, R_eq 7.9): none; #187 (t=11200, R_eq 2.52): none
- species `prey` (channels ['prey a'], own threshold): components final 19, mean 35.4, max 56; tracks 268, persistent 11; splits 61, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 23
- species `predator` (channels ['predator b'], own threshold): components final 32, mean 35.2, max 58; tracks 205, persistent 0; splits 30, persistent splits 14 (K=5), max generation 2, merges 4, merge/split 0.133; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 353 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
