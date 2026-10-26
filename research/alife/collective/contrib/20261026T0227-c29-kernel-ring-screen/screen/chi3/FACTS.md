# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi3 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5831], min area 6 px

## Measurements
- components: final 26, mean 24.8, max 45; occupancy final 0.19
- tracks: 360; persistent (alive >= 50% of run): 0; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 26, 26], H1 [12, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.0315/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 1000, default): splits 153, persistent splits 36 (0 more failed only because the siblings re-merged within K), max generation 6, merges 19, merge/split ratio 0.124, nucleations 0
- channel total drift (end/start - 1): [-0.3608, -0.833, -0.0986, -0.3822]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 170 at frame 124: holes 0, rim-vs-core 0.79, rim-vs-outside 0.59, heterogeneity 0.22; core [0.201, 0.88, 0.805, 0.795] rim [0.416, 0.259, 0.424, 0.568]
  - track 257 at frame 160: holes 0, rim-vs-core 0.37, rim-vs-outside 0.77, heterogeneity 0.14; core [0.093, 0.68, 0.586, 0.893] rim [0.257, 0.469, 0.584, 0.642]
  - track 262 at frame 161: holes 0, rim-vs-core 0.40, rim-vs-outside 0.77, heterogeneity 0.14; core [0.109, 0.682, 0.622, 0.942] rim [0.268, 0.476, 0.59, 0.644]
  - track 309 at frame 165: holes 0, rim-vs-core 0.70, rim-vs-outside 0.56, heterogeneity 0.19; core [0.184, 0.814, 0.776, 0.84] rim [0.373, 0.299, 0.453, 0.541]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.11, rim/outside 0.897 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.494)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 6.51 (aggregate of 155 individuals; 6/155 membrane-like individually; rim level 0.706)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 5.45 (aggregate of 155 individuals; 93/155 membrane-like individually; rim level 0.749)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 6.39 (aggregate of 155 individuals; 48/155 membrane-like individually; rim level 0.855)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #170 (t=6200, R_eq 5.61): ['L link', 'membrane (wall)']; #257 (t=8000, R_eq 7.11): ['L link']; #262 (t=8050, R_eq 7): none; #309 (t=8250, R_eq 5.53): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
