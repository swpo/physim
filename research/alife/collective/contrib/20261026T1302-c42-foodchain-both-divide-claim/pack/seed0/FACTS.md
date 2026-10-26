# Evidence pack: condensate-food-chain (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 187s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/pack/seed0 --seeds 0 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0418, 1.3631], min area 6 px

## Measurements
- components: final 26, mean 34.6, max 73; occupancy final 0.23
- tracks: 484; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.13, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 27, 18], H1 [1, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00298/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 147, persistent splits 55 (0 more failed only because the siblings re-merged within K), max generation 5, merges 39, merge/split ratio 0.265, nucleations 74
- channel total drift (end/start - 1): [-0.4769, 3.4917, -0.3785, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 19: holes 0, rim-vs-core 0.25, rim-vs-outside 0.25, heterogeneity 0.04; core [0.004, 0.844, 0.724, 0.088] rim [0.016, 0.596, 0.718, 0.088]
  - track 116 at frame 19: holes 0, rim-vs-core 0.21, rim-vs-outside 0.25, heterogeneity 0.04; core [0.004, 0.822, 0.712, 0.027] rim [0.014, 0.609, 0.708, 0.026]
  - track 80 at frame 18: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.04; core [0.004, 0.847, 0.739, 0.044] rim [0.018, 0.585, 0.735, 0.044]
  - track 360 at frame 89: holes 0, rim-vs-core 0.25, rim-vs-outside 0.25, heterogeneity 0.06; core [0.003, 0.843, 0.644, 0.199] rim [0.014, 0.591, 0.636, 0.203]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 177 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 3.32 (aggregate of 177 individuals; 19/177 membrane-like individually; rim level 0.233)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 4.43 (aggregate of 177 individuals; 22/177 membrane-like individually; rim level 0.488)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.954 (aggregate of 177 individuals; 0/177 membrane-like individually; rim level 0.537)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 1.33 (aggregate of 177 individuals; 0/177 membrane-like individually; rim level 0.388)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=1900, R_eq 5.23): none; #116 (t=1900, R_eq 5.97): none; #80 (t=1800, R_eq 5.11): none; #360 (t=8900, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 7, mean 10.9, max 62; tracks 308, persistent 0; splits 68, persistent splits 9 (K=5), max generation 2, merges 18, merge/split 0.265; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 22, mean 27.5, max 45; tracks 366, persistent 0; splits 92, persistent splits 30 (K=5), max generation 2, merges 23, merge/split 0.25; moving tracks 18

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 33 of 177 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
