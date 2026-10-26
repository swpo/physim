# Evidence pack: membrane-kinds (seed 21)

- world: `../../../../../threads/autopoiesis/worlds/membrane_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_kinds/world.py --out collective/contrib/wip-c33-mk/pack --seeds 21 22 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6117], min area 6 px

## Measurements
- components: final 11, mean 13.0, max 23; occupancy final 0.19
- tracks: 171; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 8.03, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 11, 11], H1 [6, 5, 1]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0244/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 1000, default): splits 71, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 5, merge/split ratio 0.07, nucleations 0
- channel total drift (end/start - 1): [-0.3678, -0.9915, None, -0.2752, -0.4405]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 90 at frame 99: holes 0, rim-vs-core 0.44, rim-vs-outside 1.02, heterogeneity 0.19; core [0.054, 0.001, 0.962, 0.586, 0.49] rim [0.242, 0.0, 0.614, 0.585, 0.682]
  - track 46 at frame 35: holes 1, rim-vs-core 0.28, rim-vs-outside 0.66, heterogeneity 0.16; core [0.132, 0.763, 0.0, 0.586, 0.72] rim [0.224, 0.569, 0.0, 0.508, 0.556]
  - track 83 at frame 96: holes 0, rim-vs-core 0.39, rim-vs-outside 0.94, heterogeneity 0.17; core [0.125, 0.868, 0.0, 0.628, 0.54] rim [0.283, 0.54, 0.0, 0.6, 0.674]
  - track 148 at frame 180: holes 0, rim-vs-core 0.40, rim-vs-outside 0.86, heterogeneity 0.15; core [0.08, 0.031, 0.869, 0.59, 0.815] rim [0.261, 0.022, 0.562, 0.626, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.97, rim/outside 0.782 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.465)
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 6.34 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.49)
  - radial K2: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 6.7 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.246)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 4.91 (aggregate of 78 individuals; 64/78 membrane-like individually; rim level 0.562)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.8, rim/outside 5.23 (aggregate of 78 individuals; 51/78 membrane-like individually; rim level 0.586)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #90 (t=4950, R_eq 8.57, ring): ['L link', 'membrane (wall)']; #46 (t=1750, R_eq 9.92, ring): ['L link', 'membrane (wall)']; #83 (t=4800, R_eq 8.35, ring): ['L link', 'membrane (wall)']; #148 (t=9000, R_eq 7.63): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 40 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
