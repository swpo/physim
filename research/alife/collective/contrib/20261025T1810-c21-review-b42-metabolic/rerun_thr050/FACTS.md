# Evidence pack: pcell-mwall-b42-starve (seed 8)

- world: `../../20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 483s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world_starve.py --out collective/contrib/20261025T1810-c21-review-b42-metabolic/rerun --seeds 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5923], min area 6 px

## Measurements
- components: final 0, mean 13.8, max 26; occupancy final 0.00
- tracks: 38; persistent (alive >= 50% of run): 22; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 39.44 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.000577/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 10000, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5087, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 61: holes 0, rim-vs-core 0.70, rim-vs-outside 0.98, heterogeneity 0.22; core [0.202, 0.641, 0.899, 0.708, 0.856, 0.697] rim [0.428, 0.128, 0.521, 0.639, 0.742, 0.589]
  - track 10 at frame 61: holes 0, rim-vs-core 0.69, rim-vs-outside 1.32, heterogeneity 0.24; core [0.077, 0.642, 0.65, 0.472, 0.953, 0.353] rim [0.324, 0.207, 0.647, 0.772, 0.77, 0.675]
  - track 12 at frame 61: holes 0, rim-vs-core 0.60, rim-vs-outside 1.30, heterogeneity 0.22; core [0.099, 0.67, 0.692, 0.589, 0.91, 0.424] rim [0.364, 0.22, 0.613, 0.73, 0.842, 0.668]
  - track 13 at frame 61: holes 0, rim-vs-core 0.66, rim-vs-outside 0.87, heterogeneity 0.22; core [0.226, 0.565, 0.83, 0.771, 0.803, 0.711] rim [0.435, 0.129, 0.481, 0.594, 0.631, 0.588]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 13.8, rim/outside 0.797 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.6)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.637, rim/outside 55.2 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.551)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 84.8 (aggregate of 68 individuals; 50/68 membrane-like individually; rim level 0.892)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.17, rim/outside 81.4 (aggregate of 68 individuals; 67/68 membrane-like individually; rim level 0.928)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 85.7 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.889)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.1, rim/outside 80.6 (aggregate of 68 individuals; 67/68 membrane-like individually; rim level 0.889)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=30500, R_eq 5.53): ['membrane (wall)', 'M wall material']; #10 (t=30500, R_eq 7.96): ['L link', 'membrane (wall)', 'M wall material']; #12 (t=30500, R_eq 6.82): ['L link', 'membrane (wall)', 'M wall material']; #13 (t=30500, R_eq 5.38): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
