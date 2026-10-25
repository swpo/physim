# Evidence pack: membrane-evo-up (seed 33)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 94s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out collective/contrib/20261025T1355-c09-review-membrane-evo/membrane_evo_up/seed33 --seeds 33 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7072], min area 6 px

## Measurements
- components: final 16, mean 10.1, max 18; occupancy final 0.31
- tracks: 159; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.34, final 14; holes at thresholds 0.2/0.35/0.5 final [9, 15, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 15], H1 [18, 15, 10]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00382/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 5000, default): splits 59, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 26, merge/split ratio 0.441, nucleations 0
- channel total drift (end/start - 1): [-0.9763, None, 0.4807, 0.007]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 79: holes 1, rim-vs-core 0.30, rim-vs-outside 0.72, heterogeneity 0.20; core [0.82, 0.0, 0.648, 0.587] rim [0.541, 0.0, 0.538, 0.608]
  - track 29 at frame 71: holes 1, rim-vs-core 0.40, rim-vs-outside 0.67, heterogeneity 0.21; core [0.862, 0.0, 0.677, 0.574] rim [0.491, 0.0, 0.548, 0.619]
  - track 34 at frame 74: holes 1, rim-vs-core 0.37, rim-vs-outside 0.68, heterogeneity 0.21; core [0.825, 0.0, 0.64, 0.55] rim [0.478, 0.0, 0.534, 0.634]
  - track 78 at frame 136: holes 1, rim-vs-core 0.36, rim-vs-outside 0.73, heterogeneity 0.21; core [0.114, 0.826, 0.674, 0.542] rim [0.069, 0.502, 0.56, 0.629]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 6.25 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.298)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 2.32 (aggregate of 67 individuals; 4/67 membrane-like individually; rim level 0.314)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 2.69 (aggregate of 67 individuals; 35/67 membrane-like individually; rim level 0.47)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.04, rim/outside 2.19 (aggregate of 67 individuals; 48/67 membrane-like individually; rim level 0.448)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #24 (t=19750, R_eq 13.01, ring): ['L link', 'membrane (wall)']; #29 (t=17750, R_eq 9.87, ring): ['K1', 'L link', 'membrane (wall)']; #34 (t=18500, R_eq 9.51, ring): ['L link', 'membrane (wall)']; #78 (t=34000, R_eq 10.69, ring): ['K2', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
