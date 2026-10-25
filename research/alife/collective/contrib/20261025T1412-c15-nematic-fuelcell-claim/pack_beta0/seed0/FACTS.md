# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 658s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/beta0_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8751, 0.7197], min area 6 px

## Measurements
- components: final 15, mean 10.2, max 15; occupancy final 0.10
- tracks: 24; persistent (alive >= 50% of run): 10; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 35.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 16, 15], H1 [1, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0287/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.143, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.0647, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 111: holes 0, rim-vs-core 0.54, rim-vs-outside 0.64, heterogeneity 0.15; core [0.967, 0.915, 0.265, 0.969] rim [0.793, 0.668, 0.706, 0.902]
  - track 4 at frame 104: holes 0, rim-vs-core 0.42, rim-vs-outside 0.63, heterogeneity 0.14; core [0.94, 0.822, 0.328, 0.926] rim [0.799, 0.661, 0.68, 0.857]
  - track 8 at frame 114: holes 0, rim-vs-core 0.46, rim-vs-outside 0.60, heterogeneity 0.15; core [0.947, 0.863, 0.323, 0.934] rim [0.793, 0.646, 0.696, 0.883]
  - track 9 at frame 126: holes 0, rim-vs-core 0.67, rim-vs-outside 0.35, heterogeneity 0.18; core [0.936, 0.905, 0.367, 0.949] rim [0.674, 0.555, 0.857, 0.831]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 3.7 (aggregate of 69 individuals; 6/69 membrane-like individually; rim level 0.57)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 5.26 (aggregate of 69 individuals; 6/69 membrane-like individually; rim level 0.479)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 2.34 (aggregate of 69 individuals; 32/69 membrane-like individually; rim level 0.524)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.5 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.821)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=555, R_eq 7.48): none; #4 (t=520, R_eq 6.6, ring): none; #8 (t=570, R_eq 6.56, ring): none; #9 (t=630, R_eq 4.11): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
