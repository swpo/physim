# Evidence pack: membrane-evo-down (seed 22)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo_down/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 0.7 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 106s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_down/world.py --out collective/contrib/_c07rev9/membrane_evo_down/seed22 --seeds 22 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7276], min area 6 px

## Measurements
- components: final 14, mean 10.0, max 16; occupancy final 0.26
- tracks: 105; persistent (alive >= 50% of run): 1; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.83 (1 = constant size)
- enclosures: components with a hole mean 9.19, final 12; holes at thresholds 0.2/0.35/0.5 final [7, 13, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 13], H1 [13, 13, 1]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00408/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 5000, default): splits 43, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.07, nucleations 0
- channel total drift (end/start - 1): [-0.6548, None, 0.0633, -0.285]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 62 at frame 120: holes 1, rim-vs-core 0.41, rim-vs-outside 0.70, heterogeneity 0.22; core [0.851, 0.0, 0.733, 0.497] rim [0.484, 0.0, 0.587, 0.614]
  - track 70 at frame 125: holes 1, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.20; core [0.848, 0.0, 0.637, 0.435] rim [0.537, 0.0, 0.576, 0.617]
  - track 65 at frame 114: holes 1, rim-vs-core 0.38, rim-vs-outside 0.66, heterogeneity 0.20; core [0.805, 0.0, 0.655, 0.581] rim [0.45, 0.0, 0.533, 0.624]
  - track 59 at frame 98: holes 1, rim-vs-core 0.36, rim-vs-outside 0.72, heterogeneity 0.20; core [0.849, 0.0, 0.65, 0.48] rim [0.523, 0.0, 0.548, 0.595]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 9.06 (aggregate of 70 individuals; 12/70 membrane-like individually; rim level 0.582)
  - radial K2: flat profile (no radial structure; level 0; aggregate of 70 individuals)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 5.87 (aggregate of 70 individuals; 51/70 membrane-like individually; rim level 0.486)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.07, rim/outside 3.96 (aggregate of 70 individuals; 63/70 membrane-like individually; rim level 0.462)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #62 (t=30000, R_eq 9.39, ring): ['L link', 'membrane (wall)']; #70 (t=31250, R_eq 11.86, ring): ['K1', 'L link', 'membrane (wall)']; #65 (t=28500, R_eq 10, ring): ['L link', 'membrane (wall)']; #59 (t=24500, R_eq 12.05, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
