# Evidence pack: phase-membrane (seed 13)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0721-c02-review-pm-damage/twin/seed13 --seeds 13 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5375], min area 6 px

## Measurements
- components: final 17, mean 14.6, max 24; occupancy final 0.34
- tracks: 156; persistent (alive >= 50% of run): 2; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.12 (1 = constant size)
- enclosures: components with a hole mean 9.50, final 12; holes at thresholds 0.2/0.35/0.5 final [3, 12, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [17, 17, 8]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0106/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 62, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.129, nucleations 0
- channel total drift (end/start - 1): [-0.5162, -0.6479, 0.1099, -0.0646]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 71 at frame 87: holes 1, rim-vs-core 0.19, rim-vs-outside 0.80, heterogeneity 0.17; core [0.067, 0.649, 0.373, 0.768] rim [0.144, 0.589, 0.483, 0.64]
  - track 87 at frame 89: holes 1, rim-vs-core 0.18, rim-vs-outside 0.87, heterogeneity 0.19; core [0.092, 0.792, 0.538, 0.59] rim [0.164, 0.63, 0.528, 0.613]
  - track 73 at frame 74: holes 1, rim-vs-core 0.30, rim-vs-outside 0.77, heterogeneity 0.20; core [0.108, 0.829, 0.619, 0.611] rim [0.204, 0.566, 0.505, 0.591]
  - track 100 at frame 94: holes 1, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.21; core [0.108, 0.81, 0.595, 0.625] rim [0.183, 0.655, 0.546, 0.589]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 13.2, rim/outside 0.833 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.463)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 4.96 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.733)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.74, rim/outside 3.97 (aggregate of 89 individuals; 77/89 membrane-like individually; rim level 0.57)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.33, rim/outside 4.03 (aggregate of 89 individuals; 77/89 membrane-like individually; rim level 0.612)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #71 (t=4350, R_eq 14.65): none; #87 (t=4450, R_eq 10.16, ring): ['L link', 'membrane (wall)']; #73 (t=3700, R_eq 9.15, ring): ['L link', 'membrane (wall)']; #100 (t=4700, R_eq 10.45, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
