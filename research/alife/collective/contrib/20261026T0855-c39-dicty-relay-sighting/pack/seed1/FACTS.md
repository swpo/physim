# Evidence pack: dicty-relay (seed 1)

- world: `../../world.py`, family `excitable-chemotaxis`
- parent: None; mutation: new class: agents with FitzHugh-Nagumo relay of a diffusing signal and chemotaxis while excited
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 107s; status ok
- command: `python -m labkit.run collective/contrib/c39-dicty-wip/world.py --out collective/contrib/c39-dicty-wip/pack/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 7.4287], min area 6 px

## Measurements
- components: final 7, mean 21.9, max 113; occupancy final 0.17
- tracks: 981; persistent (alive >= 50% of run): 1; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.33 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 4], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0328/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 100, default): splits 176, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 287, merge/split ratio 1.63, nucleations 226
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 634 at frame 94: holes 0, rim-vs-core 0.06, rim-vs-outside 0.06, heterogeneity 0.01; core [0.191, 0.002, 0.0] rim [0.129, 0.002, 0.0]
  - track 879 at frame 151: holes 0, rim-vs-core 0.01, rim-vs-outside 0.01, heterogeneity 0.00; core [0.12, 0.0, 0.0] rim [0.11, 0.0, 0.0]
  - track 667 at frame 76: holes 0, rim-vs-core 0.47, rim-vs-outside 0.11, heterogeneity 0.15; core [0.519, 0.485, 1.0] rim [0.122, 0.23, 1.0]
  - track 806 at frame 79: holes 0, rim-vs-core 0.56, rim-vs-outside 0.12, heterogeneity 0.30; core [0.56, 0.551, 0.787] rim [0.121, 0.241, 0.64]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.643, rim/outside 8.29 (aggregate of 77 individuals; 2/77 membrane-like individually; rim level 0.256)
  - radial signal u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.658, rim/outside 5.89 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.13)
  - radial excited fraction: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 5.38 (aggregate of 77 individuals; 7/77 membrane-like individually; rim level 0.251)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #634 (t=470, R_eq 4.85): none; #879 (t=755, R_eq 2.88): none; #667 (t=380, R_eq 5.23): none; #806 (t=395, R_eq 5.47): none

## Warnings
- radial: 1 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
