# Evidence pack: pcell-mwall-gate (seed 1)

- world: `../../world_mg.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 626s; status ok
- command: `python -m labkit.run scratch/c14/world_mg.py --out scratch/c14/mgpack/seed1 --seeds 1 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5053], min area 6 px

## Measurements
- components: final 22, mean 19.6, max 24; occupancy final 0.40
- tracks: 55; persistent (alive >= 50% of run): 18; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 63.77 (1 = constant size)
- enclosures: components with a hole mean 4.20, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 13, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 22, 22], H1 [20, 12, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000466/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 10000, default): splits 14, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.286, nucleations 0
- channel total drift (end/start - 1): [-0.5189, -0.655, 0.2649, 0.1527, -0.5869, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 1.22, heterogeneity 0.25; core [0.096, 0.597, 0.611, 0.342, 0.948, 0.238] rim [0.208, 0.378, 0.606, 0.534, 0.796, 0.444]
  - track 10 at frame 101: holes 0, rim-vs-core 0.77, rim-vs-outside 0.75, heterogeneity 0.25; core [0.237, 0.523, 0.841, 0.678, 0.821, 0.601] rim [0.466, 0.081, 0.441, 0.597, 0.409, 0.537]
  - track 14 at frame 101: holes 0, rim-vs-core 0.81, rim-vs-outside 1.17, heterogeneity 0.26; core [0.149, 0.641, 0.736, 0.47, 0.907, 0.335] rim [0.401, 0.129, 0.633, 0.777, 0.586, 0.698]
  - track 47 at frame 175: holes 0, rim-vs-core 0.79, rim-vs-outside 1.17, heterogeneity 0.25; core [0.114, 0.608, 0.672, 0.452, 0.911, 0.316] rim [0.362, 0.136, 0.627, 0.782, 0.588, 0.679]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.17, rim/outside 0.906 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.562)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.524, rim/outside 10 (aggregate of 119 individuals; 4/119 membrane-like individually; rim level 0.393)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 11.2 (aggregate of 119 individuals; 59/119 membrane-like individually; rim level 0.771)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.46, rim/outside 10.8 (aggregate of 119 individuals; 103/119 membrane-like individually; rim level 0.787)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 10.4 (aggregate of 119 individuals; 4/119 membrane-like individually; rim level 0.784)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.72, rim/outside 11.5 (aggregate of 119 individuals; 104/119 membrane-like individually; rim level 0.705)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #6 (t=50500, R_eq 11): ['membrane (wall)', 'M wall material']; #10 (t=50500, R_eq 5.97): ['membrane (wall)', 'M wall material']; #14 (t=50500, R_eq 6.98): ['L link', 'membrane (wall)', 'M wall material']; #47 (t=87500, R_eq 7.65): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
