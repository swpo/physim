# Evidence pack: kstrail (seed 8)

- world: `../../../../../../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 57s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/kst/kstrail/seed8 --seeds 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 4, mean 8.0, max 16; occupancy final 0.05
- tracks: 68; persistent (alive >= 50% of run): 1; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.502/time; max body lengths 13.0
- replication (lineage window K = 20 frames = time 60, default): splits 15, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 21, merge/split ratio 1.4, nucleations 17
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 121: holes 0, rim-vs-core 0.38, rim-vs-outside 0.52, heterogeneity 0.17; core [0.949, 0.573, 0.554] rim [0.619, 0.441, 0.419]
  - track 23 at frame 103: holes 0, rim-vs-core 0.39, rim-vs-outside 0.53, heterogeneity 0.17; core [0.953, 0.616, 0.615] rim [0.631, 0.474, 0.45]
  - track 12 at frame 87: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.15; core [0.892, 0.451, 0.405] rim [0.52, 0.352, 0.289]
  - track 63 at frame 185: holes 0, rim-vs-core 0.45, rim-vs-outside 0.86, heterogeneity 0.18; core [0.995, 0.986, 0.991] rim [0.728, 0.747, 0.716]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 21.2 (aggregate of 44 individuals; 2/44 membrane-like individually; rim level 0.724)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.58 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.508)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 5.24 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.471)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=363, R_eq 7.05): none; #23 (t=309, R_eq 7.09): none; #12 (t=261, R_eq 5.92): none; #63 (t=555, R_eq 14.21): none

## Warnings
- radial: 2 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
