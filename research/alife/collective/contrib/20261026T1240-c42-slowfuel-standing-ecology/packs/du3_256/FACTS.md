# Evidence pack: condensate-food-chain (seed 0)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 638s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_256 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0523, 1.1465], min area 6 px

## Measurements
- components: final 193, mean 245.2, max 413; occupancy final 0.26
- tracks: 1902; persistent (alive >= 50% of run): 89; longest 101 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 2.18, final 4; holes at thresholds 0.2/0.35/0.5 final [16, 13, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [245, 207, 170], H1 [18, 9, 1]
- motion: 145 long-lived tracks moved >= 1 body length; max speed 0.00604/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 2000, default): splits 461, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 2, merges 366, merge/split ratio 0.794, nucleations 175
- channel total drift (end/start - 1): [-0.3215, 1.9782, -0.4045, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 50: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.07; core [0.905, 0.001, 0.046, 0.572] rim [0.577, 0.001, 0.155, 0.524]
  - track 170 at frame 50: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.07; core [0.894, 0.001, 0.049, 0.612] rim [0.57, 0.001, 0.156, 0.564]
  - track 196 at frame 50: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.07; core [0.906, 0.0, 0.048, 0.62] rim [0.572, 0.0, 0.155, 0.573]
  - track 1182 at frame 72: holes 0, rim-vs-core 0.33, rim-vs-outside 0.31, heterogeneity 0.07; core [0.889, 0.002, 0.049, 0.537] rim [0.584, 0.002, 0.155, 0.49]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1381 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 8.11 (aggregate of 1381 individuals; 23/1381 membrane-like individually; rim level 0.591)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 3.65 (aggregate of 1381 individuals; 12/1381 membrane-like individually; rim level 0.196)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2, rim/outside 0.843 (aggregate of 1381 individuals; 0/1381 membrane-like individually; rim level 0.389)
  - radial waste w: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 1.23 (aggregate of 1381 individuals; 0/1381 membrane-like individually; rim level 0.502)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=5000, R_eq 3.91): none; #170 (t=5000, R_eq 3.95): none; #196 (t=5000, R_eq 3.87): none; #1182 (t=7200, R_eq 4.03): none
- species `prey` (channels ['prey a'], own threshold): components final 165, mean 185.8, max 351; tracks 1399, persistent 88; splits 334, persistent splits 25 (K=20), max generation 2, merges 49, merge/split 0.147; moving tracks 94
- species `predator` (channels ['predator b'], own threshold): components final 40, mean 71.0, max 110; tracks 783, persistent 2; splits 91, persistent splits 0 (K=20), max generation 0, merges 171, merge/split 1.88; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 1381 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
