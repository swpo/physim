# Evidence pack: condensate-food-chain (seed 6)

- world: `../../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 51 frames x 200 steps x dt 0.5 = time 5000; grid [384, 384]; wall 575s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/20261026T0720-c34-review-arena-negative/rerun384/seed6 --seeds 6 --size 384 384 --frames 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0102, 1.2773], min area 7 px

## Measurements
- components: final 392, mean 362.4, max 451; occupancy final 0.31
- tracks: 1580; persistent (alive >= 50% of run): 297; longest 51 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 37.14 (1 = constant size)
- enclosures: components with a hole mean 0.53, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [401, 395, 392], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00761/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 389, persistent splits 75 (0 more failed only because the siblings re-merged within K), max generation 2, merges 153, merge/split ratio 0.393, nucleations 70
- channel total drift (end/start - 1): [0.3095, -0.994, -0.7318, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 57 at frame 25: holes 0, rim-vs-core 0.32, rim-vs-outside 0.51, heterogeneity 0.06; core [0.945, 0.0, 0.03, 0.967] rim [0.636, 0.0, 0.081, 0.919]
  - track 99 at frame 25: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.06; core [0.938, 0.0, 0.025, 0.981] rim [0.655, 0.0, 0.082, 0.927]
  - track 102 at frame 25: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.06; core [0.906, 0.0, 0.044, 0.959] rim [0.548, 0.0, 0.088, 0.92]
  - track 1434 at frame 38: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.06; core [0.938, 0.0, 0.027, 0.976] rim [0.644, 0.0, 0.083, 0.923]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2138 components >= 14 px at frames [8, 17, 25, 33, 42, 50]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 11.9 (aggregate of 2138 individuals; 14/2138 membrane-like individually; rim level 0.822)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.53 (aggregate of 2138 individuals; 12/2138 membrane-like individually; rim level 0.0315)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 4.31, rim/outside 0.878 (aggregate of 2138 individuals; 0/2138 membrane-like individually; rim level 0.144)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 1.12 (aggregate of 2138 individuals; 0/2138 membrane-like individually; rim level 0.931)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #57 (t=2500, R_eq 6.21): none; #99 (t=2500, R_eq 6.75): none; #102 (t=2500, R_eq 5.61): none; #1434 (t=3800, R_eq 6.68): none
- species `prey` (channels ['prey a'], own threshold): components final 392, mean 345.0, max 431; tracks 1268, persistent 296; splits 283, persistent splits 75 (K=20), max generation 2, merges 94, merge/split 0.332; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 34.3, max 172; tracks 375, persistent 0; splits 76, persistent splits 0 (K=20), max generation 0, merges 23, merge/split 0.303; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 2138 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
