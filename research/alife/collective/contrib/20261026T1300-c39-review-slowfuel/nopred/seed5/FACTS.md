# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T1240-c42-slowfuel-standing-ecology/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 98s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1240-c42-slowfuel-standing-ecology/world.py --out collective/contrib/c39-rev-slow-wip/nopred/seed5 --seeds 5 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0447, 1.0795], min area 6 px

## Measurements
- components: final 103, mean 101.2, max 103; occupancy final 0.27
- tracks: 183; persistent (alive >= 50% of run): 103; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 5.11 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [103, 103, 103], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000745/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 28, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.321, nucleations 4
- channel total drift (end/start - 1): [0.0581, None, -0.6029, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 61: holes 0, rim-vs-core 0.43, rim-vs-outside 0.30, heterogeneity 0.09; core [0.865, 0.0, 0.066, 0.9] rim [0.472, 0.0, 0.176, 0.767]
  - track 28 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.09; core [0.873, 0.0, 0.057, 0.917] rim [0.499, 0.0, 0.174, 0.771]
  - track 52 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.08; core [0.878, 0.0, 0.061, 0.905] rim [0.513, 0.0, 0.167, 0.778]
  - track 175 at frame 65: holes 0, rim-vs-core 0.24, rim-vs-outside 0.47, heterogeneity 0.08; core [0.888, 0.0, 0.061, 0.903] rim [0.668, 0.0, 0.123, 0.832]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 616 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 30.9 (aggregate of 616 individuals; 0/616 membrane-like individually; rim level 0.792)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 616 individuals)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 14.4, rim/outside 0.816 (aggregate of 616 individuals; 0/616 membrane-like individually; rim level 0.274)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 1.56 (aggregate of 616 individuals; 0/616 membrane-like individually; rim level 0.862)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=6100, R_eq 3.74): none; #28 (t=6100, R_eq 3.91): none; #52 (t=6100, R_eq 3.66): none; #175 (t=6500, R_eq 3.48): none
- species `prey` (channels ['prey a'], own threshold): components final 103, mean 101.2, max 103; tracks 183, persistent 103; splits 28, persistent splits 4 (K=20), max generation 1, merges 9, merge/split 0.321; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
