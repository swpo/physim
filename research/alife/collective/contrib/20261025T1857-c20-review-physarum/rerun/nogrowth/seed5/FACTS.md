# Evidence pack: physarum-growth (seed 5)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 7s; status ok
- command: `python -m labkit.run /tmp/c20ph/world.py --out /tmp/c20ph/nogrowth --seeds 4 5 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 111.1289], min area 6 px

## Measurements
- components: final 4, mean 4.7, max 6; occupancy final 0.02
- tracks: 38; persistent (alive >= 50% of run): 5; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 4], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00396/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 38
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 103: holes 0, rim-vs-core 0.48, rim-vs-outside 0.28, heterogeneity 0.27; core [0.772, 0.985] rim [0.38, 0.715]
  - track 8 at frame 113: holes 0, rim-vs-core 0.32, rim-vs-outside 0.43, heterogeneity 0.27; core [0.773, 0.98] rim [0.591, 0.715]
  - track 21 at frame 133: holes 0, rim-vs-core 0.56, rim-vs-outside 0.25, heterogeneity 0.29; core [0.864, 0.99] rim [0.37, 0.724]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.751, rim/outside 8.49 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.732)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 5.35 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.962)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=2575, R_eq 4.75): none; #8 (t=2825, R_eq 4.18): none; #21 (t=3325, R_eq 4.22): none; #0 (t=1675, R_eq 1.78): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
