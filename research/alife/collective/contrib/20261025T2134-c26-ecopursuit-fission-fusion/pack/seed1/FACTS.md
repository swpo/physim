# Evidence pack: eco-pursuit (seed 1)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 345s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8991], min area 6 px

## Measurements
- components: final 30, mean 30.8, max 40; occupancy final 0.07
- tracks: 2911; persistent (alive >= 50% of run): 0; longest 23 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 33, 21], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.287/time; max body lengths 8.6
- replication (lineage window K = 20 frames = time 240, default): splits 67, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 75, merge/split ratio 1.12, nucleations 2700
- channel total drift (end/start - 1): [None, 0.4193, 0.8251, -0.0965]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1967 at frame 148: holes 0, rim-vs-core 0.44, rim-vs-outside 0.51, heterogeneity 0.30; core [0.095, 0.568, 0.848, 0.086] rim [0.144, 0.534, 0.444, 0.263]
  - track 2148 at frame 161: holes 0, rim-vs-core 0.32, rim-vs-outside 0.27, heterogeneity 0.23; core [0.06, 0.527, 0.594, 0.293] rim [0.071, 0.609, 0.293, 0.374]
  - track 1959 at frame 148: holes 0, rim-vs-core 0.38, rim-vs-outside 0.28, heterogeneity 0.32; core [0.322, 0.577, 0.718, 0.148] rim [0.356, 0.516, 0.381, 0.308]
  - track 361 at frame 35: holes 0, rim-vs-core 0.58, rim-vs-outside 0.57, heterogeneity 0.32; core [0.24, 0.602, 0.892, 0.147] rim [0.373, 0.708, 0.34, 0.233]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 179 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 4.6 (aggregate of 179 individuals; 24/179 membrane-like individually; rim level 0.229)
  - radial preyB: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 6.5 (aggregate of 179 individuals; 25/179 membrane-like individually; rim level 0.589)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.597, rim/outside 9.9 (aggregate of 179 individuals; 9/179 membrane-like individually; rim level 0.418)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.25, rim/outside 0.742 (aggregate of 179 individuals; 0/179 membrane-like individually; rim level 0.538)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1967 (t=1776, R_eq 6.56): none; #2148 (t=1932, R_eq 5.26): ['preyA', 'preyB']; #1959 (t=1776, R_eq 5.86): none; #361 (t=420, R_eq 6.77): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 31, mean 32.7, max 41; tracks 2558, persistent 0; splits 78, persistent splits 0 (K=20), max generation 0, merges 89, merge/split 1.14; moving tracks 3
- species `predator` (channels ['predator'], own threshold): components final 28, mean 24.7, max 34; tracks 2917, persistent 0; splits 8, persistent splits 0 (K=20), max generation 0, merges 31, merge/split 3.88; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 179 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
