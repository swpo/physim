# Evidence pack: condensate-food-chain (seed 4)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 177s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/more/seed4 --seeds 4 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0369, 1.3539], min area 6 px

## Measurements
- components: final 30, mean 36.7, max 73; occupancy final 0.25
- tracks: 462; persistent (alive >= 50% of run): 0; longest 43 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.21, final 4; holes at thresholds 0.2/0.35/0.5 final [5, 4, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 28, 18], H1 [7, 4, 1]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00577/time; max body lengths 1.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 127, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 4, merges 41, merge/split ratio 0.323, nucleations 90
- channel total drift (end/start - 1): [-0.3362, 2.7639, -0.4521, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 22: holes 0, rim-vs-core 0.25, rim-vs-outside 0.40, heterogeneity 0.25; core [0.273, 0.692, 0.277, 0.496] rim [0.27, 0.465, 0.353, 0.434]
  - track 132 at frame 24: holes 0, rim-vs-core 0.33, rim-vs-outside 0.32, heterogeneity 0.07; core [0.891, 0.002, 0.046, 0.763] rim [0.579, 0.003, 0.118, 0.697]
  - track 31 at frame 18: holes 0, rim-vs-core 0.18, rim-vs-outside 0.34, heterogeneity 0.31; core [0.402, 0.533, 0.335, 0.502] rim [0.318, 0.373, 0.355, 0.484]
  - track 248 at frame 56: holes 0, rim-vs-core 0.20, rim-vs-outside 0.43, heterogeneity 0.04; core [0.003, 0.868, 0.743, 0.141] rim [0.013, 0.663, 0.737, 0.143]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 183 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 2.91 (aggregate of 183 individuals; 20/183 membrane-like individually; rim level 0.216)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 5.08 (aggregate of 183 individuals; 25/183 membrane-like individually; rim level 0.522)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 0.956 (aggregate of 183 individuals; 0/183 membrane-like individually; rim level 0.53)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 1.24 (aggregate of 183 individuals; 0/183 membrane-like individually; rim level 0.395)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=2200, R_eq 8.81): none; #132 (t=2400, R_eq 5.32): none; #31 (t=1800, R_eq 8.33): none; #248 (t=5600, R_eq 6.15): none
- species `prey` (channels ['prey a'], own threshold): components final 10, mean 12.1, max 60; tracks 281, persistent 0; splits 55, persistent splits 4 (K=5), max generation 2, merges 12, merge/split 0.218; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 21, mean 28.0, max 37; tracks 333, persistent 0; splits 80, persistent splits 35 (K=5), max generation 3, merges 21, merge/split 0.263; moving tracks 21

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 31 of 183 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
