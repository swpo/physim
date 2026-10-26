# Evidence pack: condensate-food-chain (seed 7)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 400 steps x dt 0.25 (--dt; world META dt 0.5) = time 12000; grid [128, 128]; wall 309s; status ok
- command: `python -m labkit.run world_claim.py --out rerun_dthalf/seed7 --seeds 7 --size 128 128 --frames 120 --spf 400 --dt 0.25 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0337, 1.3329], min area 6 px

## Measurements
- components: final 36, mean 35.8, max 69; occupancy final 0.24
- tracks: 461; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.55, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 39, 21], H1 [2, 2, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00669/time; max body lengths 1.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 147, persistent splits 68 (0 more failed only because the siblings re-merged within K), max generation 5, merges 46, merge/split ratio 0.313, nucleations 55
- channel total drift (end/start - 1): [-0.2799, 2.5958, -0.4742, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 62 at frame 20: holes 0, rim-vs-core 0.20, rim-vs-outside 0.50, heterogeneity 0.07; core [0.001, 0.922, 0.53, 0.259] rim [0.015, 0.721, 0.52, 0.265]
  - track 78 at frame 19: holes 0, rim-vs-core 0.34, rim-vs-outside 0.32, heterogeneity 0.07; core [0.918, 0.0, 0.05, 0.81] rim [0.601, 0.0, 0.134, 0.729]
  - track 28 at frame 17: holes 0, rim-vs-core 0.15, rim-vs-outside 0.43, heterogeneity 0.04; core [0.003, 0.831, 0.776, 0.086] rim [0.013, 0.679, 0.767, 0.087]
  - track 427 at frame 116: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.07; core [0.905, 0.0, 0.048, 0.812] rim [0.565, 0.0, 0.13, 0.732]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 191 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 3.81 (aggregate of 191 individuals; 23/191 membrane-like individually; rim level 0.279)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 4.97 (aggregate of 191 individuals; 16/191 membrane-like individually; rim level 0.468)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.942 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.48)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 1.27 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.455)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #62 (t=2000, R_eq 7): none; #78 (t=1900, R_eq 5.53): none; #28 (t=1700, R_eq 7): none; #427 (t=11600, R_eq 5.53): none
- species `prey` (channels ['prey a'], own threshold): components final 16, mean 15.4, max 62; tracks 316, persistent 0; splits 97, persistent splits 21 (K=5), max generation 5, merges 9, merge/split 0.093; moving tracks 6
- species `predator` (channels ['predator b'], own threshold): components final 27, mean 24.0, max 33; tracks 305, persistent 0; splits 74, persistent splits 32 (K=5), max generation 2, merges 18, merge/split 0.243; moving tracks 22

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.25 only relabels time (world META dt 0.5): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 26 of 191 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
