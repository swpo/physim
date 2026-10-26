# Evidence pack: membrane-kinds (seed 7)

- world: `../../../../threads/autopoiesis/worlds/membrane_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_kinds/world.py --out collective/contrib/20261025T2308-c21-review-mkinds/rerun7 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5399], min area 6 px

## Measurements
- components: final 12, mean 14.2, max 22; occupancy final 0.29
- tracks: 160; persistent (alive >= 50% of run): 2; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 71.11 (1 = constant size)
- enclosures: components with a hole mean 9.64, final 9; holes at thresholds 0.2/0.35/0.5 final [3, 10, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 12], H1 [13, 12, 8]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00686/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 68, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 5, merges 4, merge/split ratio 0.059, nucleations 0
- channel total drift (end/start - 1): [-0.4734, -0.7083, None, 0.0077, -0.0914]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 129: holes 0, rim-vs-core 0.37, rim-vs-outside 0.80, heterogeneity 0.16; core [0.102, 0.82, 0.0, 0.596, 0.619] rim [0.283, 0.507, 0.0, 0.656, 0.659]
  - track 62 at frame 91: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.15; core [0.097, 0.774, 0.0, 0.598, 0.648] rim [0.163, 0.617, 0.0, 0.546, 0.609]
  - track 104 at frame 153: holes 1, rim-vs-core 0.34, rim-vs-outside 0.77, heterogeneity 0.17; core [0.121, 0.842, 0.0, 0.68, 0.602] rim [0.226, 0.56, 0.0, 0.528, 0.575]
  - track 142 at frame 180: holes 1, rim-vs-core 0.15, rim-vs-outside 0.83, heterogeneity 0.14; core [0.094, 0.733, 0.0, 0.557, 0.664] rim [0.157, 0.603, 0.0, 0.533, 0.623]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 12.9, rim/outside 0.797 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.461)
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 6.24 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.708)
  - radial K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1.19 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.0119)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 4.7 (aggregate of 84 individuals; 72/84 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.82, rim/outside 4.53 (aggregate of 84 individuals; 71/84 membrane-like individually; rim level 0.582)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #86 (t=6450, R_eq 8.18): ['membrane (wall)']; #62 (t=4550, R_eq 10.23, ring): ['L link', 'membrane (wall)']; #104 (t=7650, R_eq 9.29, ring): ['L link', 'membrane (wall)']; #142 (t=9000, R_eq 11.35, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 58 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
