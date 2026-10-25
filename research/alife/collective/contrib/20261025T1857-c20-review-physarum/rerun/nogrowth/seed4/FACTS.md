# Evidence pack: physarum-growth (seed 4)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run /tmp/c20ph/world.py --out /tmp/c20ph/nogrowth --seeds 4 5 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 91.8522], min area 6 px

## Measurements
- components: final 6, mean 5.6, max 7; occupancy final 0.02
- tracks: 26; persistent (alive >= 50% of run): 5; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 5], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00652/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 26
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.55, rim-vs-outside 0.18, heterogeneity 0.30; core [0.7, 0.915] rim [0.25, 0.607]
  - track 1 at frame 103: holes 0, rim-vs-core 0.45, rim-vs-outside 0.24, heterogeneity 0.31; core [0.636, 0.933] rim [0.34, 0.594]
  - track 2 at frame 103: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.28; core [0.684, 0.942] rim [0.528, 0.661]
  - track 4 at frame 103: holes 0, rim-vs-core 0.55, rim-vs-outside 0.23, heterogeneity 0.29; core [0.78, 0.952] rim [0.325, 0.647]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.666, rim/outside 10.4 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.613)
  - radial trail: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 6.79 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.889)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2525, R_eq 3.99): none; #1 (t=2575, R_eq 4.69): none; #2 (t=2575, R_eq 3.43): none; #4 (t=2575, R_eq 3.78): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
