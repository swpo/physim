# Evidence pack: condensate-food-chain (seed 5)

- world: `../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 569s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/wip-c33-fc/rerun_nopred --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.217], min area 6 px

## Measurements
- components: final 223, mean 222.9, max 241; occupancy final 0.32
- tracks: 495; persistent (alive >= 50% of run): 223; longest 101 frames; alive start-to-end: 28
- size of persistent tracks: max/min area ratio 26.71 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [223, 223, 223], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000889/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 69, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 43, merge/split ratio 0.623, nucleations 30
- channel total drift (end/start - 1): [0.2797, None, -0.7383, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.22, rim-vs-outside 0.49, heterogeneity 0.08; core [0.879, 0.0, 0.038, 0.887] rim [0.671, 0.0, 0.057, 0.827]
  - track 6 at frame 50: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.08; core [0.889, 0.0, 0.035, 0.893] rim [0.484, 0.0, 0.078, 0.76]
  - track 15 at frame 50: holes 0, rim-vs-core 0.34, rim-vs-outside 0.33, heterogeneity 0.06; core [0.906, 0.0, 0.041, 0.87] rim [0.58, 0.0, 0.073, 0.774]
  - track 493 at frame 54: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.07; core [0.9, 0.0, 0.034, 0.895] rim [0.536, 0.0, 0.075, 0.77]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1338 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 20.7 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.881)
  - radial predator b: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.222 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.0006)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.11, rim/outside 0.887 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.112)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 1.48 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.866)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5000, R_eq 5.53): none; #6 (t=5000, R_eq 5.56): none; #15 (t=5000, R_eq 4.69): none; #493 (t=5400, R_eq 5.35): none
- species `prey` (channels ['prey a'], own threshold): components final 223, mean 222.9, max 241; tracks 494, persistent 223; splits 69, persistent splits 1 (K=20), max generation 1, merges 43, merge/split 0.623; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 4.5, max 146; tracks 315, persistent 0; splits 79, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 0.051; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
