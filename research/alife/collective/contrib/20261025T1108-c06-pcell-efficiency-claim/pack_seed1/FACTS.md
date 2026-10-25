# Evidence pack: pcell-yeff-cap (seed 1)

- world: `../world_cap_pack.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 620s; status ok
- command: `python -m labkit.run collective/work/pcell/yeff/world_cap_pack.py --out collective/work/pcell/yeff/pack_s1 --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5387], min area 6 px

## Measurements
- components: final 14, mean 16.5, max 25; occupancy final 0.38
- tracks: 83; persistent (alive >= 50% of run): 13; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.20 (1 = constant size)
- enclosures: components with a hole mean 8.30, final 9; holes at thresholds 0.2/0.35/0.5 final [17, 9, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 14, 14], H1 [13, 13, 4]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.000476/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 10000, default): splits 12, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.25, nucleations 19
- channel total drift (end/start - 1): [-0.6894, -0.4616, 0.6956, 0.1478, -0.2641]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 101: holes 1, rim-vs-core 0.37, rim-vs-outside 0.93, heterogeneity 0.24; core [0.174, 0.66, 0.613, 0.364, 0.947] rim [0.265, 0.397, 0.608, 0.556, 0.803]
  - track 34 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 0.69, heterogeneity 0.23; core [0.272, 0.55, 0.834, 0.728, 0.894] rim [0.408, 0.111, 0.506, 0.62, 0.453]
  - track 69 at frame 168: holes 1, rim-vs-core 0.48, rim-vs-outside 0.95, heterogeneity 0.24; core [0.19, 0.682, 0.708, 0.485, 0.924] rim [0.32, 0.304, 0.575, 0.59, 0.72]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 3.09, rim/outside 0.992 (aggregate of 96 individuals; 1/96 membrane-like individually; rim level 0.471)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 4.06 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.509)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.33 (aggregate of 96 individuals; 44/96 membrane-like individually; rim level 0.703)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.52, rim/outside 2.89 (aggregate of 96 individuals; 75/96 membrane-like individually; rim level 0.633)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 3.27 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.867)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #31 (t=50500, R_eq 11.28, ring): ['membrane (wall)']; #34 (t=50500, R_eq 5.67): ['L link', 'membrane (wall)']; #47 (t=53000, R_eq 17.35, ring): none; #69 (t=84000, R_eq 9.11): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
