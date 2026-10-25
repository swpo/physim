# Evidence pack: physarum (seed 0)

- world: `../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run (c19 run, WORLD_P SA 120 RA 45 frac 0.05).py --out (c19 run, WORLD_P SA 120 RA 45 frac 0.05) --seeds 0 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 5.0], min area 6 px

## Measurements
- components: final 5, mean 4.1, max 7; occupancy final 0.01
- tracks: 64; persistent (alive >= 50% of run): 3; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00707/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 64
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.04, rim-vs-outside 0.50, heterogeneity 0.06; core [1.0, 1.0] rim [0.958, 1.0]
  - track 9 at frame 124: holes 0, rim-vs-core 0.23, rim-vs-outside 0.43, heterogeneity 0.13; core [1.0, 1.0] rim [0.769, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 4.4 (aggregate of 21 individuals; 2/21 membrane-like individually; rim level 0.955)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.09 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2600, R_eq 2.46): none; #7 (t=3075, R_eq 2.46): none; #9 (t=3100, R_eq 2.76): none; #30 (t=3650, R_eq 2.33): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
