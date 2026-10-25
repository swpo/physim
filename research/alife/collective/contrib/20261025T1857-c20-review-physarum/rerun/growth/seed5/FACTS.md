# Evidence pack: physarum-growth (seed 5)

- world: `../../world.py`, family `physarum-agents`
- parent: None; mutation: new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail
- run: 201 frames x 25 steps x dt 1.0 = time 5000; grid [128, 128]; wall 11s; status ok
- command: `python -m labkit.run /tmp/c20ph/world.py --out /tmp/c20ph/growth --seeds 4 5 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 22.4126], min area 6 px

## Measurements
- components: final 7, mean 7.4, max 12; occupancy final 0.02
- tracks: 19; persistent (alive >= 50% of run): 7; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0142/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 500, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio n/a, nucleations 16
- channel total drift (end/start - 1): [0.3926, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 103: holes 0, rim-vs-core 0.44, rim-vs-outside 0.18, heterogeneity 0.33; core [0.419, 0.846] rim [0.15, 0.504]
  - track 11 at frame 103: holes 0, rim-vs-core 0.56, rim-vs-outside 0.19, heterogeneity 0.33; core [0.455, 0.91] rim [0.045, 0.534]
  - track 12 at frame 103: holes 0, rim-vs-core 0.50, rim-vs-outside 0.21, heterogeneity 0.34; core [0.5, 0.911] rim [0.143, 0.568]
  - track 15 at frame 104: holes 0, rim-vs-core 0.48, rim-vs-outside 0.16, heterogeneity 0.32; core [0.5, 0.831] rim [0.105, 0.554]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.558, rim/outside 10.8 (aggregate of 43 individuals; 1/43 membrane-like individually; rim level 0.302)
  - radial trail: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 8.09 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.805)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=2575, R_eq 4.03): none; #11 (t=2575, R_eq 4.18): none; #12 (t=2575, R_eq 4.03): ['agent density']; #15 (t=2600, R_eq 3.78): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
