# Evidence pack: eco-pursuit (seed 1)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 318s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack_food --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8555], min area 6 px

## Measurements
- components: final 0, mean 19.4, max 39; occupancy final 0.00
- tracks: 1883; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 240, default): splits 37, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 58, merge/split ratio 1.57, nucleations 1750
- channel total drift (end/start - 1): [None, -0.9526, -0.7422, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 358 at frame 35: holes 0, rim-vs-core 0.60, rim-vs-outside 0.56, heterogeneity 0.30; core [0.215, 0.61, 0.902, 0.591] rim [0.357, 0.724, 0.332, 0.634]
  - track 876 at frame 69: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.27; core [0.242, 0.775, 0.568, 0.475] rim [0.13, 0.419, 0.519, 0.612]
  - track 856 at frame 66: holes 0, rim-vs-core 0.45, rim-vs-outside 0.48, heterogeneity 0.27; core [0.148, 0.509, 0.867, 0.554] rim [0.153, 0.572, 0.432, 0.643]
  - track 1463 at frame 109: holes 0, rim-vs-core 0.73, rim-vs-outside 0.58, heterogeneity 0.30; core [0.161, 0.28, 0.892, 0.626] rim [0.427, 0.704, 0.364, 0.603]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [34, 67, 101, 133]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 3.74 (aggregate of 98 individuals; 14/98 membrane-like individually; rim level 0.194)
  - radial preyB: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 6.6 (aggregate of 98 individuals; 14/98 membrane-like individually; rim level 0.56)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.613, rim/outside 8.68 (aggregate of 98 individuals; 3/98 membrane-like individually; rim level 0.443)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.91 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.749)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #358 (t=420, R_eq 6.86): none; #876 (t=828, R_eq 5.61): none; #856 (t=792, R_eq 6.1): none; #1463 (t=1308, R_eq 6.13): ['preyA', 'preyB']
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 0, mean 20.8, max 41; tracks 1697, persistent 0; splits 42, persistent splits 0 (K=20), max generation 0, merges 54, merge/split 1.29; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 0, mean 15.7, max 32; tracks 1867, persistent 0; splits 6, persistent splits 0 (K=20), max generation 0, merges 18, merge/split 3; moving tracks 4

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
