# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 539s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1619-c19-fuelcell-slowd-twins/chis0_Df0.5/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.865, 0.6421], min area 6 px

## Measurements
- components: final 20, mean 11.1, max 20; occupancy final 0.09
- tracks: 37; persistent (alive >= 50% of run): 10; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 43.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 20, 18], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0431/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.071, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.2127, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 114: holes 0, rim-vs-core 0.35, rim-vs-outside 0.42, heterogeneity 0.12; core [0.95, 0.87, 0.982, 0.968] rim [0.736, 0.613, 0.923, 0.89]
  - track 9 at frame 113: holes 0, rim-vs-core 0.29, rim-vs-outside 0.62, heterogeneity 0.10; core [0.958, 0.862, 0.974, 0.941] rim [0.804, 0.64, 0.939, 0.83]
  - track 10 at frame 124: holes 0, rim-vs-core 0.40, rim-vs-outside 0.41, heterogeneity 0.12; core [0.95, 0.922, 0.877, 0.899] rim [0.739, 0.637, 0.806, 0.724]
  - track 23 at frame 178: holes 0, rim-vs-core 0.45, rim-vs-outside 0.44, heterogeneity 0.12; core [0.966, 0.954, 0.871, 0.942] rim [0.734, 0.635, 0.791, 0.743]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 3.68 (aggregate of 78 individuals; 9/78 membrane-like individually; rim level 0.605)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 5.44 (aggregate of 78 individuals; 10/78 membrane-like individually; rim level 0.497)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.933, rim/outside 1.47 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.833)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 2.15 (aggregate of 78 individuals; 1/78 membrane-like individually; rim level 0.718)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=570, R_eq 4.75): none; #9 (t=565, R_eq 8.02, ring): none; #10 (t=620, R_eq 3.66): none; #23 (t=890, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
