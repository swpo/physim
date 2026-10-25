# Evidence pack: physarum-growth (seed 1)

- world: `../../world_g.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run (c19 run) --out (c19 run) --seeds 0 1 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 22.2379], min area 6 px

## Measurements
- components: final 6, mean 7.1, max 10; occupancy final 0.02
- tracks: 13; persistent (alive >= 50% of run): 7; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.90 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0197/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [0.1779, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.20, heterogeneity 0.34; core [0.517, 0.896] rim [0.095, 0.561]
  - track 2 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.20, heterogeneity 0.34; core [0.533, 0.906] rim [0.15, 0.58]
  - track 5 at frame 103: holes 0, rim-vs-core 0.46, rim-vs-outside 0.18, heterogeneity 0.33; core [0.471, 0.864] rim [0.143, 0.539]
  - track 9 at frame 103: holes 0, rim-vs-core 0.35, rim-vs-outside 0.28, heterogeneity 0.33; core [0.364, 0.856] rim [0.273, 0.522]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 41 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.508, rim/outside 10.8 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.3)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 7.99 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.795)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2525, R_eq 3.99): none; #2 (t=2525, R_eq 3.99): none; #5 (t=2575, R_eq 4.18): none; #9 (t=2575, R_eq 4.18): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
