# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [256, 256]; wall 1013s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/20261026T0600-c34-review-food-chain/rerun/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0089, 1.2436], min area 6 px

## Measurements
- components: final 177, mean 169.2, max 232; occupancy final 0.32
- tracks: 762; persistent (alive >= 50% of run): 174; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 12.67 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [177, 177, 177], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00472/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 190, persistent splits 64 (0 more failed only because the siblings re-merged within K), max generation 3, merges 80, merge/split ratio 0.421, nucleations 15
- channel total drift (end/start - 1): [0.2947, -1.0, -0.7338, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.51, heterogeneity 0.07; core [0.958, 0.0, 0.024, 0.955] rim [0.624, 0.0, 0.076, 0.87]
  - track 139 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.52, heterogeneity 0.07; core [0.952, 0.0, 0.023, 0.958] rim [0.635, 0.0, 0.076, 0.869]
  - track 194 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.52, heterogeneity 0.07; core [0.957, 0.0, 0.023, 0.956] rim [0.636, 0.0, 0.075, 0.871]
  - track 682 at frame 118: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.958, 0.0, 0.023, 0.956] rim [0.651, 0.0, 0.074, 0.873]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1015 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 24.2 (aggregate of 1015 individuals; 3/1015 membrane-like individually; rim level 0.89)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.08 (aggregate of 1015 individuals; 0/1015 membrane-like individually; rim level 0.0036)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.44, rim/outside 0.876 (aggregate of 1015 individuals; 0/1015 membrane-like individually; rim level 0.129)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 1.24 (aggregate of 1015 individuals; 0/1015 membrane-like individually; rim level 0.92)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #70 (t=10100, R_eq 6.18): none; #139 (t=10100, R_eq 6.43): none; #194 (t=10100, R_eq 6.23): none; #682 (t=11800, R_eq 6.1): none
- species `prey` (channels ['prey a'], own threshold): components final 177, mean 166.4, max 197; tracks 599, persistent 174; splits 132, persistent splits 65 (K=20), max generation 3, merges 47, merge/split 0.356; moving tracks 7
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 5.1, max 88; tracks 193, persistent 0; splits 37, persistent splits 0 (K=20), max generation 0, merges 14, merge/split 0.378; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 1015 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
