# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 400 steps x dt 0.25 (--dt; world META dt 0.5) = time 12000; grid [128, 128]; wall 347s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/dthalf/seed0 --seeds 0 --size 128 128 --frames 120 --spf 400 --dt 0.25 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0434, 1.3612], min area 6 px

## Measurements
- components: final 27, mean 35.4, max 72; occupancy final 0.20
- tracks: 493; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.24, final 2; holes at thresholds 0.2/0.35/0.5 final [3, 2, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 27, 15], H1 [4, 3, 1]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00288/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 146, persistent splits 68 (0 more failed only because the siblings re-merged within K), max generation 5, merges 41, merge/split ratio 0.281, nucleations 81
- channel total drift (end/start - 1): [-0.5143, 3.4272, -0.3396, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 98 at frame 19: holes 0, rim-vs-core 0.25, rim-vs-outside 0.25, heterogeneity 0.04; core [0.004, 0.841, 0.724, 0.098] rim [0.016, 0.594, 0.718, 0.099]
  - track 80 at frame 18: holes 0, rim-vs-core 0.16, rim-vs-outside 0.43, heterogeneity 0.05; core [0.002, 0.864, 0.694, 0.092] rim [0.009, 0.704, 0.679, 0.101]
  - track 115 at frame 18: holes 0, rim-vs-core 0.15, rim-vs-outside 0.42, heterogeneity 0.04; core [0.002, 0.839, 0.694, 0.046] rim [0.01, 0.693, 0.691, 0.043]
  - track 334 at frame 79: holes 0, rim-vs-core 0.18, rim-vs-outside 0.33, heterogeneity 0.04; core [0.004, 0.871, 0.677, 0.2] rim [0.013, 0.689, 0.683, 0.189]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 180 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 2.69 (aggregate of 180 individuals; 24/180 membrane-like individually; rim level 0.198)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 5.06 (aggregate of 180 individuals; 26/180 membrane-like individually; rim level 0.531)
  - radial fuel u: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.957 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.54)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 1.25 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.374)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #98 (t=1900, R_eq 5.29): none; #80 (t=1800, R_eq 6.21): none; #115 (t=1800, R_eq 6.31): none; #334 (t=7900, R_eq 3.24): none
- species `prey` (channels ['prey a'], own threshold): components final 6, mean 10.8, max 64; tracks 315, persistent 0; splits 67, persistent splits 3 (K=5), max generation 2, merges 17, merge/split 0.254; moving tracks 7
- species `predator` (channels ['predator b'], own threshold): components final 24, mean 28.4, max 45; tracks 387, persistent 0; splits 95, persistent splits 36 (K=5), max generation 3, merges 31, merge/split 0.326; moving tracks 19

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.25 only relabels time (world META dt 0.5): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 42 of 180 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
