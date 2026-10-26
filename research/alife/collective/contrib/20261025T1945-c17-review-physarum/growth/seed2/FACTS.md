# Evidence pack: physarum-growth (seed 2)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run world.py --out growth --seeds 2 3 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 22.2714], min area 6 px

## Measurements
- components: final 5, mean 6.8, max 9; occupancy final 0.02
- tracks: 15; persistent (alive >= 50% of run): 7; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0124/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 10
- channel total drift (end/start - 1): [-0.0429, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.37, heterogeneity 0.33; core [0.391, 0.897] rim [0.257, 0.689]
  - track 10 at frame 104: holes 0, rim-vs-core 0.31, rim-vs-outside 0.28, heterogeneity 0.33; core [0.361, 0.825] rim [0.273, 0.531]
  - track 0 at frame 77: holes 0, rim-vs-core 0.49, rim-vs-outside 0.21, heterogeneity 0.31; core [0.406, 0.88] rim [0.043, 0.551]
  - track 12 at frame 133: holes 0, rim-vs-core 0.47, rim-vs-outside 0.17, heterogeneity 0.34; core [0.457, 0.885] rim [0.143, 0.541]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.512, rim/outside 10.5 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.284)
  - radial trail: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 7.93 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.796)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=2525, R_eq 4.3): none; #10 (t=2600, R_eq 4.3): none; #0 (t=1925, R_eq 4.18): none; #12 (t=3325, R_eq 4.22): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
