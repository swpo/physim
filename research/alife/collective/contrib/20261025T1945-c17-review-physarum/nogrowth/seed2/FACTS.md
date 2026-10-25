# Evidence pack: physarum-growth (seed 2)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out nogrowth --seeds 2 3 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 99.6223], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 9; occupancy final 0.02
- tracks: 103; persistent (alive >= 50% of run): 5; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.60 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 2], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00654/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 103
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.48, rim-vs-outside 0.26, heterogeneity 0.28; core [0.669, 0.987] rim [0.293, 0.681]
  - track 2 at frame 103: holes 0, rim-vs-core 0.28, rim-vs-outside 0.52, heterogeneity 0.26; core [0.786, 0.995] rim [0.6, 0.78]
  - track 3 at frame 103: holes 0, rim-vs-core 0.30, rim-vs-outside 0.32, heterogeneity 0.23; core [0.875, 0.948] rim [0.625, 0.775]
  - track 4 at frame 103: holes 0, rim-vs-core 0.37, rim-vs-outside 0.21, heterogeneity 0.26; core [0.706, 0.973] rim [0.412, 0.752]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.751, rim/outside 8.61 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.715)
  - radial trail: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 4.68 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.951)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2525, R_eq 5.47): none; #2 (t=2575, R_eq 3.04): none; #3 (t=2575, R_eq 2.52): none; #4 (t=2575, R_eq 3.29): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
