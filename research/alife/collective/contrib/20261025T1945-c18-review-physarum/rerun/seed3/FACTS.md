# Evidence pack: physarum-growth (seed 3)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev16/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev16/growth --seeds 3 4 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 22.4109], min area 6 px

## Measurements
- components: final 6, mean 7.9, max 11; occupancy final 0.02
- tracks: 20; persistent (alive >= 50% of run): 8; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0246/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 15
- channel total drift (end/start - 1): [0.1656, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 103: holes 0, rim-vs-core 0.53, rim-vs-outside 0.19, heterogeneity 0.34; core [0.5, 0.884] rim [0.095, 0.545]
  - track 8 at frame 103: holes 0, rim-vs-core 0.50, rim-vs-outside 0.19, heterogeneity 0.35; core [0.567, 0.871] rim [0.2, 0.524]
  - track 14 at frame 106: holes 0, rim-vs-core 0.40, rim-vs-outside 0.16, heterogeneity 0.31; core [0.387, 0.8] rim [0.095, 0.526]
  - track 15 at frame 97: holes 0, rim-vs-core 0.35, rim-vs-outside 0.17, heterogeneity 0.32; core [0.345, 0.842] rim [0.19, 0.533]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.469, rim/outside 10.3 (aggregate of 46 individuals; 1/46 membrane-like individually; rim level 0.313)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 7.71 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.762)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=2575, R_eq 4.18): none; #8 (t=2575, R_eq 3.99): none; #14 (t=2650, R_eq 4.07): none; #15 (t=2425, R_eq 3.99): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
