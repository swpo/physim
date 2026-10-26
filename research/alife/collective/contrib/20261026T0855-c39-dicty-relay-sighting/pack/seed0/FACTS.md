# Evidence pack: dicty-relay (seed 0)

- world: `../../world.py`, family `excitable-chemotaxis`
- parent: None; mutation: new class: agents with FitzHugh-Nagumo relay of a diffusing signal and chemotaxis while excited
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 105s; status ok
- command: `python -m labkit.run collective/contrib/c39-dicty-wip/world.py --out collective/contrib/c39-dicty-wip/pack/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 7.1905], min area 6 px

## Measurements
- components: final 11, mean 22.6, max 112; occupancy final 0.17
- tracks: 856; persistent (alive >= 50% of run): 4; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.94 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 5, 3], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0134/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 154, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 254, merge/split ratio 1.65, nucleations 202
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 480 at frame 111: holes 0, rim-vs-core 0.14, rim-vs-outside 0.07, heterogeneity 0.03; core [0.271, 0.051, 0.0] rim [0.131, 0.039, 0.0]
  - track 504 at frame 114: holes 0, rim-vs-core 0.09, rim-vs-outside 0.07, heterogeneity 0.02; core [0.232, 0.014, 0.0] rim [0.138, 0.012, 0.0]
  - track 691 at frame 128: holes 0, rim-vs-core 0.30, rim-vs-outside 0.42, heterogeneity 0.23; core [0.311, 0.225, 0.855] rim [0.206, 0.099, 0.602]
  - track 163 at frame 66: holes 0, rim-vs-core 0.04, rim-vs-outside 0.03, heterogeneity 0.01; core [0.158, 0.0, 0.0] rim [0.121, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.625, rim/outside 6.62 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.253)
  - radial signal u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.649, rim/outside 3.74 (aggregate of 90 individuals; 3/90 membrane-like individually; rim level 0.128)
  - radial excited fraction: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 3.69 (aggregate of 90 individuals; 7/90 membrane-like individually; rim level 0.285)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #480 (t=555, R_eq 4.89): none; #504 (t=570, R_eq 5.14): none; #691 (t=640, R_eq 12.1): none; #163 (t=330, R_eq 5.47): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
