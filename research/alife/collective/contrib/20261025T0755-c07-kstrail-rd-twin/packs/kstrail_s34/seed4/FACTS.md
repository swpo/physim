# Evidence pack: kstrail (seed 4)

- world: `../../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 55s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out /tmp/claude-0/c07/kstrail --seeds 3 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 8, mean 9.3, max 15; occupancy final 0.05
- tracks: 57; persistent (alive >= 50% of run): 4; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.40 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 8], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.588/time; max body lengths 19.1
- replication (lineage window K = 20 frames = time 60, default): splits 13, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 12, merge/split ratio 0.923, nucleations 19
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 118: holes 0, rim-vs-core 0.48, rim-vs-outside 0.53, heterogeneity 0.22; core [0.962, 0.856, 0.755] rim [0.602, 0.632, 0.525]
  - track 9 at frame 121: holes 0, rim-vs-core 0.43, rim-vs-outside 0.54, heterogeneity 0.20; core [0.958, 0.74, 0.636] rim [0.608, 0.557, 0.454]
  - track 7 at frame 106: holes 0, rim-vs-core 0.42, rim-vs-outside 0.35, heterogeneity 0.17; core [0.905, 0.577, 0.447] rim [0.514, 0.453, 0.34]
  - track 34 at frame 156: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.15; core [0.887, 0.481, 0.374] rim [0.507, 0.379, 0.281]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 22.2 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.737)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 3.69 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.639)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 5.4 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=354, R_eq 8.1): none; #9 (t=363, R_eq 7.09): none; #7 (t=318, R_eq 5.75): none; #34 (t=468, R_eq 5.11): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
