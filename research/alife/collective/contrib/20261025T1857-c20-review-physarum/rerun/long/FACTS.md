# Evidence pack: physarum-growth (seed 4)

- world: `../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run /tmp/c20ph/world.py --out /tmp/c20ph/long --seeds 4 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 21.5126], min area 6 px

## Measurements
- components: final 4, mean 5.6, max 10; occupancy final 0.01
- tracks: 16; persistent (alive >= 50% of run): 5; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.21 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00325/time; max body lengths 8.3
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 16
- channel total drift (end/start - 1): [-0.2025, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.24, heterogeneity 0.34; core [0.5, 0.907] rim [0.136, 0.552]
  - track 4 at frame 99: holes 0, rim-vs-core 0.40, rim-vs-outside 0.17, heterogeneity 0.33; core [0.406, 0.875] rim [0.182, 0.545]
  - track 13 at frame 106: holes 0, rim-vs-core 0.37, rim-vs-outside 0.20, heterogeneity 0.32; core [0.378, 0.852] rim [0.182, 0.54]
  - track 11 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.20, heterogeneity 0.33; core [0.516, 0.893] rim [0.048, 0.571]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.441, rim/outside 10.4 (aggregate of 32 individuals; 2/32 membrane-like individually; rim level 0.264)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 8.48 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.829)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=10100, R_eq 4.22): none; #4 (t=9900, R_eq 4.15): none; #13 (t=10600, R_eq 4.33): none; #11 (t=10100, R_eq 4.07): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
