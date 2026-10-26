# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 176s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa8 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0398, 1.2597], min area 6 px

## Measurements
- components: final 27, mean 36.1, max 77; occupancy final 0.26
- tracks: 367; persistent (alive >= 50% of run): 14; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.09 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 28, 27], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00505/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 82, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 97, merge/split ratio 1.18, nucleations 14
- channel total drift (end/start - 1): [-0.747, 5.6849, -0.2437, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 61: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.04; core [0.003, 0.926, 0.731, 0.034] rim [0.012, 0.671, 0.729, 0.034]
  - track 180 at frame 65: holes 0, rim-vs-core 0.31, rim-vs-outside 0.29, heterogeneity 0.05; core [0.003, 0.921, 0.736, 0.041] rim [0.015, 0.608, 0.734, 0.039]
  - track 187 at frame 66: holes 0, rim-vs-core 0.16, rim-vs-outside 0.41, heterogeneity 0.05; core [0.003, 0.916, 0.712, 0.077] rim [0.009, 0.752, 0.708, 0.081]
  - track 255 at frame 79: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.04; core [0.002, 0.932, 0.736, 0.052] rim [0.013, 0.639, 0.734, 0.051]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 196 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 2.19 (aggregate of 196 individuals; 8/196 membrane-like individually; rim level 0.175)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 4.19 (aggregate of 196 individuals; 8/196 membrane-like individually; rim level 0.554)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.987 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.558)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 1.14 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.263)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #63 (t=6100, R_eq 4.55): none; #180 (t=6500, R_eq 5.05): none; #187 (t=6600, R_eq 4.26): none; #255 (t=7900, R_eq 4.92): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 11.8, max 71; tracks 258, persistent 0; splits 63, persistent splits 0 (K=20), max generation 0, merges 15, merge/split 0.238; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 27, mean 26.6, max 32; tracks 144, persistent 17; splits 29, persistent splits 4 (K=20), max generation 2, merges 30, merge/split 1.03; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 196 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
