# Evidence pack: nematic-fuelcell (seed 5)

- world: `../../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 358s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2039-c23-audit-fuelcell/rerun/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.858, 0.646], min area 6 px

## Measurements
- components: final 26, mean 16.1, max 27; occupancy final 0.09
- tracks: 56; persistent (alive >= 50% of run): 8; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 27, 26], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.0537/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.136, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.1539, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 89: holes 0, rim-vs-core 0.44, rim-vs-outside 0.41, heterogeneity 0.16; core [0.884, 0.676, 0.565, 0.863] rim [0.714, 0.502, 0.869, 0.652]
  - track 1 at frame 84: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.15; core [0.892, 0.695, 0.542, 0.854] rim [0.723, 0.511, 0.849, 0.648]
  - track 2 at frame 84: holes 0, rim-vs-core 0.48, rim-vs-outside 0.41, heterogeneity 0.14; core [0.907, 0.763, 0.494, 0.795] rim [0.72, 0.532, 0.831, 0.635]
  - track 20 at frame 150: holes 0, rim-vs-core 0.44, rim-vs-outside 0.38, heterogeneity 0.15; core [0.898, 0.735, 0.507, 0.798] rim [0.725, 0.52, 0.819, 0.655]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 111 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.23 (aggregate of 111 individuals; 2/111 membrane-like individually; rim level 0.656)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 6.79 (aggregate of 111 individuals; 3/111 membrane-like individually; rim level 0.555)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 2.27 (aggregate of 111 individuals; 59/111 membrane-like individually; rim level 0.589)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 2.61 (aggregate of 111 individuals; 2/111 membrane-like individually; rim level 0.579)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=445, R_eq 5.92): none; #1 (t=420, R_eq 5.7): none; #2 (t=420, R_eq 4.79): none; #20 (t=750, R_eq 4.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
