# Evidence pack: physarum (seed 0)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run (c19 run) --out (c19 run) --seeds 0 1 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 83.8046], min area 6 px

## Measurements
- components: final 7, mean 6.3, max 7; occupancy final 0.02
- tracks: 13; persistent (alive >= 50% of run): 6; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00478/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 13
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.19, rim-vs-outside 0.38, heterogeneity 0.31; core [0.591, 0.927] rim [0.515, 0.756]
  - track 1 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.36, heterogeneity 0.29; core [0.708, 0.938] rim [0.417, 0.619]
  - track 2 at frame 101: holes 0, rim-vs-core 0.63, rim-vs-outside 0.20, heterogeneity 0.33; core [0.736, 0.926] rim [0.205, 0.587]
  - track 3 at frame 103: holes 0, rim-vs-core 0.34, rim-vs-outside 0.38, heterogeneity 0.25; core [0.731, 0.903] rim [0.5, 0.652]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 39 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.628, rim/outside 10.2 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.562)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 6.5 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.864)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2525, R_eq 4.22): none; #1 (t=2525, R_eq 3.66): none; #2 (t=2525, R_eq 4.3): none; #3 (t=2575, R_eq 3.09): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
