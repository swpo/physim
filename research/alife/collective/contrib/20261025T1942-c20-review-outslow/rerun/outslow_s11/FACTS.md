# Evidence pack: nematic-fuelcell-outslow (seed 11)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 658s; status ok
- command: `python -m labkit.run /tmp/c20os/world.py --out /tmp/c20os/outslow --seeds 11 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8606, 0.696], min area 6 px

## Measurements
- components: final 28, mean 16.1, max 28; occupancy final 0.10
- tracks: 63; persistent (alive >= 50% of run): 6; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.39 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 28], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0674/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.16, nucleations 9
- channel total drift (end/start - 1): [-0.5045, -0.0113, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 119: holes 0, rim-vs-core 0.37, rim-vs-outside 0.37, heterogeneity 0.10; core [0.917, 0.848, 0.911, 0.849] rim [0.705, 0.563, 0.838, 0.767]
  - track 15 at frame 139: holes 0, rim-vs-core 0.42, rim-vs-outside 0.36, heterogeneity 0.11; core [0.931, 0.896, 0.902, 0.889] rim [0.698, 0.576, 0.822, 0.791]
  - track 19 at frame 138: holes 0, rim-vs-core 0.31, rim-vs-outside 0.59, heterogeneity 0.09; core [0.946, 0.833, 0.949, 0.876] rim [0.783, 0.565, 0.93, 0.863]
  - track 42 at frame 176: holes 0, rim-vs-core 0.40, rim-vs-outside 0.40, heterogeneity 0.11; core [0.942, 0.9, 0.931, 0.927] rim [0.722, 0.595, 0.853, 0.836]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 4.67 (aggregate of 112 individuals; 6/112 membrane-like individually; rim level 0.667)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 7.3 (aggregate of 112 individuals; 7/112 membrane-like individually; rim level 0.57)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.51 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.843)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.95 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.8)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=595, R_eq 4.33): none; #15 (t=695, R_eq 3.74): none; #19 (t=690, R_eq 7.65): none; #42 (t=880, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
