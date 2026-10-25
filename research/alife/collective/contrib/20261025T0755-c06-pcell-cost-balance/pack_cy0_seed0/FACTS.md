# Evidence pack: pcell-yield (seed 0)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 475s; status ok
- command: `python -m labkit.run collective/work/pcell/claim/world.py --out collective/work/pcell/claim/pack --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.563], min area 6 px

## Measurements
- components: final 3, mean 15.7, max 23; occupancy final 0.20
- tracks: 90; persistent (alive >= 50% of run): 12; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.97 (1 = constant size)
- enclosures: components with a hole mean 7.47, final 1; holes at thresholds 0.2/0.35/0.5 final [27, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 3, 3], H1 [8, 3, 2]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.00106/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 10000, default): splits 24, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 16, merge/split ratio 0.667, nucleations 4
- channel total drift (end/start - 1): [-0.8048, -0.3721, 1.0753, -0.4818, 0.2731]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 86: holes 0, rim-vs-core 0.61, rim-vs-outside 1.00, heterogeneity 0.21; core [0.181, 0.627, 0.641, 0.438, 0.666] rim [0.38, 0.189, 0.636, 0.772, 0.488]
  - track 28 at frame 86: holes 0, rim-vs-core 0.50, rim-vs-outside 1.00, heterogeneity 0.21; core [0.178, 0.654, 0.64, 0.395, 0.629] rim [0.328, 0.306, 0.635, 0.699, 0.501]
  - track 24 at frame 74: holes 1, rim-vs-core 0.28, rim-vs-outside 0.87, heterogeneity 0.20; core [0.19, 0.62, 0.664, 0.521, 0.656] rim [0.27, 0.376, 0.604, 0.596, 0.592]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.85, rim/outside 0.953 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.474)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.727, rim/outside 4.55 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.491)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.89 (aggregate of 83 individuals; 35/83 membrane-like individually; rim level 0.706)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.04, rim/outside 3.62 (aggregate of 83 individuals; 64/83 membrane-like individually; rim level 0.638)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 3.37 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.601)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #25 (t=43000, R_eq 8.29): ['L link', 'membrane (wall)']; #28 (t=43000, R_eq 8.14): ['L link', 'membrane (wall)']; #24 (t=37000, R_eq 10.88, ring): ['membrane (wall)']; #48 (t=54500, R_eq 14.57, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
