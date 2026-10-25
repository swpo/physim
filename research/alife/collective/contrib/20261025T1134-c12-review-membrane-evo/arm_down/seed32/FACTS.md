# Evidence pack: membrane-evo-down (seed 32)

- world: `../../world_down.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 0.7 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1134-c12-review-membrane-evo/world_down.py --out collective/contrib/20261025T1134-c12-review-membrane-evo/arm_down/seed32 --seeds 32 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7343], min area 6 px

## Measurements
- components: final 18, mean 11.8, max 18; occupancy final 0.29
- tracks: 107; persistent (alive >= 50% of run): 2; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.91 (1 = constant size)
- enclosures: components with a hole mean 10.70, final 15; holes at thresholds 0.2/0.35/0.5 final [5, 16, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 18, 18], H1 [18, 16, 6]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00229/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 5000, default): splits 44, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.023, nucleations 0
- channel total drift (end/start - 1): [-0.6536, None, 0.1128, -0.1919]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 95: holes 1, rim-vs-core 0.37, rim-vs-outside 0.67, heterogeneity 0.21; core [0.817, 0.0, 0.706, 0.537] rim [0.481, 0.0, 0.567, 0.615]
  - track 55 at frame 120: holes 1, rim-vs-core 0.38, rim-vs-outside 0.69, heterogeneity 0.21; core [0.832, 0.0, 0.677, 0.549] rim [0.477, 0.0, 0.566, 0.628]
  - track 46 at frame 104: holes 1, rim-vs-core 0.40, rim-vs-outside 0.74, heterogeneity 0.20; core [0.854, 0.0, 0.58, 0.381] rim [0.532, 0.0, 0.554, 0.621]
  - track 60 at frame 112: holes 1, rim-vs-core 0.33, rim-vs-outside 0.72, heterogeneity 0.20; core [0.824, 0.0, 0.626, 0.503] rim [0.525, 0.0, 0.549, 0.613]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 8.32 (aggregate of 83 individuals; 15/83 membrane-like individually; rim level 0.61)
  - radial K2: flat profile (no radial structure; level 0; aggregate of 83 individuals)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 5.57 (aggregate of 83 individuals; 59/83 membrane-like individually; rim level 0.517)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.94, rim/outside 4.08 (aggregate of 83 individuals; 69/83 membrane-like individually; rim level 0.517)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #31 (t=23750, R_eq 9.95, ring): ['L link', 'membrane (wall)']; #55 (t=30000, R_eq 9.25, ring): ['K1', 'L link', 'membrane (wall)']; #46 (t=26000, R_eq 11.6, ring): ['membrane (wall)']; #60 (t=28000, R_eq 12.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 65 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
