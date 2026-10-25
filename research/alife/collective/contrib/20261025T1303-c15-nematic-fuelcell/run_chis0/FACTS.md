# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 721s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z35/chis0 --seeds 0 --no-movie`
- segmentation: matter > 0.54 of robust range [-0.8819, 0.7384], min area 6 px

## Measurements
- components: final 9, mean 9.0, max 12; occupancy final 0.10
- tracks: 17; persistent (alive >= 50% of run): 8; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 34.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 10, 9], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0692/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 100, default): splits 3, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.667, nucleations 9
- channel total drift (end/start - 1): [-0.5044, 0.0321, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 108: holes 0, rim-vs-core 0.29, rim-vs-outside 0.62, heterogeneity 0.10; core [0.936, 0.841, 0.959, 0.914] rim [0.771, 0.624, 0.907, 0.847]
  - track 5 at frame 111: holes 0, rim-vs-core 0.32, rim-vs-outside 0.67, heterogeneity 0.11; core [0.962, 0.919, 0.978, 0.973] rim [0.782, 0.681, 0.914, 0.888]
  - track 6 at frame 111: holes 0, rim-vs-core 0.29, rim-vs-outside 0.64, heterogeneity 0.10; core [0.944, 0.867, 0.974, 0.949] rim [0.769, 0.654, 0.906, 0.871]
  - track 9 at frame 131: holes 0, rim-vs-core 0.46, rim-vs-outside 0.38, heterogeneity 0.12; core [0.943, 0.909, 0.894, 0.949] rim [0.686, 0.568, 0.788, 0.826]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 3.47 (aggregate of 59 individuals; 3/59 membrane-like individually; rim level 0.53)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.706, rim/outside 4.96 (aggregate of 59 individuals; 3/59 membrane-like individually; rim level 0.454)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 1.57 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.805)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 1.57 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.802)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=540, R_eq 8.46, ring): none; #5 (t=555, R_eq 7.42): none; #6 (t=555, R_eq 7.98): none; #9 (t=655, R_eq 4.3): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
