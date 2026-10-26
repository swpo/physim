# Evidence pack: condensate-food-chain (seed 2)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 180s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_s2 --seeds 2 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0502, 1.2136], min area 6 px

## Measurements
- components: final 42, mean 55.8, max 106; occupancy final 0.27
- tracks: 420; persistent (alive >= 50% of run): 36; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 8.30 (1 = constant size)
- enclosures: components with a hole mean 0.82, final 1; holes at thresholds 0.2/0.35/0.5 final [7, 11, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 45, 41], H1 [13, 10, 4]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.0055/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 2000, default): splits 91, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 98, merge/split ratio 1.08, nucleations 46
- channel total drift (end/start - 1): [-0.3708, 2.3957, -0.3869, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.17, rim-vs-outside 0.43, heterogeneity 0.06; core [0.895, 0.001, 0.053, 0.527] rim [0.727, 0.001, 0.096, 0.509]
  - track 33 at frame 61: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.06; core [0.913, 0.0, 0.042, 0.526] rim [0.61, 0.0, 0.132, 0.488]
  - track 49 at frame 61: holes 0, rim-vs-core 0.30, rim-vs-outside 0.33, heterogeneity 0.05; core [0.92, 0.0, 0.051, 0.507] rim [0.632, 0.0, 0.126, 0.477]
  - track 187 at frame 70: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.06; core [0.91, 0.0, 0.05, 0.512] rim [0.602, 0.0, 0.13, 0.481]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 304 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 10.3 (aggregate of 304 individuals; 3/304 membrane-like individually; rim level 0.69)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 3.29 (aggregate of 304 individuals; 0/304 membrane-like individually; rim level 0.121)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.39, rim/outside 0.789 (aggregate of 304 individuals; 0/304 membrane-like individually; rim level 0.308)
  - radial waste w: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 1.25 (aggregate of 304 individuals; 0/304 membrane-like individually; rim level 0.49)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6100, R_eq 3.43): none; #33 (t=6100, R_eq 3.52): none; #49 (t=6100, R_eq 3.09): none; #187 (t=7000, R_eq 3.24): none
- species `prey` (channels ['prey a'], own threshold): components final 43, mean 48.3, max 90; tracks 332, persistent 37; splits 63, persistent splits 3 (K=20), max generation 1, merges 10, merge/split 0.159; moving tracks 41
- species `predator` (channels ['predator b'], own threshold): components final 7, mean 9.4, max 28; tracks 163, persistent 0; splits 21, persistent splits 0 (K=20), max generation 0, merges 39, merge/split 1.86; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 304 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
