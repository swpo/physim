# Evidence pack: kstrail (seed 7)

- world: `../../../../../../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 57s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/kst/kstrail/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9999], min area 6 px

## Measurements
- components: final 13, mean 9.3, max 16; occupancy final 0.05
- tracks: 112; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.507/time; max body lengths 11.9
- replication (lineage window K = 20 frames = time 60, default): splits 33, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 27, merge/split ratio 0.818, nucleations 20
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 66 at frame 156: holes 0, rim-vs-core 0.39, rim-vs-outside 0.34, heterogeneity 0.15; core [0.893, 0.488, 0.401] rim [0.527, 0.385, 0.302]
  - track 8 at frame 84: holes 0, rim-vs-core 0.43, rim-vs-outside 0.55, heterogeneity 0.20; core [0.955, 0.721, 0.66] rim [0.623, 0.545, 0.454]
  - track 73 at frame 165: holes 0, rim-vs-core 0.43, rim-vs-outside 0.56, heterogeneity 0.20; core [0.956, 0.729, 0.673] rim [0.626, 0.548, 0.469]
  - track 102 at frame 190: holes 0, rim-vs-core 0.47, rim-vs-outside 0.28, heterogeneity 0.17; core [0.9, 0.554, 0.497] rim [0.471, 0.429, 0.361]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 16 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.682)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 3.14 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.577)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 4.31 (aggregate of 58 individuals; 2/58 membrane-like individually; rim level 0.499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #66 (t=468, R_eq 5.26): none; #8 (t=252, R_eq 7.25): none; #73 (t=495, R_eq 7.11): none; #102 (t=570, R_eq 5.44): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
