# Evidence pack: condensate-food-chain (seed 3)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 177s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/more/seed3 --seeds 3 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0375, 1.3566], min area 6 px

## Measurements
- components: final 27, mean 36.0, max 63; occupancy final 0.24
- tracks: 475; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.72, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 29, 18], H1 [4, 2, 1]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00438/time; max body lengths 1.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 147, persistent splits 61 (0 more failed only because the siblings re-merged within K), max generation 4, merges 49, merge/split ratio 0.333, nucleations 76
- channel total drift (end/start - 1): [-0.2516, 1.9701, -0.4823, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 85 at frame 19: holes 0, rim-vs-core 0.18, rim-vs-outside 0.29, heterogeneity 0.06; core [0.004, 0.834, 0.667, 0.172] rim [0.011, 0.656, 0.631, 0.208]
  - track 156 at frame 33: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.04; core [0.006, 0.822, 0.735, 0.131] rim [0.02, 0.56, 0.73, 0.132]
  - track 216 at frame 51: holes 0, rim-vs-core 0.16, rim-vs-outside 0.26, heterogeneity 0.04; core [0.006, 0.796, 0.653, 0.229] rim [0.013, 0.641, 0.655, 0.225]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 170 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 2.81 (aggregate of 170 individuals; 17/170 membrane-like individually; rim level 0.218)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.28 (aggregate of 170 individuals; 24/170 membrane-like individually; rim level 0.505)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 0.96 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.54)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 1.27 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.376)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #85 (t=1900, R_eq 4.85): none; #156 (t=3300, R_eq 5.11): none; #216 (t=5100, R_eq 3.52): none; #282 (t=6500, R_eq 2.52): none
- species `prey` (channels ['prey a'], own threshold): components final 13, mean 12.8, max 52; tracks 290, persistent 0; splits 75, persistent splits 12 (K=5), max generation 1, merges 2, merge/split 0.027; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 21, mean 26.8, max 37; tracks 357, persistent 0; splits 91, persistent splits 35 (K=5), max generation 2, merges 30, merge/split 0.33; moving tracks 10

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 170 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
