# Evidence pack: ambplus (seed 0)

- world: `../../../w/ambplus.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 97 frames x 1400 steps x dt 0.03 (--dt; world META dt 0.05) = time 4032; grid [128, 128]; wall 349s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/ambplus.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/runs/B16 --seeds 0 1 --frames 96 --spf 1400 --dt 0.03 --no-movie`
- segmentation: matter > 0.47 of robust range [-1.0363, 1.1786], min area 6 px

## Measurements
- components: final 26, mean 21.6, max 28; occupancy final 0.27
- tracks: 30; persistent (alive >= 50% of run): 26; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 840, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 28
- channel total drift (end/start - 1): [0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 57: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.16; core [0.928] rim [0.639]
  - track 1 at frame 57: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.16; core [0.927] rim [0.636]
  - track 2 at frame 57: holes 0, rim-vs-core 0.29, rim-vs-outside 0.34, heterogeneity 0.16; core [0.93] rim [0.638]
  - track 3 at frame 57: holes 0, rim-vs-core 0.28, rim-vs-outside 0.33, heterogeneity 0.16; core [0.929] rim [0.647]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 136 components >= 12 px at frames [32, 48, 64, 80, 96]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 14.7 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.872)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2394, R_eq 8.12): none; #1 (t=2394, R_eq 7.98): none; #2 (t=2394, R_eq 7.69): none; #3 (t=2394, R_eq 7.63): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
