# Evidence pack: nematic-fuelcell (seed 4)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 936s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1632-c13-review-fuelcell-res15/world.py --out collective/contrib/20261025T1632-c13-review-fuelcell-res15/rerun_res15_chis0/seed4 --seeds 4 --size 192 192 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8482, 0.6696], min area 6 px

## Measurements
- components: final 7, mean 2.1, max 7; occupancy final 0.05
- tracks: 13; persistent (alive >= 50% of run): 1; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 145.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 7, 7], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0686/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5014, -0.4822, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 82: holes 0, rim-vs-core 0.30, rim-vs-outside 0.69, heterogeneity 0.11; core [0.998, 0.999, 0.996, 0.979] rim [0.825, 0.79, 0.938, 0.874]
  - track 4 at frame 173: holes 0, rim-vs-core 0.40, rim-vs-outside 0.51, heterogeneity 0.12; core [0.985, 0.978, 0.947, 0.933] rim [0.767, 0.688, 0.854, 0.805]
  - track 6 at frame 175: holes 0, rim-vs-core 0.38, rim-vs-outside 0.53, heterogeneity 0.11; core [0.991, 0.986, 0.96, 0.953] rim [0.785, 0.706, 0.868, 0.829]
  - track 8 at frame 180: holes 0, rim-vs-core 0.37, rim-vs-outside 0.53, heterogeneity 0.11; core [0.992, 0.984, 0.97, 0.967] rim [0.79, 0.708, 0.876, 0.849]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 4.06 (aggregate of 16 individuals; 1/16 membrane-like individually; rim level 0.585)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.754, rim/outside 6.08 (aggregate of 16 individuals; 1/16 membrane-like individually; rim level 0.541)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 1.62 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.835)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 1.86 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.841)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=410, R_eq 12.46): none; #4 (t=865, R_eq 7.51): none; #6 (t=875, R_eq 7.46): none; #8 (t=900, R_eq 7.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 16 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
