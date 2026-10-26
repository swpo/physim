# Evidence pack: condensate-food-chain (seed 13)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [40, 40]; wall 22s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1648-c41-review-arena-heldout/L40_s13 --seeds 13 --size 40 40 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0486, 1.3312], min area 6 px

## Measurements
- components: final 4, mean 3.4, max 7; occupancy final 0.17
- tracks: 54; persistent (alive >= 50% of run): 0; longest 25 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 17, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.235, nucleations 8
- channel total drift (end/start - 1): [-0.6433, 3.0055, -0.2282, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 95: holes 0, rim-vs-core 0.18, rim-vs-outside 0.29, heterogeneity 0.03; core [0.007, 0.818, 0.742, 0.039] rim [0.016, 0.638, 0.741, 0.039]
  - track 24 at frame 32: holes 0, rim-vs-core 0.25, rim-vs-outside 0.28, heterogeneity 0.04; core [0.004, 0.872, 0.74, 0.123] rim [0.017, 0.621, 0.735, 0.123]
  - track 31 at frame 55: holes 0, rim-vs-core 0.17, rim-vs-outside 0.34, heterogeneity 0.04; core [0.006, 0.83, 0.732, 0.122] rim [0.014, 0.663, 0.731, 0.122]
  - track 44 at frame 99: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.04; core [0.004, 0.847, 0.742, 0.116] rim [0.016, 0.621, 0.736, 0.116]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 2.89 (aggregate of 27 individuals; 2/27 membrane-like individually; rim level 0.221)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.78 (aggregate of 27 individuals; 1/27 membrane-like individually; rim level 0.491)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.97 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.561)
  - radial waste w: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 1.17 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.373)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #42 (t=9500, R_eq 3.95): none; #24 (t=3200, R_eq 4.72): none; #31 (t=5500, R_eq 5.53): none; #44 (t=9900, R_eq 5.84): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 0.9, max 6; tracks 33, persistent 0; splits 9, persistent splits 0 (K=5), max generation 0, merges 2, merge/split 0.222; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 4, mean 2.9, max 6; tracks 43, persistent 0; splits 11, persistent splits 1 (K=5), max generation 1, merges 4, merge/split 0.364; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
