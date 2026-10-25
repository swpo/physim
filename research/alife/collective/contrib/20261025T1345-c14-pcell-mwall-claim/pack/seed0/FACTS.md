# Evidence pack: pcell-mwall (seed 0)

- world: `../../world_m.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 1145s; status ok
- command: `python -m labkit.run scratch/c14/world_m.py --out scratch/c14/mpack/seed0 --seeds 0 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5612], min area 6 px

## Measurements
- components: final 17, mean 17.2, max 23; occupancy final 0.39
- tracks: 64; persistent (alive >= 50% of run): 11; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.19 (1 = constant size)
- enclosures: components with a hole mean 7.95, final 12; holes at thresholds 0.2/0.35/0.5 final [11, 12, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 17, 17], H1 [18, 15, 6]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.00112/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 10000, default): splits 19, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.105, nucleations 4
- channel total drift (end/start - 1): [-0.6511, -0.5124, 0.5904, -0.0174, -0.3455, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 101: holes 1, rim-vs-core 0.40, rim-vs-outside 1.02, heterogeneity 0.23; core [0.18, 0.596, 0.681, 0.524, 0.956, 0.334] rim [0.292, 0.312, 0.579, 0.599, 0.764, 0.465]
  - track 24 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 0.91, heterogeneity 0.21; core [0.223, 0.631, 0.871, 0.766, 0.902, 0.529] rim [0.379, 0.147, 0.492, 0.585, 0.74, 0.399]
  - track 25 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 1.26, heterogeneity 0.23; core [0.176, 0.69, 0.758, 0.581, 0.958, 0.362] rim [0.263, 0.422, 0.643, 0.618, 0.838, 0.412]
  - track 57 at frame 185: holes 1, rim-vs-core 0.26, rim-vs-outside 0.94, heterogeneity 0.22; core [0.189, 0.519, 0.678, 0.615, 0.971, 0.378] rim [0.259, 0.348, 0.576, 0.567, 0.83, 0.435]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 102 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.73, rim/outside 0.946 (aggregate of 102 individuals; 0/102 membrane-like individually; rim level 0.477)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 5.47 (aggregate of 102 individuals; 1/102 membrane-like individually; rim level 0.523)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 4.42 (aggregate of 102 individuals; 52/102 membrane-like individually; rim level 0.713)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.55, rim/outside 3.76 (aggregate of 102 individuals; 84/102 membrane-like individually; rim level 0.645)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 4.3 (aggregate of 102 individuals; 0/102 membrane-like individually; rim level 0.874)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3, rim/outside 3.85 (aggregate of 102 individuals; 88/102 membrane-like individually; rim level 0.522)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #14 (t=50500, R_eq 9.04, ring): ['L link', 'membrane (wall)', 'M wall material']; #24 (t=50500, R_eq 5.26): ['membrane (wall)', 'M wall material']; #25 (t=50500, R_eq 7.36): ['L link', 'membrane (wall)', 'M wall material']; #57 (t=92500, R_eq 9.59, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 102 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
