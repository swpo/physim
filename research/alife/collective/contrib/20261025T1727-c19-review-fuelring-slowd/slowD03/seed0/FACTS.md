# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 513s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1727-c19-review-fuelring-slowd/slowD03/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8553, 0.6092], min area 6 px

## Measurements
- components: final 20, mean 11.1, max 20; occupancy final 0.08
- tracks: 34; persistent (alive >= 50% of run): 8; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 20, 18], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0474/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.083, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.2936, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 109: holes 0, rim-vs-core 0.35, rim-vs-outside 0.50, heterogeneity 0.10; core [0.988, 0.962, 1.0, 1.0] rim [0.77, 0.7, 0.966, 0.918]
  - track 5 at frame 94: holes 0, rim-vs-core 0.28, rim-vs-outside 0.68, heterogeneity 0.09; core [0.973, 0.855, 0.975, 0.98] rim [0.831, 0.658, 0.935, 0.836]
  - track 8 at frame 101: holes 0, rim-vs-core 0.31, rim-vs-outside 0.38, heterogeneity 0.10; core [0.92, 0.758, 0.954, 0.888] rim [0.744, 0.556, 0.899, 0.743]
  - track 12 at frame 133: holes 0, rim-vs-core 0.35, rim-vs-outside 0.37, heterogeneity 0.11; core [0.922, 0.828, 0.948, 0.905] rim [0.739, 0.592, 0.886, 0.736]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 3.44 (aggregate of 76 individuals; 8/76 membrane-like individually; rim level 0.591)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 4.73 (aggregate of 76 individuals; 9/76 membrane-like individually; rim level 0.485)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 1.44 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.839)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 2.44 (aggregate of 76 individuals; 1/76 membrane-like individually; rim level 0.67)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=545, R_eq 4.41): none; #5 (t=470, R_eq 6.6): none; #8 (t=505, R_eq 5.7): none; #12 (t=665, R_eq 5.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
