# Evidence pack: condensate-food-chain (seed 11)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [32, 32]; wall 18s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1646-c41-review-arena-size/L32_s11 --seeds 11 --size 32 32 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0422, 1.4032], min area 6 px

## Measurements
- components: final 1, mean 2.5, max 5; occupancy final 0.16
- tracks: 27; persistent (alive >= 50% of run): 0; longest 31 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 7, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.286, nucleations 6
- channel total drift (end/start - 1): [-0.6623, 3.7709, -0.2226, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 17: holes 0, rim-vs-core 0.23, rim-vs-outside 0.52, heterogeneity 0.06; core [0.909, 0.018, 0.021, 0.998] rim [0.692, 0.017, 0.095, 0.96]
  - track 22 at frame 105: holes 0, rim-vs-core 0.16, rim-vs-outside 0.45, heterogeneity 0.03; core [0.003, 0.872, 0.734, 0.105] rim [0.01, 0.713, 0.731, 0.105]
  - track 19 at frame 83: holes 0, rim-vs-core 0.16, rim-vs-outside 0.23, heterogeneity 0.03; core [0.002, 0.804, 0.421, 0.556] rim [0.006, 0.64, 0.411, 0.563]
  - track 5 at frame 13: holes 0, rim-vs-core 0.19, rim-vs-outside 0.59, heterogeneity 0.07; core [0.916, 0.019, 0.01, 0.967] rim [0.759, 0.022, 0.084, 0.889]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 10 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 1.97 (aggregate of 10 individuals; 2/10 membrane-like individually; rim level 0.175)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 6.07 (aggregate of 10 individuals; 3/10 membrane-like individually; rim level 0.555)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.966 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.551)
  - radial waste w: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 1.16 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.348)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=1700, R_eq 6.21): none; #22 (t=10500, R_eq 6.13, ring): ['predator b']; #19 (t=8300, R_eq 3.24): none; #5 (t=1300, R_eq 6.21): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 0.8, max 4; tracks 12, persistent 0; splits 1, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 1, mean 2.0, max 3; tracks 26, persistent 0; splits 6, persistent splits 2 (K=5), max generation 1, merges 2, merge/split 0.333; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 10 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
