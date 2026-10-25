# Evidence pack: pcell-multilevel-res15 (seed 0)

- world: `../../world_res15.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 125 steps x dt 1.0 = time 20000; grid [192, 192]; wall 203s; status ok
- command: `python -m labkit.run collective/work/pcell/W/world_res15.py --out collective/work/pcell/W/pack_res15 --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.4996], min area 6 px

## Measurements
- components: final 25, mean 20.6, max 26; occupancy final 0.34
- tracks: 76; persistent (alive >= 50% of run): 22; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.69 (1 = constant size)
- enclosures: components with a hole mean 8.19, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 5, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 25, 25], H1 [25, 22, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2500, default): splits 22, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.182, nucleations 7
- channel total drift (end/start - 1): [-0.4847, -0.6598, 0.0928, -0.1103, -0.6681]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 83: holes 2, rim-vs-core 0.43, rim-vs-outside 1.15, heterogeneity 0.22; core [0.099, 0.74, 0.588, 0.444, 0.882] rim [0.234, 0.385, 0.605, 0.625, 0.79]
  - track 26 at frame 83: holes 0, rim-vs-core 0.66, rim-vs-outside 1.17, heterogeneity 0.23; core [0.101, 0.689, 0.624, 0.428, 0.912] rim [0.329, 0.207, 0.631, 0.777, 0.76]
  - track 29 at frame 83: holes 1, rim-vs-core 0.38, rim-vs-outside 1.20, heterogeneity 0.23; core [0.083, 0.701, 0.549, 0.375, 0.893] rim [0.211, 0.448, 0.602, 0.606, 0.812]
  - track 65 at frame 117: holes 0, rim-vs-core 0.40, rim-vs-outside 1.16, heterogeneity 0.23; core [0.126, 0.742, 0.694, 0.529, 0.836] rim [0.267, 0.398, 0.629, 0.638, 0.764]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.7, rim/outside 0.927 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.55)
  - radial K particles: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 14.3 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.626)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 9.94 (aggregate of 133 individuals; 118/133 membrane-like individually; rim level 0.785)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 5.93, rim/outside 8.14 (aggregate of 133 individuals; 129/133 membrane-like individually; rim level 0.796)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 10.1 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.858)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #24 (t=10375, R_eq 14.43): ['L link', 'membrane (wall)']; #26 (t=10375, R_eq 12.91): ['L link', 'membrane (wall)']; #29 (t=10375, R_eq 14.1): ['L link', 'membrane (wall)']; #65 (t=14625, R_eq 11.77): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
