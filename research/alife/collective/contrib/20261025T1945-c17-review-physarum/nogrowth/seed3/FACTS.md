# Evidence pack: physarum-growth (seed 3)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run world.py --out nogrowth --seeds 2 3 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 105.6952], min area 6 px

## Measurements
- components: final 5, mean 4.8, max 5; occupancy final 0.02
- tracks: 11; persistent (alive >= 50% of run): 5; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 4], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00303/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 103: holes 0, rim-vs-core 0.53, rim-vs-outside 0.21, heterogeneity 0.30; core [0.734, 0.943] rim [0.31, 0.631]
  - track 5 at frame 104: holes 0, rim-vs-core 0.44, rim-vs-outside 0.24, heterogeneity 0.29; core [0.713, 0.946] rim [0.42, 0.618]
  - track 6 at frame 104: holes 0, rim-vs-core 0.42, rim-vs-outside 0.21, heterogeneity 0.28; core [0.727, 0.946] rim [0.432, 0.643]
  - track 9 at frame 111: holes 0, rim-vs-core 0.42, rim-vs-outside 0.24, heterogeneity 0.30; core [0.649, 0.936] rim [0.364, 0.625]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.631, rim/outside 10.1 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.61)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 7.07 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.909)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=2575, R_eq 4.11): none; #5 (t=2600, R_eq 4.79): none; #6 (t=2600, R_eq 4.18): none; #9 (t=2775, R_eq 4.33): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
