# Evidence pack: membrane-evo (seed 32)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1134-c12-review-membrane-evo/world_twin.py --out collective/contrib/20261025T1134-c12-review-membrane-evo/arm_twin/seed32 --seeds 32 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7349], min area 6 px

## Measurements
- components: final 15, mean 11.8, max 18; occupancy final 0.29
- tracks: 86; persistent (alive >= 50% of run): 5; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.97 (1 = constant size)
- enclosures: components with a hole mean 10.89, final 12; holes at thresholds 0.2/0.35/0.5 final [9, 14, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [17, 13, 10]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00229/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 5000, default): splits 34, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6746, None, 0.1596, -0.1787]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 102: holes 1, rim-vs-core 0.37, rim-vs-outside 0.68, heterogeneity 0.20; core [0.825, 0.0, 0.665, 0.56] rim [0.482, 0.0, 0.557, 0.636]
  - track 49 at frame 114: holes 1, rim-vs-core 0.34, rim-vs-outside 0.71, heterogeneity 0.20; core [0.732, 0.0, 0.553, 0.629] rim [0.402, 0.0, 0.476, 0.693]
  - track 54 at frame 117: holes 1, rim-vs-core 0.39, rim-vs-outside 0.69, heterogeneity 0.21; core [0.834, 0.0, 0.677, 0.549] rim [0.477, 0.0, 0.556, 0.632]
  - track 60 at frame 112: holes 1, rim-vs-core 0.32, rim-vs-outside 0.72, heterogeneity 0.20; core [0.824, 0.0, 0.637, 0.525] rim [0.526, 0.0, 0.546, 0.612]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 8.76 (aggregate of 80 individuals; 13/80 membrane-like individually; rim level 0.598)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.66 (aggregate of 80 individuals; 1/80 membrane-like individually; rim level 0.0192)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 5.87 (aggregate of 80 individuals; 56/80 membrane-like individually; rim level 0.514)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.85, rim/outside 4.26 (aggregate of 80 individuals; 71/80 membrane-like individually; rim level 0.516)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #31 (t=25500, R_eq 9.57, ring): ['K1', 'L link', 'membrane (wall)']; #49 (t=28500, R_eq 8.96, ring): ['membrane (wall)']; #54 (t=29250, R_eq 9.24, ring): ['L link', 'membrane (wall)']; #60 (t=28000, R_eq 13.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 67 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
