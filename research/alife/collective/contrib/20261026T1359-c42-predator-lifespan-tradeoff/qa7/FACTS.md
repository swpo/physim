# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 181s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa7 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0599, 1.2442], min area 6 px

## Measurements
- components: final 58, mean 52.7, max 72; occupancy final 0.23
- tracks: 268; persistent (alive >= 50% of run): 45; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 13.12 (1 = constant size)
- enclosures: components with a hole mean 1.73, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 59, 58], H1 [3, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 51, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 57, merge/split ratio 1.12, nucleations 21
- channel total drift (end/start - 1): [-0.776, 5.4726, -0.2226, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 55 at frame 61: holes 0, rim-vs-core 0.17, rim-vs-outside 0.37, heterogeneity 0.04; core [0.002, 0.915, 0.732, 0.017] rim [0.007, 0.741, 0.732, 0.016]
  - track 64 at frame 61: holes 0, rim-vs-core 0.28, rim-vs-outside 0.27, heterogeneity 0.04; core [0.002, 0.916, 0.728, 0.029] rim [0.011, 0.639, 0.727, 0.027]
  - track 83 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.28, heterogeneity 0.04; core [0.002, 0.91, 0.732, 0.048] rim [0.012, 0.617, 0.731, 0.046]
  - track 216 at frame 82: holes 0, rim-vs-core 0.21, rim-vs-outside 0.37, heterogeneity 0.04; core [0.002, 0.915, 0.709, 0.048] rim [0.009, 0.708, 0.709, 0.045]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 312 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.98, rim/outside 0.615 (aggregate of 312 individuals; 2/312 membrane-like individually; rim level 0.0374)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 7.29 (aggregate of 312 individuals; 25/312 membrane-like individually; rim level 0.763)
  - radial fuel u: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 312 individuals; 0/312 membrane-like individually; rim level 0.702)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 1.07 (aggregate of 312 individuals; 0/312 membrane-like individually; rim level 0.0549)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #55 (t=6100, R_eq 3.95): none; #64 (t=6100, R_eq 3.99): none; #83 (t=6200, R_eq 4.33): none; #216 (t=8200, R_eq 3.99): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 3.8, max 61; tracks 165, persistent 0; splits 20, persistent splits 0 (K=20), max generation 0, merges 14, merge/split 0.7; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 58, mean 49.5, max 58; tracks 150, persistent 43; splits 40, persistent splits 15 (K=20), max generation 3, merges 22, merge/split 0.55; moving tracks 5

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 32 of 312 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
