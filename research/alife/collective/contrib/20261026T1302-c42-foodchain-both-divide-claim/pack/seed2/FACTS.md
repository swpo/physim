# Evidence pack: condensate-food-chain (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 186s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/pack/seed2 --seeds 2 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0335, 1.3623], min area 6 px

## Measurements
- components: final 35, mean 37.6, max 75; occupancy final 0.21
- tracks: 465; persistent (alive >= 50% of run): 0; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.14, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 32, 17], H1 [9, 5, 1]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00707/time; max body lengths 1.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 130, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 4, merges 44, merge/split ratio 0.338, nucleations 86
- channel total drift (end/start - 1): [-0.4001, 2.9891, -0.3833, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 27: holes 0, rim-vs-core 0.16, rim-vs-outside 0.63, heterogeneity 0.07; core [0.93, 0.005, 0.032, 0.823] rim [0.783, 0.005, 0.08, 0.783]
  - track 131 at frame 28: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.06; core [0.892, 0.0, 0.049, 0.81] rim [0.597, 0.0, 0.104, 0.763]
  - track 114 at frame 25: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.06; core [0.897, 0.003, 0.047, 0.837] rim [0.586, 0.003, 0.114, 0.779]
  - track 255 at frame 58: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.04; core [0.005, 0.856, 0.631, 0.278] rim [0.015, 0.597, 0.629, 0.278]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 200 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 3.33 (aggregate of 200 individuals; 12/200 membrane-like individually; rim level 0.244)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 4.94 (aggregate of 200 individuals; 30/200 membrane-like individually; rim level 0.502)
  - radial fuel u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.967 (aggregate of 200 individuals; 0/200 membrane-like individually; rim level 0.529)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 1.23 (aggregate of 200 individuals; 0/200 membrane-like individually; rim level 0.405)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=2700, R_eq 6.31): none; #131 (t=2800, R_eq 4.55): none; #114 (t=2500, R_eq 5.05): none; #255 (t=5800, R_eq 3.14): none
- species `prey` (channels ['prey a'], own threshold): components final 10, mean 14.0, max 64; tracks 289, persistent 0; splits 65, persistent splits 5 (K=5), max generation 2, merges 11, merge/split 0.169; moving tracks 6
- species `predator` (channels ['predator b'], own threshold): components final 27, mean 27.0, max 33; tracks 359, persistent 0; splits 90, persistent splits 34 (K=5), max generation 2, merges 29, merge/split 0.322; moving tracks 19

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 200 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
