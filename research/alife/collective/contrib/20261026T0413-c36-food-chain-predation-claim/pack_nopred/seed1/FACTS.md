# Evidence pack: condensate-food-chain (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 683s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/packC/s1 --seeds 1 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0093, 1.2165], min area 6 px

## Measurements
- components: final 218, mean 217.0, max 225; occupancy final 0.31
- tracks: 496; persistent (alive >= 50% of run): 218; longest 101 frames; alive start-to-end: 22
- size of persistent tracks: max/min area ratio 13.89 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [218, 218, 218], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 87, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 46, merge/split ratio 0.529, nucleations 30
- channel total drift (end/start - 1): [0.3186, None, -0.7372, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.895, 0.0, 0.038, 0.894] rim [0.51, 0.0, 0.077, 0.783]
  - track 18 at frame 50: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.08; core [0.896, 0.0, 0.032, 0.912] rim [0.498, 0.0, 0.08, 0.776]
  - track 23 at frame 50: holes 0, rim-vs-core 0.42, rim-vs-outside 0.30, heterogeneity 0.08; core [0.89, 0.0, 0.037, 0.895] rim [0.485, 0.0, 0.079, 0.779]
  - track 480 at frame 55: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.895, 0.0, 0.038, 0.892] rim [0.51, 0.0, 0.077, 0.784]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1309 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 20.6 (aggregate of 1309 individuals; 0/1309 membrane-like individually; rim level 0.881)
  - radial predator b: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.23 (aggregate of 1309 individuals; 0/1309 membrane-like individually; rim level 0.0008)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.04, rim/outside 0.884 (aggregate of 1309 individuals; 0/1309 membrane-like individually; rim level 0.113)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 1.42 (aggregate of 1309 individuals; 0/1309 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=5000, R_eq 5.26): none; #18 (t=5000, R_eq 5.86): none; #23 (t=5000, R_eq 5.41): none; #480 (t=5500, R_eq 5.2): none
- species `prey` (channels ['prey a'], own threshold): components final 218, mean 217.0, max 225; tracks 497, persistent 218; splits 88, persistent splits 8 (K=20), max generation 1, merges 47, merge/split 0.534; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 4.1, max 139; tracks 276, persistent 0; splits 72, persistent splits 0 (K=20), max generation 0, merges 2, merge/split 0.028; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
