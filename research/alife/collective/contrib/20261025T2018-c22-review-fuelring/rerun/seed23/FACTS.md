# Evidence pack: nematic-fuelcell (seed 23)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 375s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2030-c22-review-fuelring/rerun/seed23 --seeds 23 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8567, 0.6778], min area 6 px

## Measurements
- components: final 28, mean 16.7, max 29; occupancy final 0.09
- tracks: 65; persistent (alive >= 50% of run): 13; longest 144 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 28], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.0497/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.115, nucleations 10
- channel total drift (end/start - 1): [-0.4914, -0.1686, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 96: holes 0, rim-vs-core 0.43, rim-vs-outside 0.46, heterogeneity 0.15; core [0.912, 0.83, 0.478, 0.682] rim [0.741, 0.612, 0.777, 0.561]
  - track 8 at frame 91: holes 0, rim-vs-core 0.61, rim-vs-outside 0.43, heterogeneity 0.19; core [0.949, 0.656, 0.44, 0.972] rim [0.704, 0.418, 0.888, 0.735]
  - track 1 at frame 77: holes 0, rim-vs-core 0.44, rim-vs-outside 0.69, heterogeneity 0.14; core [0.945, 0.784, 0.381, 0.816] rim [0.794, 0.548, 0.718, 0.742]
  - track 50 at frame 183: holes 0, rim-vs-core 0.60, rim-vs-outside 0.41, heterogeneity 0.17; core [0.943, 0.915, 0.393, 0.703] rim [0.705, 0.592, 0.819, 0.58]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4 (aggregate of 112 individuals; 5/112 membrane-like individually; rim level 0.634)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 6.1 (aggregate of 112 individuals; 6/112 membrane-like individually; rim level 0.528)
  - radial shell s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 2.23 (aggregate of 112 individuals; 57/112 membrane-like individually; rim level 0.576)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 2.47 (aggregate of 112 individuals; 7/112 membrane-like individually; rim level 0.537)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=480, R_eq 4.65): none; #8 (t=455, R_eq 4.55): ['shell s']; #1 (t=385, R_eq 6.7, ring): ['phi (droplet)', 'order |Q|', 'shell s', 'fuel f']; #50 (t=915, R_eq 3.48): ['shell s']

## Warnings
- radial: 13 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
