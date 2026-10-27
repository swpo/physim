# Evidence pack: condensate-food-chain (seed 21)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 400 steps x dt 0.25 (--dt; world META dt 0.5) = time 12000; grid [128, 128]; wall 350s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1639-c41-review-foodchain-dthalf/dthalf_s21 --seeds 21 --size 128 128 --frames 120 --spf 400 --dt 0.25 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.036, 1.343], min area 6 px

## Measurements
- components: final 33, mean 34.4, max 69; occupancy final 0.24
- tracks: 470; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.08, final 2; holes at thresholds 0.2/0.35/0.5 final [3, 2, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 35, 22], H1 [5, 2, 1]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0051/time; max body lengths 1.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 144, persistent splits 63 (0 more failed only because the siblings re-merged within K), max generation 6, merges 41, merge/split ratio 0.285, nucleations 64
- channel total drift (end/start - 1): [-0.3971, 3.0464, -0.4051, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 82 at frame 19: holes 0, rim-vs-core 0.15, rim-vs-outside 0.42, heterogeneity 0.04; core [0.003, 0.827, 0.704, 0.092] rim [0.011, 0.676, 0.699, 0.092]
  - track 130 at frame 20: holes 0, rim-vs-core 0.24, rim-vs-outside 0.52, heterogeneity 0.09; core [0.844, 0.065, 0.034, 0.848] rim [0.659, 0.045, 0.136, 0.736]
  - track 84 at frame 18: holes 0, rim-vs-core 0.24, rim-vs-outside 0.25, heterogeneity 0.05; core [0.003, 0.837, 0.662, 0.142] rim [0.014, 0.598, 0.654, 0.145]
  - track 444 at frame 117: holes 0, rim-vs-core 0.22, rim-vs-outside 0.40, heterogeneity 0.06; core [0.875, 0.003, 0.053, 0.872] rim [0.659, 0.003, 0.091, 0.836]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 2.52 (aggregate of 181 individuals; 15/181 membrane-like individually; rim level 0.188)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.22 (aggregate of 181 individuals; 21/181 membrane-like individually; rim level 0.527)
  - radial fuel u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.966 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.558)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 1.26 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.343)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #82 (t=1900, R_eq 6.72): none; #130 (t=2000, R_eq 7.25): none; #84 (t=1800, R_eq 5.64): none; #444 (t=11700, R_eq 5.94): none
- species `prey` (channels ['prey a'], own threshold): components final 11, mean 12.3, max 57; tracks 307, persistent 0; splits 79, persistent splits 13 (K=5), max generation 6, merges 11, merge/split 0.139; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 25, mean 25.8, max 36; tracks 371, persistent 0; splits 92, persistent splits 38 (K=5), max generation 2, merges 34, merge/split 0.37; moving tracks 14

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.25 only relabels time (world META dt 0.5): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 28 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
