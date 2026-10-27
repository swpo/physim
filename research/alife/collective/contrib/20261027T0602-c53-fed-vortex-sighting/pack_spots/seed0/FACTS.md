# Evidence pack: fed-vortices (seed 0)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 301 frames x 150 steps x dt 0.02 = time 900; grid [128, 128]; wall 79s; status ok
- command: `python -m labkit.run collective/contrib/c53-fv/world.py --out collective/contrib/c53-fv/pack_spots --seeds 0 1 --frames 300 --spf 150 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.1809], min area 6 px

## Measurements
- components: final 3, mean 5.1, max 49; occupancy final 0.02
- tracks: 149; persistent (alive >= 50% of run): 3; longest 301 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.201/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 60, default): splits 34, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 32, merge/split ratio 0.941, nucleations 0
- channel total drift (end/start - 1): [-0.9324, -0.0411, -1433.4861, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 45 at frame 151: holes 0, rim-vs-core 0.48, rim-vs-outside 0.79, heterogeneity 0.19; core [0.915, 0.056, 0.006, 0.863] rim [0.669, 0.233, 0.136, 0.514]
  - track 140 at frame 159: holes 0, rim-vs-core 0.69, rim-vs-outside 0.57, heterogeneity 0.19; core [0.907, 0.063, 0.009, 0.854] rim [0.558, 0.311, 0.195, 0.352]
  - track 148 at frame 161: holes 0, rim-vs-core 0.61, rim-vs-outside 0.66, heterogeneity 0.19; core [0.917, 0.052, 0.006, 0.857] rim [0.598, 0.284, 0.172, 0.417]
  - track 28 at frame 10: holes 0, rim-vs-core 0.59, rim-vs-outside 0.30, heterogeneity 0.16; core [0.829, 0.042, 0.99, 0.613] rim [0.485, 0.159, 0.854, 0.173]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 44.6 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.828)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 51.7, rim/outside 0.734 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.571)
  - radial vorticity (signed): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 47.8, rim/outside 0.865 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.468)
  - radial eating: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 83 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.82)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #45 (t=453, R_eq 6.15): none; #140 (t=477, R_eq 6.18): none; #148 (t=483, R_eq 6.21): none; #28 (t=30, R_eq 5.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
