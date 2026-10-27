# Evidence pack: condensate-food-chain (seed 30)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [80, 80]; wall 60s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/ar/pack80/seed30 --seeds 30 --size 80 80 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0395, 1.3478], min area 6 px

## Measurements
- components: final 9, mean 13.6, max 34; occupancy final 0.20
- tracks: 192; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.67, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 9, 7], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 50, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 4, merges 18, merge/split ratio 0.36, nucleations 31
- channel total drift (end/start - 1): [-0.4882, 3.0831, -0.3051, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 21: holes 0, rim-vs-core 0.14, rim-vs-outside 0.43, heterogeneity 0.04; core [0.002, 0.835, 0.702, 0.16] rim [0.01, 0.692, 0.685, 0.164]
  - track 28 at frame 19: holes 1, rim-vs-core 0.20, rim-vs-outside 0.59, heterogeneity 0.08; core [0.889, 0.039, 0.035, 0.841] rim [0.707, 0.033, 0.097, 0.78]
  - track 21 at frame 16: holes 0, rim-vs-core 0.18, rim-vs-outside 0.32, heterogeneity 0.07; core [0.003, 0.832, 0.537, 0.315] rim [0.008, 0.653, 0.517, 0.331]
  - track 161 at frame 91: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.04; core [0.006, 0.847, 0.729, 0.118] rim [0.019, 0.588, 0.727, 0.118]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 3.72 (aggregate of 72 individuals; 8/72 membrane-like individually; rim level 0.251)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.75 (aggregate of 72 individuals; 9/72 membrane-like individually; rim level 0.505)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.958 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.52)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 1.26 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.425)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=2100, R_eq 6.98): none; #28 (t=1900, R_eq 8.99, ring): ['prey a']; #21 (t=1600, R_eq 4.37): none; #161 (t=9100, R_eq 3.29): none
- species `prey` (channels ['prey a'], own threshold): components final 2, mean 4.7, max 26; tracks 118, persistent 0; splits 25, persistent splits 5 (K=5), max generation 3, merges 7, merge/split 0.28; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 7, mean 10.5, max 17; tracks 149, persistent 0; splits 29, persistent splits 9 (K=5), max generation 1, merges 17, merge/split 0.586; moving tracks 7

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 72 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
