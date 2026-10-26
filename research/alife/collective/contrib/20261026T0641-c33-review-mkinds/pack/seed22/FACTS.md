# Evidence pack: membrane-kinds (seed 22)

- world: `../../../../../threads/autopoiesis/worlds/membrane_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_kinds/world.py --out collective/contrib/wip-c33-mk/pack --seeds 21 22 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6057], min area 6 px

## Measurements
- components: final 12, mean 13.9, max 23; occupancy final 0.21
- tracks: 156; persistent (alive >= 50% of run): 1; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.91 (1 = constant size)
- enclosures: components with a hole mean 8.19, final 6; holes at thresholds 0.2/0.35/0.5 final [2, 6, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [11, 8, 6]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0112/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 1000, default): splits 62, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.097, nucleations 0
- channel total drift (end/start - 1): [-0.3645, -0.9493, None, -0.2636, -0.4491]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 55: holes 1, rim-vs-core 0.21, rim-vs-outside 0.86, heterogeneity 0.16; core [0.113, 0.832, 0.0, 0.614, 0.579] rim [0.182, 0.64, 0.0, 0.567, 0.619]
  - track 69 at frame 104: holes 0, rim-vs-core 0.72, rim-vs-outside 0.51, heterogeneity 0.16; core [0.231, 0.828, 0.0, 0.859, 0.837] rim [0.388, 0.312, 0.0, 0.523, 0.492]
  - track 142 at frame 190: holes 1, rim-vs-core 0.32, rim-vs-outside 0.81, heterogeneity 0.18; core [0.131, 0.862, 0.004, 0.691, 0.603] rim [0.233, 0.588, 0.002, 0.551, 0.595]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 11.5, rim/outside 0.788 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.468)
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 5.76 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.582)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 7.14 (aggregate of 81 individuals; 1/81 membrane-like individually; rim level 0.191)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 4.93 (aggregate of 81 individuals; 69/81 membrane-like individually; rim level 0.61)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.62, rim/outside 4.85 (aggregate of 81 individuals; 69/81 membrane-like individually; rim level 0.624)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #9 (t=2750, R_eq 10.52, ring): ['L link', 'membrane (wall)']; #69 (t=5200, R_eq 5.26): ['membrane (wall)']; #1 (t=2100, R_eq 14.52, ring): ['K2', 'L link', 'membrane (wall)']; #142 (t=9500, R_eq 8.81, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 49 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
