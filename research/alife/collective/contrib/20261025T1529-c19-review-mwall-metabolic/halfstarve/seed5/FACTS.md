# Evidence pack: pcell-mwall-b42-halfstarve (seed 5)

- world: `../../world_halfstarve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 437s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1529-c19-review-mwall-metabolic/world_halfstarve.py --out collective/contrib/20261025T1529-c19-review-mwall-metabolic/halfstarve/seed5 --seeds 5 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5886], min area 6 px

## Measurements
- components: final 15, mean 19.5, max 27; occupancy final 0.17
- tracks: 58; persistent (alive >= 50% of run): 15; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.56 (1 = constant size)
- enclosures: components with a hole mean 3.32, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 15], H1 [14, 9, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000449/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 17, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.059, nucleations 1
- channel total drift (end/start - 1): [-0.4031, -0.843, -0.448, -0.5949, -0.8186, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 1.31, heterogeneity 0.21; core [0.12, 0.783, 0.713, 0.602, 0.874, 0.396] rim [0.334, 0.245, 0.689, 0.799, 0.817, 0.742]
  - track 16 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 1.04, heterogeneity 0.22; core [0.208, 0.626, 0.867, 0.748, 0.882, 0.654] rim [0.344, 0.307, 0.639, 0.648, 0.802, 0.587]
  - track 26 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 1.34, heterogeneity 0.23; core [0.145, 0.739, 0.761, 0.531, 0.863, 0.424] rim [0.368, 0.214, 0.68, 0.777, 0.764, 0.706]
  - track 56 at frame 178: holes 1, rim-vs-core 0.34, rim-vs-outside 1.22, heterogeneity 0.23; core [0.099, 0.642, 0.689, 0.522, 0.996, 0.374] rim [0.222, 0.383, 0.612, 0.583, 0.915, 0.5]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 114 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 10.5, rim/outside 0.859 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.573)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.699, rim/outside 30.1 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.548)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 26.3 (aggregate of 114 individuals; 96/114 membrane-like individually; rim level 0.845)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.11, rim/outside 21.9 (aggregate of 114 individuals; 109/114 membrane-like individually; rim level 0.861)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 27.4 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.894)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.46, rim/outside 22.6 (aggregate of 114 individuals; 110/114 membrane-like individually; rim level 0.771)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #15 (t=50500, R_eq 6.1): ['L link', 'membrane (wall)', 'M wall material']; #16 (t=50500, R_eq 5.41): ['membrane (wall)', 'M wall material']; #26 (t=50500, R_eq 6.28): ['L link', 'membrane (wall)', 'M wall material']; #56 (t=89000, R_eq 8.72, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 114 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
