# Evidence pack: condensate-food-chain (seed 6)

- world: `../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [384, 384]; wall 1315s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/wip-c33-fca/pack384 --seeds 6 --size 384 384 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2479], min area 7 px

## Measurements
- components: final 406, mean 382.0, max 471; occupancy final 0.31
- tracks: 1606; persistent (alive >= 50% of run): 387; longest 101 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 24.14 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [406, 406, 406], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00761/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 392, persistent splits 131 (0 more failed only because the siblings re-merged within K), max generation 4, merges 154, merge/split ratio 0.393, nucleations 62
- channel total drift (end/start - 1): [0.3125, -0.9997, -0.7333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.51, heterogeneity 0.07; core [0.954, 0.0, 0.025, 0.959] rim [0.635, 0.0, 0.076, 0.887]
  - track 75 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.51, heterogeneity 0.07; core [0.954, 0.0, 0.025, 0.961] rim [0.641, 0.0, 0.076, 0.888]
  - track 107 at frame 50: holes 0, rim-vs-core 0.30, rim-vs-outside 0.53, heterogeneity 0.06; core [0.955, 0.0, 0.023, 0.967] rim [0.664, 0.0, 0.075, 0.894]
  - track 1590 at frame 82: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.898, 0.0, 0.044, 0.931] rim [0.506, 0.0, 0.085, 0.877]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2275 components >= 14 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 17.2 (aggregate of 2275 individuals; 4/2275 membrane-like individually; rim level 0.874)
  - radial predator b: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.1 (aggregate of 2275 individuals; 3/2275 membrane-like individually; rim level 0.0066)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.75, rim/outside 0.876 (aggregate of 2275 individuals; 0/2275 membrane-like individually; rim level 0.131)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 1.2 (aggregate of 2275 individuals; 0/2275 membrane-like individually; rim level 0.925)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=5000, R_eq 6.13): none; #75 (t=5000, R_eq 6.18): none; #107 (t=5000, R_eq 6.23): none; #1590 (t=8200, R_eq 5.41): none
- species `prey` (channels ['prey a'], own threshold): components final 406, mean 373.0, max 429; tracks 1310, persistent 387; splits 302, persistent splits 131 (K=20), max generation 4, merges 98, merge/split 0.325; moving tracks 6
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 18.0, max 172; tracks 380, persistent 0; splits 81, persistent splits 0 (K=20), max generation 0, merges 23, merge/split 0.284; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 2275 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
