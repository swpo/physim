# Evidence pack: ringswim-waste (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 17s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/wtilt/a0/seed4 --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5351], min area 6 px

## Measurements
- components: final 16, mean 14.8, max 20; occupancy final 0.26
- tracks: 161; persistent (alive >= 50% of run): 1; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.56 (1 = constant size)
- enclosures: components with a hole mean 9.12, final 12; holes at thresholds 0.2/0.35/0.5 final [3, 12, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [16, 13, 11]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00765/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 66, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.076, nucleations 0
- channel total drift (end/start - 1): [-0.4217, -0.7443, -0.094, -0.3274]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 76 at frame 114: holes 0, rim-vs-core 0.47, rim-vs-outside 0.92, heterogeneity 0.24; core [0.103, 0.885, 0.672, 0.507] rim [0.291, 0.491, 0.553, 0.647]
  - track 69 at frame 101: holes 1, rim-vs-core 0.22, rim-vs-outside 0.83, heterogeneity 0.20; core [0.101, 0.809, 0.621, 0.59] rim [0.177, 0.609, 0.558, 0.609]
  - track 61 at frame 86: holes 1, rim-vs-core 0.20, rim-vs-outside 0.85, heterogeneity 0.19; core [0.104, 0.785, 0.624, 0.62] rim [0.173, 0.611, 0.562, 0.617]
  - track 113 at frame 168: holes 0, rim-vs-core 0.41, rim-vs-outside 0.97, heterogeneity 0.19; core [0.093, 0.81, 0.609, 0.61] rim [0.283, 0.472, 0.629, 0.735]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.817 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.49)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 8.15 (aggregate of 92 individuals; 2/92 membrane-like individually; rim level 0.701)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 5.96 (aggregate of 92 individuals; 74/92 membrane-like individually; rim level 0.619)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.03, rim/outside 6.22 (aggregate of 92 individuals; 69/92 membrane-like individually; rim level 0.647)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #76 (t=5700, R_eq 8.44, ring): ['L link', 'membrane (wall)']; #69 (t=5050, R_eq 11.31, ring): ['L link', 'membrane (wall)']; #61 (t=4300, R_eq 10.54, ring): ['L link', 'membrane (wall)']; #113 (t=8400, R_eq 7.42): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 92 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
