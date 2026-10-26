# Evidence pack: dicty-relay (seed 0)

- world: `../../world.py`, family `excitable-chemotaxis`
- parent: None; mutation: new class: agents with FitzHugh-Nagumo relay of a diffusing signal and chemotaxis while excited
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 83s; status ok
- command: `python -m labkit.run collective/contrib/c39-dicty-wip/world.py --out collective/contrib/c39-dicty-wip/ctrl_v0/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.60 of robust range [0.1093, 0.7626], min area 6 px

## Measurements
- components: final 43, mean 47.3, max 97; occupancy final 0.03
- tracks: 3572; persistent (alive >= 50% of run): 0; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [59, 84, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [148, 35, 1], H1 [144, 31, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.105/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 331, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 309, merge/split ratio 0.934, nucleations 2546
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1555 at frame 97: holes 0, rim-vs-core 0.10, rim-vs-outside 0.19, heterogeneity 0.04; core [0.913, 0.0, 0.0] rim [0.814, 0.0, 0.0]
  - track 1239 at frame 77: holes 0, rim-vs-core 0.10, rim-vs-outside 0.17, heterogeneity 0.11; core [0.885, 0.434, 0.967] rim [0.809, 0.405, 0.914]
  - track 2393 at frame 143: holes 0, rim-vs-core 0.16, rim-vs-outside 0.25, heterogeneity 0.03; core [1.0, 0.0, 0.0] rim [0.84, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 117 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial agent density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 1.61 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.792)
  - radial signal u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.14 (aggregate of 117 individuals; 4/117 membrane-like individually; rim level 0.249)
  - radial excited fraction: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 1.06 (aggregate of 117 individuals; 6/117 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1555 (t=485, R_eq 2.59): none; #1239 (t=385, R_eq 3.04): none; #2080 (t=630, R_eq 2.19): none; #2393 (t=715, R_eq 2.33): none

## Warnings
- radial: 3 of 117 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
