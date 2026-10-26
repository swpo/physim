# Evidence pack: pcell-mwall-b42-res15 (seed 10)

- world: `../world_res15.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [192, 192]; wall 1169s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1940-c21-audit-b42/world_res15.py --out collective/contrib/20261025T1940-c21-audit-b42/rerun_res15 --seeds 10 --threshold 0.35 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 1.6623], min area 6 px

## Measurements
- components: final 29, mean 29.0, max 39; occupancy final 0.37
- tracks: 70; persistent (alive >= 50% of run): 28; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.25 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 10, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 29], H1 [23, 16, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.000757/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4709, -0.6774, 0.0458, -0.0198, -0.645, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 101: holes 0, rim-vs-core 0.86, rim-vs-outside 0.72, heterogeneity 0.26; core [0.199, 0.579, 0.773, 0.727, 0.844, 0.567] rim [0.429, 0.102, 0.335, 0.476, 0.473, 0.316]
  - track 20 at frame 101: holes 0, rim-vs-core 1.07, rim-vs-outside 0.82, heterogeneity 0.24; core [0.307, 0.665, 0.951, 0.895, 0.673, 0.917] rim [0.485, 0.163, 0.385, 0.416, 0.612, 0.357]
  - track 21 at frame 101: holes 0, rim-vs-core 0.91, rim-vs-outside 0.67, heterogeneity 0.26; core [0.228, 0.599, 0.796, 0.806, 0.781, 0.636] rim [0.442, 0.096, 0.367, 0.469, 0.368, 0.386]
  - track 64 at frame 173: holes 0, rim-vs-core 0.91, rim-vs-outside 0.73, heterogeneity 0.25; core [0.265, 0.536, 0.84, 0.825, 0.764, 0.717] rim [0.452, 0.109, 0.335, 0.453, 0.494, 0.326]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 173 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.68, rim/outside 0.899 (aggregate of 173 individuals; 0/173 membrane-like individually; rim level 0.6)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.554, rim/outside 19.1 (aggregate of 173 individuals; 0/173 membrane-like individually; rim level 0.458)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 22.5 (aggregate of 173 individuals; 123/173 membrane-like individually; rim level 0.839)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.52, rim/outside 19.2 (aggregate of 173 individuals; 156/173 membrane-like individually; rim level 0.856)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 20.1 (aggregate of 173 individuals; 0/173 membrane-like individually; rim level 0.829)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.5, rim/outside 22.2 (aggregate of 173 individuals; 161/173 membrane-like individually; rim level 0.747)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #18 (t=50500, R_eq 9.59): ['L link', 'membrane (wall)', 'M wall material']; #20 (t=50500, R_eq 6.38): none; #21 (t=50500, R_eq 8.57): ['membrane (wall)', 'M wall material']; #64 (t=86500, R_eq 7.9): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
