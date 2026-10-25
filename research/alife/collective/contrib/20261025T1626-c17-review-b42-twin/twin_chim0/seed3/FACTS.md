# Evidence pack: pcell-mwall-b42-chim0 (seed 3)

- world: `../../world_chim0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 424s; status ok
- command: `python -m labkit.run collective/contrib/c17-b42twin-wip/world_chim0.py --out collective/contrib/c17-b42twin-wip/twin_chim0/seed3 --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6382], min area 6 px

## Measurements
- components: final 30, mean 27.9, max 31; occupancy final 0.33
- tracks: 60; persistent (alive >= 50% of run): 25; longest 201 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 15.17 (1 = constant size)
- enclosures: components with a hole mean 6.00, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 12, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 30], H1 [20, 14, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.000978/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.4761, -0.6719, 0.0958, -0.1349, -0.6289, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 1.31, heterogeneity 0.18; core [0.228, 0.481, 0.868, 0.774, 0.864, 0.818] rim [0.258, 0.452, 0.681, 0.648, 0.819, 0.769]
  - track 5 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 1.26, heterogeneity 0.18; core [0.101, 0.723, 0.683, 0.54, 0.907, 0.763] rim [0.328, 0.225, 0.635, 0.776, 0.855, 0.677]
  - track 8 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 0.89, heterogeneity 0.16; core [0.188, 0.595, 0.817, 0.789, 0.833, 0.872] rim [0.392, 0.165, 0.507, 0.596, 0.802, 0.767]
  - track 52 at frame 155: holes 1, rim-vs-core 0.29, rim-vs-outside 1.01, heterogeneity 0.20; core [0.109, 0.556, 0.636, 0.505, 0.996, 0.616] rim [0.214, 0.349, 0.571, 0.579, 0.849, 0.582]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 169 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.39, rim/outside 0.867 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.557)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 24.4 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.508)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 21.9 (aggregate of 169 individuals; 117/169 membrane-like individually; rim level 0.809)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.22, rim/outside 18.6 (aggregate of 169 individuals; 161/169 membrane-like individually; rim level 0.85)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 22 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.875)
  - radial M wall material: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 16 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.763)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #0 (t=50500, R_eq 6.18): ['L link', 'membrane (wall)']; #5 (t=50500, R_eq 6.79): ['L link', 'membrane (wall)']; #8 (t=50500, R_eq 5.32): ['membrane (wall)']; #52 (t=77500, R_eq 9.49, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 169 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
