# Evidence pack: condensate-food-chain (seed 21)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 202s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1510-c43-review-foodchain/world.py --out collective/contrib/20261026T1510-c43-review-foodchain/rerun/seed21 --seeds 21 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0419, 1.3626], min area 6 px

## Measurements
- components: final 33, mean 34.9, max 69; occupancy final 0.17
- tracks: 444; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.71, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 32, 16], H1 [3, 1, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00516/time; max body lengths 1.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 128, persistent splits 58 (0 more failed only because the siblings re-merged within K), max generation 6, merges 38, merge/split ratio 0.297, nucleations 82
- channel total drift (end/start - 1): [-0.4315, 2.5444, -0.3354, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 107 at frame 20: holes 0, rim-vs-core 0.24, rim-vs-outside 0.52, heterogeneity 0.08; core [0.85, 0.055, 0.031, 0.862] rim [0.662, 0.04, 0.133, 0.75]
  - track 72 at frame 19: holes 0, rim-vs-core 0.13, rim-vs-outside 0.42, heterogeneity 0.03; core [0.002, 0.823, 0.701, 0.112] rim [0.01, 0.69, 0.695, 0.113]
  - track 73 at frame 18: holes 0, rim-vs-core 0.23, rim-vs-outside 0.24, heterogeneity 0.05; core [0.003, 0.836, 0.663, 0.155] rim [0.014, 0.609, 0.655, 0.158]
  - track 415 at frame 114: holes 0, rim-vs-core 0.21, rim-vs-outside 0.25, heterogeneity 0.04; core [0.006, 0.816, 0.72, 0.056] rim [0.016, 0.605, 0.717, 0.057]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 2.59 (aggregate of 186 individuals; 10/186 membrane-like individually; rim level 0.183)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 5.44 (aggregate of 186 individuals; 19/186 membrane-like individually; rim level 0.553)
  - radial fuel u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.972 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.57)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 1.26 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.324)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #107 (t=2000, R_eq 7.23): none; #72 (t=1900, R_eq 6.72): none; #73 (t=1800, R_eq 5.64): none; #415 (t=11400, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 6, mean 10.8, max 57; tracks 291, persistent 0; splits 63, persistent splits 7 (K=5), max generation 1, merges 11, merge/split 0.175; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 26, mean 27.7, max 36; tracks 353, persistent 0; splits 80, persistent splits 30 (K=5), max generation 2, merges 33, merge/split 0.412; moving tracks 21

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 186 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
