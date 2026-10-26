# Evidence pack: ringswim-dl2 (seed 11)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 308s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0108-c29-review-local-drive/world.py --out collective/contrib/20261026T0108-c29-review-local-drive/pack_kd03 --seeds 11 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5714], min area 6 px

## Measurements
- components: final 83, mean 74.1, max 115; occupancy final 0.22
- tracks: 1278; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [88, 85, 83], H1 [67, 13, 0]
- motion: 193 long-lived tracks moved >= 1 body length; max speed 0.0392/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 1000, default): splits 556, persistent splits 105 (0 more failed only because the siblings re-merged within K), max generation 5, merges 25, merge/split ratio 0.045, nucleations 1
- channel total drift (end/start - 1): [-0.3219, -0.8165, -0.1367, -0.2314]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 438 at frame 87: holes 0, rim-vs-core 0.42, rim-vs-outside 0.95, heterogeneity 0.19; core [0.095, 0.809, 0.653, 0.723] rim [0.34, 0.466, 0.646, 0.717]
  - track 867 at frame 165: holes 0, rim-vs-core 0.44, rim-vs-outside 0.71, heterogeneity 0.17; core [0.115, 0.74, 0.681, 0.893] rim [0.277, 0.456, 0.609, 0.61]
  - track 482 at frame 89: holes 0, rim-vs-core 0.38, rim-vs-outside 0.71, heterogeneity 0.16; core [0.093, 0.667, 0.575, 0.862] rim [0.288, 0.465, 0.618, 0.605]
  - track 1089 at frame 182: holes 0, rim-vs-core 0.40, rim-vs-outside 0.94, heterogeneity 0.18; core [0.091, 0.787, 0.641, 0.744] rim [0.324, 0.463, 0.635, 0.71]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 469 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.33, rim/outside 0.861 (aggregate of 469 individuals; 0/469 membrane-like individually; rim level 0.525)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.933, rim/outside 7.34 (aggregate of 469 individuals; 13/469 membrane-like individually; rim level 0.689)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.69 (aggregate of 469 individuals; 213/469 membrane-like individually; rim level 0.733)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 7.34 (aggregate of 469 individuals; 165/469 membrane-like individually; rim level 0.807)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #438 (t=4350, R_eq 7.48): ['L link', 'membrane (wall)']; #867 (t=8250, R_eq 7.46): none; #482 (t=4450, R_eq 8.21): ['L link']; #1089 (t=9100, R_eq 7.51): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 469 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
