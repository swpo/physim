# Evidence pack: eco-pursuit (seed 0)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 390s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack_preyrm --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8481], min area 6 px

## Measurements
- components: final 0, mean 18.5, max 40; occupancy final 0.00
- tracks: 1659; persistent (alive >= 50% of run): 0; longest 16 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 240, default): splits 42, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 42, merge/split ratio 1, nucleations 1533
- channel total drift (end/start - 1): [None, -0.9887, -0.7346, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 670 at frame 59: holes 0, rim-vs-core 0.39, rim-vs-outside 0.56, heterogeneity 0.32; core [0.299, 0.609, 0.883, 0.029] rim [0.272, 0.518, 0.515, 0.109]
  - track 914 at frame 77: holes 0, rim-vs-core 0.51, rim-vs-outside 0.65, heterogeneity 0.26; core [0.035, 0.436, 0.918, 0.196] rim [0.09, 0.671, 0.469, 0.215]
  - track 706 at frame 61: holes 0, rim-vs-core 0.23, rim-vs-outside 0.53, heterogeneity 0.30; core [0.149, 0.56, 0.701, 0.038] rim [0.127, 0.461, 0.545, 0.168]
  - track 1081 at frame 91: holes 0, rim-vs-core 0.37, rim-vs-outside 0.66, heterogeneity 0.25; core [0.17, 0.731, 0.707, 0.031] rim [0.127, 0.724, 0.365, 0.165]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [34, 67, 101, 133]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 4.97 (aggregate of 90 individuals; 5/90 membrane-like individually; rim level 0.195)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 6.82 (aggregate of 90 individuals; 8/90 membrane-like individually; rim level 0.574)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.585, rim/outside 11.1 (aggregate of 90 individuals; 2/90 membrane-like individually; rim level 0.425)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.14, rim/outside 0.715 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.507)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #670 (t=708, R_eq 6.98): none; #914 (t=924, R_eq 7.02): ['preyB']; #706 (t=732, R_eq 6.53): none; #1081 (t=1092, R_eq 7.94, ring): ['preyA', 'preyB', 'predator']
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 0, mean 19.6, max 40; tracks 1495, persistent 0; splits 50, persistent splits 0 (K=20), max generation 0, merges 61, merge/split 1.22; moving tracks 1
- species `predator` (channels ['predator'], own threshold): components final 0, mean 14.7, max 32; tracks 1702, persistent 0; splits 3, persistent splits 0 (K=20), max generation 0, merges 16, merge/split 5.33; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
