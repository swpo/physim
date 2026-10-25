# Evidence pack: pcell-mwall-b42 (seed 24)

- world: `../../../20261025T1430-c14-pcell-mwall-b42-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 723s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim/world.py --out collective/contrib/20261025T2142-c24-review-b42-founders/pack/seed24 --seeds 24 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6217], min area 6 px

## Measurements
- components: final 28, mean 26.9, max 30; occupancy final 0.34
- tracks: 54; persistent (alive >= 50% of run): 23; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 31.08 (1 = constant size)
- enclosures: components with a hole mean 5.81, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 28, 28], H1 [23, 18, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.000437/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 10000, default): splits 15, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.4813, -0.6738, 0.1123, -0.1038, -0.6233, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 0.81, heterogeneity 0.22; core [0.231, 0.544, 0.833, 0.703, 0.833, 0.613] rim [0.425, 0.133, 0.521, 0.662, 0.611, 0.587]
  - track 6 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 0.79, heterogeneity 0.22; core [0.225, 0.545, 0.816, 0.758, 0.835, 0.637] rim [0.409, 0.105, 0.478, 0.602, 0.518, 0.554]
  - track 10 at frame 101: holes 0, rim-vs-core 0.65, rim-vs-outside 1.31, heterogeneity 0.22; core [0.141, 0.676, 0.712, 0.518, 0.863, 0.407] rim [0.362, 0.22, 0.648, 0.776, 0.759, 0.689]
  - track 44 at frame 166: holes 0, rim-vs-core 0.34, rim-vs-outside 1.02, heterogeneity 0.20; core [0.17, 0.591, 0.79, 0.753, 0.894, 0.589] rim [0.265, 0.39, 0.588, 0.635, 0.859, 0.499]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.2, rim/outside 0.865 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.569)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.682, rim/outside 27.5 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.52)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 25.3 (aggregate of 163 individuals; 123/163 membrane-like individually; rim level 0.832)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.65, rim/outside 21.2 (aggregate of 163 individuals; 157/163 membrane-like individually; rim level 0.864)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 25.7 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.887)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.21, rim/outside 21.7 (aggregate of 163 individuals; 160/163 membrane-like individually; rim level 0.766)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #4 (t=50500, R_eq 5.67): ['L link', 'membrane (wall)', 'M wall material']; #6 (t=50500, R_eq 5.5): ['membrane (wall)', 'M wall material']; #10 (t=50500, R_eq 6.63): ['L link', 'membrane (wall)', 'M wall material']; #44 (t=83000, R_eq 5.86): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
