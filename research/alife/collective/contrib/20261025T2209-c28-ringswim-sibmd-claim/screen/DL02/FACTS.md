# Evidence pack: ringswim-waste-256 (seed 0)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 60 steps x dt 1.0 = time 12000; grid [128, 128]; wall 69s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/c28sd/DL02 --seeds 0 --size 128 128 --spf 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5381], min area 6 px

## Measurements
- components: final 7, mean 8.1, max 25; occupancy final 0.20
- tracks: 310; persistent (alive >= 50% of run): 0; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 5.95, final 5; holes at thresholds 0.2/0.35/0.5 final [2, 5, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 7, 7], H1 [7, 7, 5]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0409/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 1200, default): splits 99, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 82, merge/split ratio 0.828, nucleations 2
- channel total drift (end/start - 1): [-0.331, -0.7985, -0.2897, -0.4659]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 29: holes 1, rim-vs-core 0.44, rim-vs-outside 0.84, heterogeneity 0.25; core [0.137, 0.866, 0.681, 0.532] rim [0.3, 0.48, 0.553, 0.602]
  - track 79 at frame 39: holes 1, rim-vs-core 0.19, rim-vs-outside 0.79, heterogeneity 0.20; core [0.123, 0.675, 0.614, 0.718] rim [0.198, 0.571, 0.549, 0.6]
  - track 214 at frame 139: holes 1, rim-vs-core 0.18, rim-vs-outside 0.76, heterogeneity 0.22; core [0.082, 0.655, 0.496, 0.681] rim [0.195, 0.557, 0.534, 0.593]
  - track 6 at frame 17: holes 0, rim-vs-core 0.41, rim-vs-outside 0.84, heterogeneity 0.21; core [0.249, 0.804, 0.873, 0.818] rim [0.373, 0.523, 0.668, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 12.2, rim/outside 0.757 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.526)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 8.07 (aggregate of 43 individuals; 2/43 membrane-like individually; rim level 0.616)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.63, rim/outside 6.17 (aggregate of 43 individuals; 31/43 membrane-like individually; rim level 0.523)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.01, rim/outside 6.39 (aggregate of 43 individuals; 29/43 membrane-like individually; rim level 0.536)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #43 (t=1740, R_eq 8.48, ring): ['L link', 'membrane (wall)']; #79 (t=2340, R_eq 12.01, ring): ['K catalyst', 'L link', 'membrane (wall)']; #214 (t=8340, R_eq 11.95, ring): ['L link', 'membrane (wall)']; #6 (t=1020, R_eq 5.08): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 28 of 43 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
