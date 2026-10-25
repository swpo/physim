# Evidence pack: kstrail (seed 3)

- world: `../../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 67s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out /tmp/claude-0/c07/kstrail --seeds 3 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9999], min area 6 px

## Measurements
- components: final 12, mean 9.2, max 14; occupancy final 0.06
- tracks: 75; persistent (alive >= 50% of run): 2; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.553/time; max body lengths 31.6
- replication (lineage window K = 20 frames = time 60, default): splits 19, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 3, merges 20, merge/split ratio 1.05, nucleations 16
- channel total drift (end/start - 1): [-0.0003, -0.0003, -0.0003]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 139: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.10; core [0.807, 0.308, 0.217] rim [0.498, 0.257, 0.171]
  - track 13 at frame 99: holes 0, rim-vs-core 0.48, rim-vs-outside 0.53, heterogeneity 0.21; core [0.958, 0.793, 0.73] rim [0.603, 0.584, 0.493]
  - track 35 at frame 145: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.16; core [0.897, 0.497, 0.404] rim [0.506, 0.388, 0.3]
  - track 50 at frame 138: holes 0, rim-vs-core 0.40, rim-vs-outside 0.56, heterogeneity 0.20; core [0.958, 0.746, 0.66] rim [0.64, 0.566, 0.486]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 19.1 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.696)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 3.33 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.574)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.52 (aggregate of 57 individuals; 1/57 membrane-like individually; rim level 0.488)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=417, R_eq 3.87): none; #13 (t=297, R_eq 8.04): none; #35 (t=435, R_eq 5.47): none; #50 (t=414, R_eq 7.57): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
