# Evidence pack: pcell-mwall-b42 (seed 1)

- world: `../../world_m42.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 1218s; status ok
- command: `python -m labkit.run scratch/c14/world_m42.py --out scratch/c14/m42pack/seed1 --seeds 1 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6251], min area 6 px

## Measurements
- components: final 30, mean 28.8, max 33; occupancy final 0.34
- tracks: 64; persistent (alive >= 50% of run): 25; longest 201 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 17.03 (1 = constant size)
- enclosures: components with a hole mean 6.16, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 30], H1 [24, 18, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.00117/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 10000, default): splits 17, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.4848, -0.6723, 0.1304, 0.0937, -0.6169, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 1.28, heterogeneity 0.23; core [0.115, 0.623, 0.643, 0.446, 0.949, 0.326] rim [0.341, 0.193, 0.605, 0.768, 0.767, 0.643]
  - track 11 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 1.29, heterogeneity 0.23; core [0.116, 0.612, 0.663, 0.442, 0.912, 0.339] rim [0.327, 0.2, 0.655, 0.789, 0.754, 0.652]
  - track 12 at frame 101: holes 0, rim-vs-core 0.63, rim-vs-outside 0.81, heterogeneity 0.20; core [0.19, 0.597, 0.788, 0.777, 0.832, 0.638] rim [0.388, 0.165, 0.479, 0.562, 0.719, 0.498]
  - track 50 at frame 155: holes 0, rim-vs-core 0.68, rim-vs-outside 1.22, heterogeneity 0.23; core [0.141, 0.61, 0.679, 0.53, 0.932, 0.345] rim [0.355, 0.182, 0.64, 0.787, 0.7, 0.671]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.64, rim/outside 0.877 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.554)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.671, rim/outside 25 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.511)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 21.6 (aggregate of 174 individuals; 122/174 membrane-like individually; rim level 0.812)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.38, rim/outside 18.1 (aggregate of 174 individuals; 166/174 membrane-like individually; rim level 0.848)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 22.4 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.896)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.91, rim/outside 18.6 (aggregate of 174 individuals; 170/174 membrane-like individually; rim level 0.744)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #6 (t=50500, R_eq 8): ['L link', 'membrane (wall)', 'M wall material']; #11 (t=50500, R_eq 7.53): ['L link', 'membrane (wall)', 'M wall material']; #12 (t=50500, R_eq 5.64): ['L link', 'membrane (wall)', 'M wall material']; #50 (t=77500, R_eq 6.82): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 37 of 174 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
