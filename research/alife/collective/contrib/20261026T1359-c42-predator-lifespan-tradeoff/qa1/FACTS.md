# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 178s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa1 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0573, 1.2048], min area 6 px

## Measurements
- components: final 25, mean 29.2, max 70; occupancy final 0.34
- tracks: 213; persistent (alive >= 50% of run): 25; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 6.55 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 2000, default): splits 24, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 56, merge/split ratio 2.33, nucleations 10
- channel total drift (end/start - 1): [-0.7876, 7.2874, -0.2725, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.26, rim-vs-outside 0.51, heterogeneity 0.05; core [0.001, 0.973, 0.646, 0.021] rim [0.013, 0.717, 0.644, 0.02]
  - track 80 at frame 61: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.05; core [0.004, 0.926, 0.649, 0.011] rim [0.019, 0.609, 0.648, 0.011]
  - track 113 at frame 62: holes 0, rim-vs-core 0.35, rim-vs-outside 0.28, heterogeneity 0.05; core [0.004, 0.924, 0.647, 0.018] rim [0.02, 0.574, 0.646, 0.017]
  - track 182 at frame 67: holes 0, rim-vs-core 0.28, rim-vs-outside 0.46, heterogeneity 0.05; core [0.002, 0.952, 0.652, 0.016] rim [0.015, 0.668, 0.651, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 3.19, rim/outside 0.87 (aggregate of 160 individuals; 1/160 membrane-like individually; rim level 0.0517)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.79 (aggregate of 160 individuals; 6/160 membrane-like individually; rim level 0.694)
  - radial fuel u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 1.01 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.638)
  - radial waste w: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 1 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.0329)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6100, R_eq 6.1): none; #80 (t=6100, R_eq 4.18): none; #113 (t=6200, R_eq 5.61): none; #182 (t=6700, R_eq 7.76): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 3.6, max 59; tracks 151, persistent 0; splits 19, persistent splits 0 (K=20), max generation 0, merges 14, merge/split 0.737; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 24, mean 26.6, max 38; tracks 90, persistent 25; splits 8, persistent splits 0 (K=20), max generation 0, merges 27, merge/split 3.38; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 160 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
