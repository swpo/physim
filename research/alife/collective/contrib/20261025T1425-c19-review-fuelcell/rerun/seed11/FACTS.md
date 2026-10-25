# Evidence pack: nematic-fuelcell (seed 11)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 569s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1425-c19-review-fuelcell/rerun/seed11 --seeds 11 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8566, 0.6662], min area 6 px

## Measurements
- components: final 25, mean 15.6, max 27; occupancy final 0.09
- tracks: 57; persistent (alive >= 50% of run): 7; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 25, 25], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0554/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.087, nucleations 9
- channel total drift (end/start - 1): [-0.5045, -0.1524, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 133: holes 0, rim-vs-core 0.66, rim-vs-outside 0.51, heterogeneity 0.19; core [0.962, 0.891, 0.411, 0.992] rim [0.723, 0.509, 0.861, 0.827]
  - track 11 at frame 133: holes 0, rim-vs-core 0.51, rim-vs-outside 0.39, heterogeneity 0.15; core [0.915, 0.796, 0.478, 0.718] rim [0.713, 0.536, 0.844, 0.575]
  - track 5 at frame 81: holes 0, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.14; core [0.891, 0.71, 0.538, 0.82] rim [0.719, 0.506, 0.852, 0.638]
  - track 45 at frame 176: holes 0, rim-vs-core 0.60, rim-vs-outside 0.42, heterogeneity 0.17; core [0.937, 0.91, 0.409, 0.758] rim [0.698, 0.575, 0.813, 0.596]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 4.02 (aggregate of 107 individuals; 5/107 membrane-like individually; rim level 0.638)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 6.13 (aggregate of 107 individuals; 5/107 membrane-like individually; rim level 0.531)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 2.25 (aggregate of 107 individuals; 55/107 membrane-like individually; rim level 0.586)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 2.5 (aggregate of 107 individuals; 6/107 membrane-like individually; rim level 0.543)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=665, R_eq 4.48): ['shell s']; #11 (t=665, R_eq 4.15): none; #5 (t=405, R_eq 5.84): none; #45 (t=880, R_eq 3.7): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
