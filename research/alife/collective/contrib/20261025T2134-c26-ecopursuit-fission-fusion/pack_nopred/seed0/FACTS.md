# Evidence pack: eco-pursuit (seed 0)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 345s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack_nopred --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9933], min area 6 px

## Measurements
- components: final 6, mean 8.6, max 27; occupancy final 0.02
- tracks: 144; persistent (alive >= 50% of run): 1; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.266/time; max body lengths 47.8
- replication (lineage window K = 20 frames = time 240, default): splits 29, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 47, merge/split ratio 1.62, nucleations 41
- channel total drift (end/start - 1): [None, -0.7114, None, -0.0176]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 123: holes 0, rim-vs-core 0.52, rim-vs-outside 0.51, heterogeneity 0.14; core [0.491, 0.958, 0.0, 0.07] rim [0.284, 0.539, 0.0, 0.306]
  - track 106 at frame 111: holes 0, rim-vs-core 0.44, rim-vs-outside 0.48, heterogeneity 0.10; core [0.0, 0.963, 0.0, 0.061] rim [0.0, 0.582, 0.0, 0.285]
  - track 124 at frame 133: holes 0, rim-vs-core 0.28, rim-vs-outside 0.65, heterogeneity 0.10; core [0.009, 0.956, 0.0, 0.077] rim [0.012, 0.715, 0.0, 0.211]
  - track 136 at frame 182: holes 0, rim-vs-core 0.52, rim-vs-outside 0.54, heterogeneity 0.15; core [0.607, 0.965, 0.0, 0.05] rim [0.386, 0.554, 0.0, 0.277]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 27.3 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.49)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 54.1 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.8)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 43 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 26.3, rim/outside 0.714 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.599)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #86 (t=1476, R_eq 5.01): none; #106 (t=1332, R_eq 4.95): none; #124 (t=1596, R_eq 4.95): none; #136 (t=2184, R_eq 5.08): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 6, mean 8.6, max 27; tracks 144, persistent 1; splits 29, persistent splits 1 (K=20), max generation 1, merges 47, merge/split 1.62; moving tracks 26
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
