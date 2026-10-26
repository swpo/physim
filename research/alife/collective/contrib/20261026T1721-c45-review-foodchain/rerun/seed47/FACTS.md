# Evidence pack: condensate-food-chain (seed 47)

- world: `../../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1721-c45-review-foodchain/rerun/seed47 --seeds 47 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.037, 1.3375], min area 6 px

## Measurements
- components: final 31, mean 33.0, max 61; occupancy final 0.21
- tracks: 457; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.76, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 32, 19], H1 [1, 1, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00809/time; max body lengths 1.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 145, persistent splits 52 (0 more failed only because the siblings re-merged within K), max generation 3, merges 40, merge/split ratio 0.276, nucleations 66
- channel total drift (end/start - 1): [-0.4579, 3.3834, -0.365, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 123 at frame 25: holes 0, rim-vs-core 0.21, rim-vs-outside 0.47, heterogeneity 0.06; core [0.001, 0.926, 0.571, 0.24] rim [0.01, 0.716, 0.561, 0.247]
  - track 62 at frame 19: holes 0, rim-vs-core 0.26, rim-vs-outside 0.26, heterogeneity 0.04; core [0.005, 0.849, 0.766, 0.095] rim [0.018, 0.593, 0.76, 0.096]
  - track 89 at frame 19: holes 0, rim-vs-core 0.25, rim-vs-outside 0.27, heterogeneity 0.04; core [0.004, 0.862, 0.708, 0.121] rim [0.015, 0.613, 0.705, 0.122]
  - track 361 at frame 99: holes 0, rim-vs-core 0.22, rim-vs-outside 0.24, heterogeneity 0.05; core [0.002, 0.837, 0.463, 0.49] rim [0.008, 0.622, 0.461, 0.489]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.79 (aggregate of 163 individuals; 18/163 membrane-like individually; rim level 0.212)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 5.18 (aggregate of 163 individuals; 23/163 membrane-like individually; rim level 0.503)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 0.954 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.535)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.29 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.377)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #123 (t=2500, R_eq 8): none; #62 (t=1900, R_eq 5.56): none; #89 (t=1900, R_eq 4.3): none; #361 (t=9900, R_eq 3.34): none
- species `prey` (channels ['prey a'], own threshold): components final 8, mean 11.6, max 60; tracks 287, persistent 0; splits 75, persistent splits 8 (K=5), max generation 3, merges 8, merge/split 0.107; moving tracks 7
- species `predator` (channels ['predator b'], own threshold): components final 25, mean 24.8, max 34; tracks 332, persistent 0; splits 94, persistent splits 32 (K=5), max generation 2, merges 17, merge/split 0.181; moving tracks 17

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 32 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
