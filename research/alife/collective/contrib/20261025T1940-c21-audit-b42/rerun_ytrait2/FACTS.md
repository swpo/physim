# Evidence pack: pcell-mwall-b42-neutral-twin (seed 10)

- world: `../world_ytrait2.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 470s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1940-c21-audit-b42/world_ytrait2.py --out collective/contrib/20261025T1940-c21-audit-b42/rerun_ytrait2 --seeds 10 --threshold 0.35 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0, 1.5944], min area 6 px

## Measurements
- components: final 27, mean 27.0, max 39; occupancy final 0.25
- tracks: 44; persistent (alive >= 50% of run): 27; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.63 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 27, 27], H1 [26, 1, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.000287/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 10000, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.3389, -0.7912, -0.2639, -0.2516, -0.8013, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 1.08, heterogeneity 0.27; core [0.18, 0.55, 0.781, 0.642, 0.851, 0.536] rim [0.344, 0.274, 0.544, 0.576, 0.559, 0.493]
  - track 6 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 1.15, heterogeneity 0.28; core [0.165, 0.532, 0.837, 0.725, 0.993, 0.62] rim [0.298, 0.329, 0.517, 0.522, 0.718, 0.43]
  - track 7 at frame 101: holes 0, rim-vs-core 0.73, rim-vs-outside 0.88, heterogeneity 0.25; core [0.124, 0.649, 0.772, 0.643, 0.607, 0.529] rim [0.408, 0.13, 0.425, 0.539, 0.384, 0.47]
  - track 8 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 0.83, heterogeneity 0.24; core [0.152, 0.595, 0.764, 0.665, 0.51, 0.543] rim [0.426, 0.106, 0.443, 0.548, 0.261, 0.504]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 162 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 14.1, rim/outside 0.855 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.634)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.508, rim/outside 41.8 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.418)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 85.8 (aggregate of 162 individuals; 159/162 membrane-like individually; rim level 0.926)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 3.29, rim/outside 79.2 (aggregate of 162 individuals; 162/162 membrane-like individually; rim level 0.936)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 79.1 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.829)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.66, rim/outside 78.8 (aggregate of 162 individuals; 162/162 membrane-like individually; rim level 0.872)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #5 (t=50500, R_eq 7): ['L link', 'membrane (wall)', 'M wall material']; #6 (t=50500, R_eq 7.16): ['L link', 'membrane (wall)', 'M wall material']; #7 (t=50500, R_eq 7.05): ['L link', 'membrane (wall)', 'M wall material']; #8 (t=50500, R_eq 6.86): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
