# Evidence pack: condensate-food-chain (seed 0)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 171s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_k5 --seeds 0 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0566, 1.1447], min area 6 px

## Measurements
- components: final 50, mean 61.1, max 108; occupancy final 0.25
- tracks: 612; persistent (alive >= 50% of run): 13; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.70 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [64, 55, 47], H1 [3, 1, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.00661/time; max body lengths 2.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 151, persistent splits 65 (0 more failed only because the siblings re-merged within K), max generation 6, merges 118, merge/split ratio 0.781, nucleations 66
- channel total drift (end/start - 1): [-0.3573, 1.9144, -0.3827, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 96 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.07; core [0.905, 0.0, 0.053, 0.492] rim [0.575, 0.0, 0.175, 0.44]
  - track 112 at frame 62: holes 0, rim-vs-core 0.34, rim-vs-outside 0.31, heterogeneity 0.07; core [0.908, 0.0, 0.053, 0.513] rim [0.588, 0.0, 0.167, 0.466]
  - track 133 at frame 49: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.07; core [0.908, 0.001, 0.059, 0.532] rim [0.574, 0.001, 0.171, 0.487]
  - track 561 at frame 114: holes 0, rim-vs-core 0.19, rim-vs-outside 0.46, heterogeneity 0.07; core [0.881, 0.007, 0.063, 0.585] rim [0.702, 0.008, 0.13, 0.558]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 345 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 6.35 (aggregate of 345 individuals; 4/345 membrane-like individually; rim level 0.494)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 3.98 (aggregate of 345 individuals; 6/345 membrane-like individually; rim level 0.285)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.58, rim/outside 0.881 (aggregate of 345 individuals; 0/345 membrane-like individually; rim level 0.496)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 1.28 (aggregate of 345 individuals; 0/345 membrane-like individually; rim level 0.394)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #96 (t=6200, R_eq 3.95): none; #112 (t=6200, R_eq 3.78): none; #133 (t=4900, R_eq 3.7): none; #561 (t=11400, R_eq 4.44): none
- species `prey` (channels ['prey a'], own threshold): components final 37, mean 40.2, max 92; tracks 422, persistent 12; splits 107, persistent splits 46 (K=5), max generation 5, merges 12, merge/split 0.112; moving tracks 25
- species `predator` (channels ['predator b'], own threshold): components final 15, mean 23.8, max 39; tracks 281, persistent 1; splits 37, persistent splits 3 (K=5), max generation 1, merges 59, merge/split 1.59; moving tracks 11

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 345 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
