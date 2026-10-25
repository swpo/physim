# Evidence pack: pcell-mwall-b42-starve (seed 7)

- world: `../world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 822s; status ok
- command: `python -m labkit.run /tmp/c20pc/world_starve.py --out /tmp/c20pc/starve_s7 --seeds 7 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6013], min area 6 px

## Measurements
- components: final 0, mean 15.6, max 29; occupancy final 0.00
- tracks: 44; persistent (alive >= 50% of run): 22; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.11 (1 = constant size)
- enclosures: components with a hole mean 1.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.000414/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 9, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.5979, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.72, rim-vs-outside 1.32, heterogeneity 0.24; core [0.086, 0.717, 0.685, 0.476, 0.894, 0.369] rim [0.335, 0.215, 0.649, 0.772, 0.761, 0.672]
  - track 7 at frame 61: holes 0, rim-vs-core 0.77, rim-vs-outside 1.30, heterogeneity 0.25; core [0.082, 0.673, 0.664, 0.422, 0.906, 0.35] rim [0.348, 0.182, 0.636, 0.775, 0.717, 0.688]
  - track 8 at frame 61: holes 0, rim-vs-core 0.64, rim-vs-outside 1.31, heterogeneity 0.22; core [0.119, 0.643, 0.702, 0.54, 0.891, 0.393] rim [0.351, 0.191, 0.666, 0.775, 0.804, 0.69]
  - track 35 at frame 91: holes 1, rim-vs-core 0.38, rim-vs-outside 1.00, heterogeneity 0.24; core [0.11, 0.553, 0.675, 0.561, 0.986, 0.4] rim [0.243, 0.289, 0.552, 0.586, 0.815, 0.49]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 10.4, rim/outside 0.822 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.584)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.643, rim/outside 40.9 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.535)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 48 (aggregate of 78 individuals; 60/78 membrane-like individually; rim level 0.872)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.32, rim/outside 43.2 (aggregate of 78 individuals; 77/78 membrane-like individually; rim level 0.91)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 46.5 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.849)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.18, rim/outside 45.3 (aggregate of 78 individuals; 77/78 membrane-like individually; rim level 0.851)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #4 (t=30500, R_eq 7.44): ['L link', 'membrane (wall)', 'M wall material']; #7 (t=30500, R_eq 8.16): ['L link', 'membrane (wall)', 'M wall material']; #8 (t=30500, R_eq 6.72): ['L link', 'membrane (wall)', 'M wall material']; #35 (t=45500, R_eq 9.77, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
