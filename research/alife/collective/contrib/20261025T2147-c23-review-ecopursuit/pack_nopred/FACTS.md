# Evidence pack: eco-pursuit (seed 3)

- world: `../../../20261025T2134-c26-ecopursuit-fission-fusion/world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 306s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2134-c26-ecopursuit-fission-fusion/world.py --out collective/contrib/20261025T2147-c23-review-ecopursuit/pack_nopred --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9932], min area 6 px

## Measurements
- components: final 5, mean 8.6, max 29; occupancy final 0.02
- tracks: 115; persistent (alive >= 50% of run): 3; longest 180 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.72 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.283/time; max body lengths 58.9
- replication (lineage window K = 20 frames = time 240, default): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 36, merge/split ratio 2, nucleations 45
- channel total drift (end/start - 1): [None, -0.7295, None, -0.0165]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 111: holes 0, rim-vs-core 0.48, rim-vs-outside 0.46, heterogeneity 0.10; core [0.013, 0.961, 0.0, 0.07] rim [0.011, 0.548, 0.0, 0.308]
  - track 82 at frame 118: holes 0, rim-vs-core 0.53, rim-vs-outside 0.73, heterogeneity 0.14; core [0.999, 0.96, 0.0, 0.076] rim [0.761, 0.547, 0.0, 0.318]
  - track 87 at frame 123: holes 0, rim-vs-core 0.48, rim-vs-outside 0.74, heterogeneity 0.13; core [0.99, 0.964, 0.0, 0.066] rim [0.76, 0.612, 0.0, 0.291]
  - track 112 at frame 151: holes 0, rim-vs-core 0.51, rim-vs-outside 0.74, heterogeneity 0.13; core [1.0, 0.955, 0.0, 0.07] rim [0.887, 0.519, 0.0, 0.31]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial preyA: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 22.8 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.439)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 45.6 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.77)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 44 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.1, rim/outside 0.71 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.598)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #61 (t=1332, R_eq 5.01): none; #82 (t=1416, R_eq 5.01): none; #87 (t=1476, R_eq 4.79): none; #112 (t=1812, R_eq 5.05): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 5, mean 8.6, max 29; tracks 115, persistent 3; splits 18, persistent splits 0 (K=20), max generation 0, merges 36, merge/split 2; moving tracks 23
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
