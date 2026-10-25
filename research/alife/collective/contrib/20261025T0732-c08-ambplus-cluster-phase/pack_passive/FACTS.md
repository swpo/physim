# Evidence pack: ambplus (seed 0)

- world: `../../w/ambplus.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 101 frames x 800 steps x dt 0.05 = time 4000; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/ambplus.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/runs/P_p04 --seeds 0 --frames 100 --spf 800 --no-movie`
- segmentation: matter > 0.48 of robust range [-0.9411, 1.028], min area 6 px

## Measurements
- components: final 16, mean 16.3, max 27; occupancy final 0.26
- tracks: 30; persistent (alive >= 50% of run): 19; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 48.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 800, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio n/a, nucleations 27
- channel total drift (end/start - 1): [0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 60: holes 0, rim-vs-core 0.28, rim-vs-outside 0.29, heterogeneity 0.16; core [0.919] rim [0.635]
  - track 1 at frame 60: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.16; core [0.918] rim [0.629]
  - track 2 at frame 60: holes 0, rim-vs-core 0.28, rim-vs-outside 0.29, heterogeneity 0.16; core [0.902] rim [0.622]
  - track 3 at frame 60: holes 0, rim-vs-core 0.30, rim-vs-outside 0.29, heterogeneity 0.16; core [0.924] rim [0.622]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 12.8 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.837)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2400, R_eq 8.67): none; #1 (t=2400, R_eq 8.56): none; #2 (t=2400, R_eq 7.51): none; #3 (t=2400, R_eq 9.52): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
