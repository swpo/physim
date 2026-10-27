# Evidence pack: driven-condensate-prey-predator (seed 14)

- world: `../../20261026T2024-c46-hunting-predators-divide-256/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1559s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2024-c46-hunting-predators-divide-256/world.py --out collective/contrib/20261027T0430-c51-review-predators-divide/pack256_s14 --seeds 14 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1422, 1.1732], min area 6 px

## Measurements
- components: final 50, mean 67.5, max 114; occupancy final 0.06
- tracks: 243; persistent (alive >= 50% of run): 23; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 34.77 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 55, 39], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 37, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 169
- channel total drift (end/start - 1): [-0.0766, None, -0.4972, -0.5635]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 55 at frame 74: holes 0, rim-vs-core 0.19, rim-vs-outside 0.46, heterogeneity 0.07; core [0.871, 0.001, 0.005, 0.705] rim [0.703, 0.001, 0.072, 0.635]
  - track 85 at frame 81: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.07; core [0.934, 0.004, 0.006, 0.797] rim [0.726, 0.001, 0.064, 0.652]
  - track 99 at frame 83: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.07; core [0.958, 0.0, 0.007, 0.839] rim [0.732, 0.0, 0.074, 0.673]
  - track 192 at frame 107: holes 0, rim-vs-core 0.12, rim-vs-outside 0.37, heterogeneity 0.05; core [0.014, 0.824, 0.514, 0.011] rim [0.018, 0.699, 0.515, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 396 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 4.65 (aggregate of 396 individuals; 8/396 membrane-like individually; rim level 0.401)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 8.86 (aggregate of 396 individuals; 4/396 membrane-like individually; rim level 0.422)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.905 (aggregate of 396 individuals; 0/396 membrane-like individually; rim level 0.384)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 5.27 (aggregate of 396 individuals; 10/396 membrane-like individually; rim level 0.397)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #55 (t=7400, R_eq 9.92): none; #85 (t=8100, R_eq 8.25): none; #99 (t=8300, R_eq 6.86): none; #192 (t=10700, R_eq 2.76): none
- species `prey` (channels ['prey a'], own threshold): components final 19, mean 33.2, max 58; tracks 314, persistent 6; splits 69, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 13
- species `predator` (channels ['predator b'], own threshold): components final 33, mean 42.7, max 68; tracks 233, persistent 0; splits 35, persistent splits 20 (K=5), max generation 3, merges 4, merge/split 0.114; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 396 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
