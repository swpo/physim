# Evidence pack: pcell-multilevel-nogate-lowD (seed 3)

- world: `../../20261025T0857-c06-pcell-contained-heredity/W/world_lowD.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 101 frames x 200 steps x dt 1.0 = time 20000; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0857-c06-pcell-contained-heredity/W/world_lowD.py --out collective/contrib/20261025T0913-c01-review-pcell-contained/pack_lowD --seeds 3 --frames 100 --spf 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5576], min area 6 px

## Measurements
- components: final 8, mean 10.3, max 15; occupancy final 0.30
- tracks: 59; persistent (alive >= 50% of run): 6; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.94 (1 = constant size)
- enclosures: components with a hole mean 8.09, final 5; holes at thresholds 0.2/0.35/0.5 final [32, 5, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 8, 8], H1 [11, 7, 5]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00306/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 4000, default): splits 20, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.1, nucleations 2
- channel total drift (end/start - 1): [-0.7389, -0.4412, 0.7299, -0.1763, -0.109]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 62: holes 0, rim-vs-core 0.53, rim-vs-outside 1.08, heterogeneity 0.21; core [0.232, 0.674, 0.764, 0.561, 0.875] rim [0.372, 0.229, 0.677, 0.748, 0.753]
  - track 36 at frame 62: holes 1, rim-vs-core 0.14, rim-vs-outside 0.85, heterogeneity 0.19; core [0.193, 0.538, 0.478, 0.589, 0.813] rim [0.229, 0.45, 0.584, 0.596, 0.819]
  - track 49 at frame 79: holes 1, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.18; core [0.194, 0.62, 0.711, 0.633, 0.875] rim [0.263, 0.419, 0.603, 0.583, 0.845]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 2.84, rim/outside 0.851 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.411)
  - radial K particles: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 3.36 (aggregate of 59 individuals; 2/59 membrane-like individually; rim level 0.51)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.37 (aggregate of 59 individuals; 28/59 membrane-like individually; rim level 0.552)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.84, rim/outside 1.98 (aggregate of 59 individuals; 45/59 membrane-like individually; rim level 0.431)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 2.77 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.806)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #21 (t=10200, R_eq 15.98, ring): ['membrane (wall)']; #33 (t=12400, R_eq 6.68): ['L link', 'membrane (wall)']; #36 (t=12400, R_eq 15.07, ring): none; #49 (t=15800, R_eq 9.93, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 45 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
