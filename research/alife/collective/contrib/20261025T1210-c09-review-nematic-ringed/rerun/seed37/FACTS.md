# Evidence pack: active-nematic-droplets (seed 37)

- world: `../../../20261025T1141-c11-active-nematic-ringed/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 319s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py --out collective/contrib/20261025T1210-c09-review-nematic-ringed/rerun/seed37 --seeds 37 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8257, 0.6224], min area 6 px

## Measurements
- components: final 30, mean 22.4, max 33; occupancy final 0.07
- tracks: 127; persistent (alive >= 50% of run): 7; longest 177 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 28], H1 [0, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.0918/time; max body lengths 5.4
- replication (lineage window K = 20 frames = time 100, default): splits 49, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 4, merges 18, merge/split ratio 0.367, nucleations 11
- channel total drift (end/start - 1): [-0.4884, -0.4045, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 113: holes 0, rim-vs-core 0.37, rim-vs-outside 0.28, heterogeneity 0.13; core [0.882, 0.759, 0.471] rim [0.718, 0.533, 0.719]
  - track 14 at frame 114: holes 0, rim-vs-core 0.57, rim-vs-outside 0.38, heterogeneity 0.18; core [0.955, 0.937, 0.428] rim [0.725, 0.614, 0.832]
  - track 21 at frame 118: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.15; core [0.942, 0.885, 0.423] rim [0.76, 0.631, 0.731]
  - track 96 at frame 178: holes 0, rim-vs-core 0.46, rim-vs-outside 0.34, heterogeneity 0.16; core [0.935, 0.903, 0.429] rim [0.745, 0.627, 0.745]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 4.76 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.762)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.76, rim/outside 8.21 (aggregate of 150 individuals; 2/150 membrane-like individually; rim level 0.647)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 2.11 (aggregate of 150 individuals; 114/150 membrane-like individually; rim level 0.65)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #9 (t=565, R_eq 3.19): none; #14 (t=570, R_eq 3.19): ['surfactant s']; #21 (t=590, R_eq 3.39): ['surfactant s']; #96 (t=890, R_eq 3.52): none

## Warnings
- radial: 4 of 150 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
