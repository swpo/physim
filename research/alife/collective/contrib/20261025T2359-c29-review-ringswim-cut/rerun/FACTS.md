# Evidence pack: ringswim-dl2 (seed 9)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 289s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2359-c29-review-ringswim-cut/world.py --out collective/contrib/20261025T2359-c29-review-ringswim-cut/rerun --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5355], min area 6 px

## Measurements
- components: final 25, mean 33.7, max 114; occupancy final 0.22
- tracks: 886; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 24.16, final 22; holes at thresholds 0.2/0.35/0.5 final [12, 28, 30]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 28, 25], H1 [32, 30, 24]
- motion: 77 long-lived tracks moved >= 1 body length; max speed 0.0561/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 1000, default): splits 279, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 216, merge/split ratio 0.774, nucleations 1
- channel total drift (end/start - 1): [-0.3695, -0.7858, -0.2301, -0.3941]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 171 at frame 42: holes 0, rim-vs-core 0.24, rim-vs-outside 0.88, heterogeneity 0.16; core [0.097, 0.666, 0.532, 0.774] rim [0.248, 0.505, 0.597, 0.692]
  - track 657 at frame 161: holes 1, rim-vs-core 0.19, rim-vs-outside 0.80, heterogeneity 0.17; core [0.077, 0.616, 0.441, 0.724] rim [0.181, 0.502, 0.504, 0.642]
  - track 30 at frame 34: holes 1, rim-vs-core 0.17, rim-vs-outside 0.81, heterogeneity 0.19; core [0.094, 0.683, 0.539, 0.691] rim [0.177, 0.552, 0.528, 0.625]
  - track 819 at frame 188: holes 1, rim-vs-core 0.21, rim-vs-outside 0.82, heterogeneity 0.22; core [0.118, 0.774, 0.609, 0.594] rim [0.203, 0.591, 0.565, 0.596]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 179 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 7.63, rim/outside 0.72 (aggregate of 179 individuals; 0/179 membrane-like individually; rim level 0.488)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 8.57 (aggregate of 179 individuals; 27/179 membrane-like individually; rim level 0.59)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 5.94 (aggregate of 179 individuals; 132/179 membrane-like individually; rim level 0.485)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.04, rim/outside 6.59 (aggregate of 179 individuals; 131/179 membrane-like individually; rim level 0.501)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #171 (t=2100, R_eq 8.25): ['L link']; #657 (t=8050, R_eq 11.17): ['L link']; #30 (t=1700, R_eq 10.17, ring): ['L link', 'membrane (wall)']; #819 (t=9400, R_eq 10.93, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 114 of 179 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
