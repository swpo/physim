# Evidence pack: condensate-food-chain (seed 1)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 169s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_s1 --seeds 1 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.05, 1.1271], min area 6 px

## Measurements
- components: final 46, mean 61.9, max 102; occupancy final 0.26
- tracks: 449; persistent (alive >= 50% of run): 38; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.17 (1 = constant size)
- enclosures: components with a hole mean 0.80, final 1; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 49, 46], H1 [7, 4, 3]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.00459/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 2000, default): splits 112, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 92, merge/split ratio 0.821, nucleations 34
- channel total drift (end/start - 1): [-0.2915, 1.9254, -0.4104, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 62: holes 0, rim-vs-core 0.31, rim-vs-outside 0.37, heterogeneity 0.07; core [0.883, 0.0, 0.053, 0.571] rim [0.585, 0.0, 0.141, 0.531]
  - track 82 at frame 62: holes 0, rim-vs-core 0.34, rim-vs-outside 0.32, heterogeneity 0.06; core [0.893, 0.0, 0.067, 0.541] rim [0.561, 0.0, 0.146, 0.508]
  - track 83 at frame 62: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.07; core [0.893, 0.0, 0.063, 0.527] rim [0.56, 0.0, 0.147, 0.491]
  - track 377 at frame 104: holes 0, rim-vs-core 0.39, rim-vs-outside 0.29, heterogeneity 0.07; core [0.879, 0.0, 0.055, 0.557] rim [0.509, 0.001, 0.165, 0.504]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 346 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 10.3 (aggregate of 346 individuals; 1/346 membrane-like individually; rim level 0.674)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 3.31 (aggregate of 346 individuals; 3/346 membrane-like individually; rim level 0.123)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.52, rim/outside 0.813 (aggregate of 346 individuals; 0/346 membrane-like individually; rim level 0.335)
  - radial waste w: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 1.25 (aggregate of 346 individuals; 0/346 membrane-like individually; rim level 0.559)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #79 (t=6200, R_eq 3.78): none; #82 (t=6200, R_eq 3.14): none; #83 (t=6200, R_eq 3.29): none; #377 (t=10400, R_eq 3.95): none
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 53.2, max 86; tracks 325, persistent 37; splits 75, persistent splits 8 (K=20), max generation 2, merges 10, merge/split 0.133; moving tracks 33
- species `predator` (channels ['predator b'], own threshold): components final 5, mean 11.3, max 24; tracks 177, persistent 0; splits 20, persistent splits 0 (K=20), max generation 0, merges 49, merge/split 2.45; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 346 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
