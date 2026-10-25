# Evidence pack: kstrail (seed 9)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 60s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out /tmp/claude-0/c11rev7/kstrail --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9997], min area 6 px

## Measurements
- components: final 11, mean 10.6, max 17; occupancy final 0.06
- tracks: 88; persistent (alive >= 50% of run): 1; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.26 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 11], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.544/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 60, default): splits 24, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 20, merge/split ratio 0.833, nucleations 22
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 148: holes 0, rim-vs-core 0.40, rim-vs-outside 0.55, heterogeneity 0.19; core [0.968, 0.716, 0.62] rim [0.638, 0.551, 0.469]
  - track 8 at frame 79: holes 0, rim-vs-core 0.38, rim-vs-outside 0.55, heterogeneity 0.18; core [0.953, 0.674, 0.56] rim [0.63, 0.525, 0.424]
  - track 54 at frame 160: holes 0, rim-vs-core 0.39, rim-vs-outside 0.54, heterogeneity 0.19; core [0.96, 0.699, 0.567] rim [0.626, 0.551, 0.439]
  - track 66 at frame 171: holes 0, rim-vs-core 0.44, rim-vs-outside 0.55, heterogeneity 0.21; core [0.958, 0.786, 0.7] rim [0.618, 0.592, 0.493]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 12.5 (aggregate of 70 individuals; 1/70 membrane-like individually; rim level 0.66)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 2.96 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.575)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 4.01 (aggregate of 70 individuals; 1/70 membrane-like individually; rim level 0.485)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #44 (t=444, R_eq 6.46): none; #8 (t=237, R_eq 6.43): none; #54 (t=480, R_eq 6.21): none; #66 (t=513, R_eq 7.46): none

## Warnings
- radial: 1 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
