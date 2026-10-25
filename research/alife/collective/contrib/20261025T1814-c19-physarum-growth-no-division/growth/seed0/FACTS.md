# Evidence pack: physarum-growth (seed 0)

- world: `../../world_g.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run (c19 run) --out (c19 run) --seeds 0 1 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 22.0243], min area 6 px

## Measurements
- components: final 4, mean 5.8, max 10; occupancy final 0.01
- tracks: 16; persistent (alive >= 50% of run): 6; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0243/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.2209, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.38, rim-vs-outside 0.17, heterogeneity 0.32; core [0.393, 0.876] rim [0.15, 0.583]
  - track 2 at frame 92: holes 0, rim-vs-core 0.46, rim-vs-outside 0.26, heterogeneity 0.32; core [0.5, 0.905] rim [0.129, 0.628]
  - track 12 at frame 114: holes 0, rim-vs-core 0.39, rim-vs-outside 0.28, heterogeneity 0.33; core [0.444, 0.927] rim [0.227, 0.606]
  - track 13 at frame 119: holes 0, rim-vs-core 0.47, rim-vs-outside 0.26, heterogeneity 0.34; core [0.5, 0.914] rim [0.182, 0.562]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 33 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.627, rim/outside 13 (aggregate of 33 individuals; 3/33 membrane-like individually; rim level 0.326)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 8.07 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.814)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=2525, R_eq 3.91): none; #2 (t=2300, R_eq 4.03): none; #12 (t=2850, R_eq 4.3): none; #13 (t=2975, R_eq 4.22): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
