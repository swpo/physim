# Evidence pack: pcell-mwall-b42 (seed 4)

- world: `../../world_m42_15.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [192, 192]; wall 1223s; status ok
- command: `python -m labkit.run scratch/c14/world_m42_15.py --out scratch/c14/m42pack15/seed4 --seeds 4 --size 192 192 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6057], min area 6 px

## Measurements
- components: final 28, mean 25.8, max 31; occupancy final 0.34
- tracks: 72; persistent (alive >= 50% of run): 24; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 22.53 (1 = constant size)
- enclosures: components with a hole mean 6.74, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 12, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 28, 28], H1 [25, 17, 1]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.000665/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 20, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.4969, -0.6631, 0.1104, -0.0552, -0.6069, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 101: holes 1, rim-vs-core 0.23, rim-vs-outside 1.02, heterogeneity 0.22; core [0.11, 0.541, 0.615, 0.554, 0.979, 0.32] rim [0.188, 0.388, 0.572, 0.585, 0.92, 0.452]
  - track 24 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 1.04, heterogeneity 0.20; core [0.219, 0.757, 0.945, 0.853, 0.767, 0.782] rim [0.38, 0.235, 0.609, 0.677, 0.73, 0.555]
  - track 27 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 1.33, heterogeneity 0.23; core [0.12, 0.718, 0.691, 0.519, 0.882, 0.354] rim [0.355, 0.23, 0.66, 0.791, 0.801, 0.652]
  - track 63 at frame 161: holes 0, rim-vs-core 0.39, rim-vs-outside 1.14, heterogeneity 0.23; core [0.162, 0.619, 0.73, 0.666, 0.913, 0.455] rim [0.288, 0.31, 0.605, 0.693, 0.759, 0.472]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 157 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.52, rim/outside 0.859 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.548)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.693, rim/outside 24.3 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.557)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 21.6 (aggregate of 157 individuals; 124/157 membrane-like individually; rim level 0.814)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.23, rim/outside 17.8 (aggregate of 157 individuals; 149/157 membrane-like individually; rim level 0.831)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 20.9 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.87)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.46, rim/outside 20.7 (aggregate of 157 individuals; 153/157 membrane-like individually; rim level 0.722)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #11 (t=50500, R_eq 16.08, ring): ['L link', 'membrane (wall)', 'M wall material']; #24 (t=50500, R_eq 6.41): ['membrane (wall)', 'M wall material']; #27 (t=50500, R_eq 10.11): ['L link', 'membrane (wall)', 'M wall material']; #63 (t=80500, R_eq 9.57): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 42 of 157 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
