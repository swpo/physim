# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 200 steps x dt 0.025 (--dt; world META dt 0.05) = time 1000; grid [128, 128]; wall 1318s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/dt2_s0 --seeds 0 --spf 200 --dt 0.025 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8554, 0.6669], min area 6 px

## Measurements
- components: final 24, mean 13.7, max 24; occupancy final 0.08
- tracks: 46; persistent (alive >= 50% of run): 7; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 29.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 23, 23], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.0652/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.056, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.2091, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 108: holes 0, rim-vs-core 0.36, rim-vs-outside 0.71, heterogeneity 0.15; core [0.914, 0.686, 0.469, 0.889] rim [0.784, 0.551, 0.744, 0.742]
  - track 5 at frame 97: holes 0, rim-vs-core 0.46, rim-vs-outside 0.73, heterogeneity 0.14; core [0.948, 0.837, 0.391, 0.838] rim [0.795, 0.589, 0.732, 0.746]
  - track 6 at frame 97: holes 0, rim-vs-core 0.44, rim-vs-outside 0.71, heterogeneity 0.16; core [0.934, 0.76, 0.415, 0.857] rim [0.782, 0.551, 0.753, 0.731]
  - track 31 at frame 185: holes 0, rim-vs-core 0.60, rim-vs-outside 0.44, heterogeneity 0.17; core [0.939, 0.915, 0.432, 0.851] rim [0.707, 0.583, 0.834, 0.659]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.37 (aggregate of 93 individuals; 6/93 membrane-like individually; rim level 0.657)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 7.15 (aggregate of 93 individuals; 7/93 membrane-like individually; rim level 0.564)
  - radial shell s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.25 (aggregate of 93 individuals; 54/93 membrane-like individually; rim level 0.58)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 2.69 (aggregate of 93 individuals; 6/93 membrane-like individually; rim level 0.569)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=540, R_eq 6.1, ring): none; #5 (t=485, R_eq 6.91): none; #6 (t=485, R_eq 7.65, ring): none; #31 (t=925, R_eq 4.07): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
