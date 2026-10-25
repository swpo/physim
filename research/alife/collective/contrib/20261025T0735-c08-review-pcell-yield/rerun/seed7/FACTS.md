# Evidence pack: pcell (seed 7)

- world: `../world_y07.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 100 steps x dt 1.0 = time 16000; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev/world_y07.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev/rerun --seeds 7 --frames 160 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6446], min area 6 px

## Measurements
- components: final 26, mean 24.4, max 26; occupancy final 0.30
- tracks: 73; persistent (alive >= 50% of run): 24; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.07 (1 = constant size)
- enclosures: components with a hole mean 8.14, final 14; holes at thresholds 0.2/0.35/0.5 final [0, 15, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 26, 26], H1 [15, 14, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00104/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 18, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.389, nucleations 2
- channel total drift (end/start - 1): [-0.4453, -0.6911, 0.0076, -0.0672]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 81: holes 1, rim-vs-core 0.26, rim-vs-outside 0.69, heterogeneity 0.21; core [0.113, 0.538, 0.614, 0.509] rim [0.231, 0.336, 0.562, 0.605]
  - track 29 at frame 81: holes 0, rim-vs-core 0.61, rim-vs-outside 0.57, heterogeneity 0.20; core [0.259, 0.648, 0.87, 0.781] rim [0.441, 0.187, 0.544, 0.646]
  - track 35 at frame 82: holes 2, rim-vs-core 0.27, rim-vs-outside 0.78, heterogeneity 0.21; core [0.08, 0.604, 0.577, 0.454] rim [0.185, 0.382, 0.569, 0.576]
  - track 69 at frame 124: holes 1, rim-vs-core 0.42, rim-vs-outside 0.82, heterogeneity 0.22; core [0.107, 0.614, 0.612, 0.419] rim [0.268, 0.31, 0.607, 0.656]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.43, rim/outside 0.854 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.575)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 28.8 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.533)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 24.6 (aggregate of 149 individuals; 102/149 membrane-like individually; rim level 0.774)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.54, rim/outside 20.4 (aggregate of 149 individuals; 145/149 membrane-like individually; rim level 0.812)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #28 (t=8100, R_eq 9.37, ring): ['L link', 'membrane (wall)']; #29 (t=8100, R_eq 4.92): ['membrane (wall)']; #35 (t=8200, R_eq 10.82): ['membrane (wall)']; #69 (t=12400, R_eq 8.65, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 149 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
