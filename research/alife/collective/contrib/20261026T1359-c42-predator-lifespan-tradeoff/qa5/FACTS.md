# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 178s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa5 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0534, 1.2777], min area 6 px

## Measurements
- components: final 37, mean 43.7, max 71; occupancy final 0.22
- tracks: 323; persistent (alive >= 50% of run): 17; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 42.14 (1 = constant size)
- enclosures: components with a hole mean 3.64, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 42, 34], H1 [4, 3, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 61, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 64, merge/split ratio 1.05, nucleations 49
- channel total drift (end/start - 1): [-0.704, 4.974, -0.2474, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 58: holes 0, rim-vs-core 0.31, rim-vs-outside 0.28, heterogeneity 0.05; core [0.006, 0.89, 0.68, 0.12] rim [0.021, 0.576, 0.677, 0.121]
  - track 65 at frame 54: holes 0, rim-vs-core 0.27, rim-vs-outside 0.27, heterogeneity 0.04; core [0.007, 0.881, 0.717, 0.047] rim [0.021, 0.607, 0.716, 0.047]
  - track 135 at frame 49: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.05; core [0.005, 0.921, 0.717, 0.118] rim [0.018, 0.644, 0.715, 0.117]
  - track 290 at frame 107: holes 0, rim-vs-core 0.26, rim-vs-outside 0.27, heterogeneity 0.04; core [0.007, 0.866, 0.656, 0.215] rim [0.018, 0.605, 0.654, 0.216]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 241 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.862 (aggregate of 241 individuals; 5/241 membrane-like individually; rim level 0.0654)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 6.78 (aggregate of 241 individuals; 29/241 membrane-like individually; rim level 0.698)
  - radial fuel u: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.999 (aggregate of 241 individuals; 0/241 membrane-like individually; rim level 0.655)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 1.11 (aggregate of 241 individuals; 0/241 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #64 (t=5800, R_eq 3.61): none; #65 (t=5400, R_eq 2.99): none; #135 (t=4900, R_eq 3.57): none; #290 (t=10700, R_eq 2.88): none
- species `prey` (channels ['prey a'], own threshold): components final 1, mean 6.2, max 61; tracks 217, persistent 0; splits 34, persistent splits 0 (K=20), max generation 0, merges 12, merge/split 0.353; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 36, mean 39.4, max 46; tracks 194, persistent 16; splits 38, persistent splits 8 (K=20), max generation 2, merges 31, merge/split 0.816; moving tracks 10

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 241 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
