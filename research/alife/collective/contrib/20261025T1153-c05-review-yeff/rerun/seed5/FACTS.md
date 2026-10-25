# Evidence pack: pcell-yeff (seed 5)

- world: `../../../../contrib/20261025T1037-c06-pcell-yeff-response/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 121 frames x 500 steps x dt 1.0 = time 60000; grid [128, 128]; wall 266s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1037-c06-pcell-yeff-response/world.py --out collective/work_c05/rev_ye/rerun/seed5 --seeds 5 --frames 120 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5683], min area 6 px

## Measurements
- components: final 4, mean 18.3, max 25; occupancy final 0.27
- tracks: 61; persistent (alive >= 50% of run): 20; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.88 (1 = constant size)
- enclosures: components with a hole mean 5.93, final 2; holes at thresholds 0.2/0.35/0.5 final [50, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 4, 4], H1 [6, 3, 3]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.000714/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.312, nucleations 3
- channel total drift (end/start - 1): [-0.7883, -0.321, 1.0655, -0.3905]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 61: holes 1, rim-vs-core 0.23, rim-vs-outside 0.63, heterogeneity 0.20; core [0.222, 0.495, 0.684, 0.596] rim [0.299, 0.321, 0.554, 0.568]
  - track 18 at frame 58: holes 1, rim-vs-core 0.44, rim-vs-outside 0.70, heterogeneity 0.21; core [0.164, 0.758, 0.571, 0.265] rim [0.246, 0.429, 0.597, 0.538]
  - track 35 at frame 57: holes 0, rim-vs-core 0.61, rim-vs-outside 0.86, heterogeneity 0.22; core [0.181, 0.656, 0.629, 0.429] rim [0.376, 0.185, 0.629, 0.77]
  - track 39 at frame 51: holes 0, rim-vs-core 0.63, rim-vs-outside 0.87, heterogeneity 0.22; core [0.2, 0.677, 0.668, 0.479] rim [0.405, 0.165, 0.627, 0.773]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 104 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.43, rim/outside 0.946 (aggregate of 104 individuals; 0/104 membrane-like individually; rim level 0.513)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 7.29 (aggregate of 104 individuals; 0/104 membrane-like individually; rim level 0.528)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 5.98 (aggregate of 104 individuals; 61/104 membrane-like individually; rim level 0.765)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.61, rim/outside 5.26 (aggregate of 104 individuals; 89/104 membrane-like individually; rim level 0.731)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #6 (t=30500, R_eq 9.66, ring): ['L link', 'membrane (wall)']; #18 (t=29000, R_eq 14, ring): ['membrane (wall)']; #35 (t=28500, R_eq 8.65): ['L link', 'membrane (wall)']; #39 (t=25500, R_eq 7.51): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 33 of 104 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
