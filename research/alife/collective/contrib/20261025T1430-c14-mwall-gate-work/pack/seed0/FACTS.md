# Evidence pack: pcell-mwall-gate (seed 0)

- world: `../../world_mg.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 616s; status ok
- command: `python -m labkit.run scratch/c14/world_mg.py --out scratch/c14/mgpack/seed0 --seeds 0 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.512], min area 6 px

## Measurements
- components: final 19, mean 19.9, max 21; occupancy final 0.42
- tracks: 44; persistent (alive >= 50% of run): 18; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 44.92 (1 = constant size)
- enclosures: components with a hole mean 4.69, final 7; holes at thresholds 0.2/0.35/0.5 final [0, 16, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 19, 19], H1 [21, 12, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0005/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.2, nucleations 1
- channel total drift (end/start - 1): [-0.5316, -0.6347, 0.2999, -0.0507, -0.5645, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.98, heterogeneity 0.23; core [0.239, 0.577, 0.881, 0.685, 0.798, 0.606] rim [0.409, 0.123, 0.542, 0.666, 0.616, 0.587]
  - track 5 at frame 101: holes 1, rim-vs-core 0.36, rim-vs-outside 0.96, heterogeneity 0.25; core [0.137, 0.504, 0.641, 0.428, 0.995, 0.301] rim [0.218, 0.329, 0.599, 0.553, 0.793, 0.486]
  - track 11 at frame 101: holes 1, rim-vs-core 0.50, rim-vs-outside 0.97, heterogeneity 0.25; core [0.126, 0.562, 0.677, 0.477, 0.947, 0.346] rim [0.274, 0.251, 0.57, 0.599, 0.683, 0.538]
  - track 38 at frame 138: holes 0, rim-vs-core 0.82, rim-vs-outside 1.19, heterogeneity 0.25; core [0.106, 0.61, 0.65, 0.379, 0.935, 0.283] rim [0.361, 0.133, 0.606, 0.761, 0.625, 0.646]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 120 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.48, rim/outside 0.912 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.562)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.533, rim/outside 9.05 (aggregate of 120 individuals; 1/120 membrane-like individually; rim level 0.392)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 9.93 (aggregate of 120 individuals; 62/120 membrane-like individually; rim level 0.764)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.28, rim/outside 9.5 (aggregate of 120 individuals; 100/120 membrane-like individually; rim level 0.773)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 9.33 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.787)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.48, rim/outside 10.2 (aggregate of 120 individuals; 101/120 membrane-like individually; rim level 0.69)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #2 (t=50500, R_eq 5.44): ['membrane (wall)', 'M wall material']; #5 (t=50500, R_eq 10.91, ring): ['L link', 'membrane (wall)', 'M wall material']; #11 (t=50500, R_eq 9.54, ring): ['L link', 'membrane (wall)', 'M wall material']; #38 (t=69000, R_eq 8.9): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
