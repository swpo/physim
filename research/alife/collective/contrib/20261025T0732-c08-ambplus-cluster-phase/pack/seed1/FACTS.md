# Evidence pack: ambplus (seed 1)

- world: `../../../w/ambplus.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 97 frames x 1400 steps x dt 0.03 (--dt; world META dt 0.05) = time 4032; grid [128, 128]; wall 358s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/ambplus.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/runs/B16 --seeds 0 1 --frames 96 --spf 1400 --dt 0.03 --no-movie`
- segmentation: matter > 0.47 of robust range [-1.0359, 1.1792], min area 6 px

## Measurements
- components: final 27, mean 21.3, max 27; occupancy final 0.27
- tracks: 27; persistent (alive >= 50% of run): 27; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 27, 27], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 840, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 27
- channel total drift (end/start - 1): [0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 57: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.16; core [0.928] rim [0.636]
  - track 1 at frame 57: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.16; core [0.929] rim [0.637]
  - track 2 at frame 57: holes 0, rim-vs-core 0.16, rim-vs-outside 0.46, heterogeneity 0.16; core [0.921] rim [0.764]
  - track 3 at frame 58: holes 0, rim-vs-core 0.28, rim-vs-outside 0.33, heterogeneity 0.16; core [0.929] rim [0.648]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [32, 48, 64, 80, 96]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 15.8 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.876)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2394, R_eq 8.5): none; #1 (t=2394, R_eq 7.88): none; #2 (t=2394, R_eq 8.35): none; #3 (t=2436, R_eq 7.48): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
