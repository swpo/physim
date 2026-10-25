# Evidence pack: physarum-growth (seed 4)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20ph/world.py --out /tmp/c20ph/growth --seeds 4 5 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 22.2154], min area 6 px

## Measurements
- components: final 6, mean 7.1, max 10; occupancy final 0.02
- tracks: 17; persistent (alive >= 50% of run): 7; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0141/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 12
- channel total drift (end/start - 1): [0.1902, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.21, heterogeneity 0.32; core [0.344, 0.855] rim [0.182, 0.528]
  - track 11 at frame 104: holes 0, rim-vs-core 0.35, rim-vs-outside 0.18, heterogeneity 0.33; core [0.342, 0.848] rim [0.217, 0.521]
  - track 13 at frame 114: holes 0, rim-vs-core 0.27, rim-vs-outside 0.40, heterogeneity 0.32; core [0.385, 0.843] rim [0.4, 0.572]
  - track 14 at frame 118: holes 0, rim-vs-core 0.30, rim-vs-outside 0.27, heterogeneity 0.33; core [0.4, 0.822] rim [0.278, 0.543]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 41 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.56, rim/outside 11.5 (aggregate of 41 individuals; 1/41 membrane-like individually; rim level 0.343)
  - radial trail: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 7.75 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.783)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=2525, R_eq 4.15): none; #11 (t=2600, R_eq 4.41): none; #13 (t=2850, R_eq 3.83): none; #14 (t=2950, R_eq 3.7): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
