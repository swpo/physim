# Evidence pack: condensate-food-chain (seed 3)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 613s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/pack256 --seeds 3 --frames 100 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0371, 1.339], min area 6 px

## Measurements
- components: final 124, mean 143.8, max 268; occupancy final 0.22
- tracks: 1610; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.43, final 9; holes at thresholds 0.2/0.35/0.5 final [11, 9, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [164, 124, 51], H1 [20, 9, 2]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.00619/time; max body lengths 2.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 462, persistent splits 182 (0 more failed only because the siblings re-merged within K), max generation 6, merges 154, merge/split ratio 0.333, nucleations 251
- channel total drift (end/start - 1): [-0.433, 3.228, -0.3774, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 232 at frame 25: holes 0, rim-vs-core 0.22, rim-vs-outside 0.52, heterogeneity 0.06; core [0.0, 0.94, 0.59, 0.22] rim [0.015, 0.718, 0.588, 0.215]
  - track 517 at frame 30: holes 0, rim-vs-core 0.27, rim-vs-outside 0.52, heterogeneity 0.09; core [0.88, 0.05, 0.034, 0.824] rim [0.659, 0.033, 0.143, 0.711]
  - track 461 at frame 24: holes 0, rim-vs-core 0.25, rim-vs-outside 0.53, heterogeneity 0.08; core [0.871, 0.02, 0.029, 0.857] rim [0.676, 0.022, 0.138, 0.738]
  - track 1242 at frame 77: holes 0, rim-vs-core 0.20, rim-vs-outside 0.25, heterogeneity 0.04; core [0.002, 0.822, 0.481, 0.548] rim [0.008, 0.625, 0.475, 0.552]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 751 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 3.29 (aggregate of 751 individuals; 67/751 membrane-like individually; rim level 0.249)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 4.91 (aggregate of 751 individuals; 106/751 membrane-like individually; rim level 0.493)
  - radial fuel u: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.951 (aggregate of 751 individuals; 0/751 membrane-like individually; rim level 0.515)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 1.24 (aggregate of 751 individuals; 0/751 membrane-like individually; rim level 0.421)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #232 (t=2500, R_eq 8.65): none; #517 (t=3000, R_eq 7.69): none; #461 (t=2400, R_eq 7.42): none; #1242 (t=7700, R_eq 4.11): none
- species `prey` (channels ['prey a'], own threshold): components final 32, mean 52.8, max 231; tracks 999, persistent 0; splits 231, persistent splits 30 (K=5), max generation 3, merges 40, merge/split 0.173; moving tracks 25
- species `predator` (channels ['predator b'], own threshold): components final 106, mean 105.5, max 132; tracks 1182, persistent 0; splits 289, persistent splits 112 (K=5), max generation 2, merges 87, merge/split 0.301; moving tracks 63

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 140 of 751 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
