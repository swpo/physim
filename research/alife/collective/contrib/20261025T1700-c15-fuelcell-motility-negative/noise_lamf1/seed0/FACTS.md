# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 682s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/lam1/shell_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8516, 0.6494], min area 6 px

## Measurements
- components: final 23, mean 13.7, max 24; occupancy final 0.08
- tracks: 64; persistent (alive >= 50% of run): 7; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 24, 22], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0641/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.348, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.1558, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 128: holes 0, rim-vs-core 0.48, rim-vs-outside 0.40, heterogeneity 0.14; core [0.933, 0.863, 0.461, 0.703] rim [0.739, 0.611, 0.8, 0.592]
  - track 8 at frame 92: holes 0, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.15; core [0.911, 0.73, 0.529, 0.789] rim [0.733, 0.534, 0.846, 0.617]
  - track 15 at frame 145: holes 0, rim-vs-core 0.47, rim-vs-outside 0.43, heterogeneity 0.14; core [0.931, 0.834, 0.467, 0.722] rim [0.745, 0.603, 0.805, 0.583]
  - track 46 at frame 182: holes 0, rim-vs-core 0.65, rim-vs-outside 0.59, heterogeneity 0.19; core [0.98, 0.962, 0.364, 1.0] rim [0.756, 0.666, 0.887, 0.894]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 4.11 (aggregate of 94 individuals; 1/94 membrane-like individually; rim level 0.649)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 6.17 (aggregate of 94 individuals; 2/94 membrane-like individually; rim level 0.554)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 2.31 (aggregate of 94 individuals; 45/94 membrane-like individually; rim level 0.607)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 2.48 (aggregate of 94 individuals; 1/94 membrane-like individually; rim level 0.566)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=640, R_eq 4.11): none; #8 (t=460, R_eq 5.47): none; #15 (t=725, R_eq 4.69): none; #46 (t=910, R_eq 4.37): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
