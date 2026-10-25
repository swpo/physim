# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 1161s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1611-c16-review-fuelcell-res15/res15_chis0/seed2 --seeds 2 --size 192 192 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.85, 0.666], min area 6 px

## Measurements
- components: final 6, mean 2.1, max 6; occupancy final 0.05
- tracks: 10; persistent (alive >= 50% of run): 1; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 144.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 6, 6], H1 [1, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0489/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5029, -0.461, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 69: holes 0, rim-vs-core 0.24, rim-vs-outside 0.78, heterogeneity 0.11; core [1.0, 1.0, 0.995, 0.978] rim [0.855, 0.828, 0.951, 0.904]
  - track 3 at frame 161: holes 0, rim-vs-core 0.37, rim-vs-outside 0.54, heterogeneity 0.11; core [0.988, 0.979, 0.951, 0.942] rim [0.776, 0.703, 0.866, 0.831]
  - track 1 at frame 153: holes 0, rim-vs-core 0.19, rim-vs-outside 0.70, heterogeneity 0.11; core [0.967, 0.865, 0.988, 0.926] rim [0.844, 0.735, 0.94, 0.872]
  - track 4 at frame 175: holes 0, rim-vs-core 0.39, rim-vs-outside 0.54, heterogeneity 0.10; core [0.998, 0.983, 0.999, 0.999] rim [0.776, 0.668, 0.93, 0.971]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 2.96 (aggregate of 16 individuals; 5/16 membrane-like individually; rim level 0.476)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 4.04 (aggregate of 16 individuals; 5/16 membrane-like individually; rim level 0.441)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.54 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.791)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 1.73 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.81)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=345, R_eq 12.11): none; #3 (t=805, R_eq 8.1): none; #1 (t=765, R_eq 13.61, ring): ['phi (droplet)', 'order |Q|']; #4 (t=875, R_eq 7.88): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 16 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
