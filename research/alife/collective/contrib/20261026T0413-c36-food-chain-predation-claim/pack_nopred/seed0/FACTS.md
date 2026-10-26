# Evidence pack: condensate-food-chain (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 690s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/packC/s0 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2168], min area 6 px

## Measurements
- components: final 223, mean 222.8, max 230; occupancy final 0.32
- tracks: 521; persistent (alive >= 50% of run): 224; longest 101 frames; alive start-to-end: 18
- size of persistent tracks: max/min area ratio 16.40 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [223, 223, 223], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 78, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 34, merge/split ratio 0.436, nucleations 30
- channel total drift (end/start - 1): [0.2819, None, -0.7382, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 50: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.08; core [0.896, 0.0, 0.034, 0.908] rim [0.501, 0.0, 0.078, 0.783]
  - track 58 at frame 50: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.08; core [0.892, 0.0, 0.035, 0.905] rim [0.492, 0.0, 0.078, 0.783]
  - track 59 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.07; core [0.897, 0.0, 0.033, 0.909] rim [0.522, 0.0, 0.077, 0.786]
  - track 515 at frame 55: holes 0, rim-vs-core 0.42, rim-vs-outside 0.30, heterogeneity 0.08; core [0.885, 0.0, 0.04, 0.886] rim [0.485, 0.0, 0.079, 0.78]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1345 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 19.9 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.88)
  - radial predator b: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.224 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.0008)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.78, rim/outside 0.889 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.112)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 1.4 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=5000, R_eq 5.64): none; #58 (t=5000, R_eq 5.59): none; #59 (t=5000, R_eq 5.61): none; #515 (t=5500, R_eq 5.23): none
- species `prey` (channels ['prey a'], own threshold): components final 223, mean 222.8, max 229; tracks 520, persistent 224; splits 78, persistent splits 3 (K=20), max generation 1, merges 34, merge/split 0.436; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 4.3, max 140; tracks 276, persistent 0; splits 72, persistent splits 0 (K=20), max generation 0, merges 3, merge/split 0.042; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
