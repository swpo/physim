# Evidence pack: pcell-mwall-b42 (seed 7)

- world: `../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 905s; status ok
- command: `python -m labkit.run /tmp/c20pc/world.py --out /tmp/c20pc/fed_s7 --seeds 7 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6335], min area 6 px

## Measurements
- components: final 29, mean 26.9, max 30; occupancy final 0.35
- tracks: 60; persistent (alive >= 50% of run): 23; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 38.43 (1 = constant size)
- enclosures: components with a hole mean 4.63, final 13; holes at thresholds 0.2/0.35/0.5 final [0, 14, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 29, 29], H1 [24, 17, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.000415/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [-0.4934, -0.6627, 0.135, 0.0671, -0.6029, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 0.82, heterogeneity 0.21; core [0.262, 0.611, 0.915, 0.825, 0.775, 0.781] rim [0.448, 0.161, 0.54, 0.615, 0.586, 0.643]
  - track 7 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 1.28, heterogeneity 0.22; core [0.11, 0.635, 0.619, 0.47, 0.903, 0.316] rim [0.351, 0.187, 0.628, 0.787, 0.782, 0.701]
  - track 9 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 0.81, heterogeneity 0.22; core [0.226, 0.589, 0.82, 0.761, 0.793, 0.682] rim [0.437, 0.134, 0.462, 0.57, 0.573, 0.525]
  - track 52 at frame 183: holes 0, rim-vs-core 0.72, rim-vs-outside 1.26, heterogeneity 0.24; core [0.104, 0.654, 0.637, 0.471, 0.956, 0.319] rim [0.332, 0.191, 0.633, 0.781, 0.771, 0.658]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 164 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.89, rim/outside 0.857 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.569)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.664, rim/outside 26.2 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.511)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 23.5 (aggregate of 164 individuals; 116/164 membrane-like individually; rim level 0.826)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.38, rim/outside 19.9 (aggregate of 164 individuals; 156/164 membrane-like individually; rim level 0.864)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 23.6 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.868)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.9, rim/outside 21.2 (aggregate of 164 individuals; 156/164 membrane-like individually; rim level 0.767)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #4 (t=50500, R_eq 4.58): ['membrane (wall)', 'M wall material']; #7 (t=50500, R_eq 7.96): ['L link', 'membrane (wall)', 'M wall material']; #9 (t=50500, R_eq 5.56): ['L link', 'membrane (wall)', 'M wall material']; #52 (t=91500, R_eq 8): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 164 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
