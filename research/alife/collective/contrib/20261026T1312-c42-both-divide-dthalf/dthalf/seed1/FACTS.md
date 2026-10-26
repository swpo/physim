# Evidence pack: condensate-food-chain (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 400 steps x dt 0.25 (--dt; world META dt 0.5) = time 12000; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/dthalf/seed1 --seeds 1 --size 128 128 --frames 120 --spf 400 --dt 0.25 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0318, 1.3403], min area 6 px

## Measurements
- components: final 31, mean 38.1, max 74; occupancy final 0.21
- tracks: 435; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.63, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 30, 19], H1 [1, 1, 1]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.00557/time; max body lengths 1.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 141, persistent splits 59 (0 more failed only because the siblings re-merged within K), max generation 9, merges 37, merge/split ratio 0.262, nucleations 55
- channel total drift (end/start - 1): [-0.3245, 2.563, -0.4067, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 31: holes 0, rim-vs-core 0.26, rim-vs-outside 0.41, heterogeneity 0.06; core [0.907, 0.0, 0.047, 0.894] rim [0.656, 0.0, 0.102, 0.842]
  - track 1 at frame 26: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.07; core [0.897, 0.0, 0.052, 0.893] rim [0.552, 0.0, 0.122, 0.829]
  - track 131 at frame 30: holes 0, rim-vs-core 0.33, rim-vs-outside 0.32, heterogeneity 0.06; core [0.906, 0.0, 0.047, 0.903] rim [0.59, 0.001, 0.118, 0.836]
  - track 411 at frame 118: holes 0, rim-vs-core 0.26, rim-vs-outside 0.52, heterogeneity 0.07; core [0.888, 0.014, 0.029, 0.821] rim [0.672, 0.015, 0.126, 0.715]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 196 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 4.46 (aggregate of 196 individuals; 8/196 membrane-like individually; rim level 0.321)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 5.06 (aggregate of 196 individuals; 13/196 membrane-like individually; rim level 0.439)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.952 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.485)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 1.27 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.439)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #63 (t=3100, R_eq 4.95): none; #1 (t=2600, R_eq 5.11): none; #131 (t=3000, R_eq 5.23): none; #411 (t=11800, R_eq 6.93): none
- species `prey` (channels ['prey a'], own threshold): components final 10, mean 17.6, max 58; tracks 290, persistent 0; splits 80, persistent splits 20 (K=5), max generation 8, merges 9, merge/split 0.113; moving tracks 6
- species `predator` (channels ['predator b'], own threshold): components final 23, mean 24.0, max 31; tracks 311, persistent 0; splits 71, persistent splits 30 (K=5), max generation 3, merges 22, merge/split 0.31; moving tracks 13

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.25 only relabels time (world META dt 0.5): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 13 of 196 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
