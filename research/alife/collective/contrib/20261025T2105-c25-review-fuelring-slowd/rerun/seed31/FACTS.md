# Evidence pack: nematic-fuelcell (seed 31)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 510s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2105-c25-review-fuelring-slowd/rerun/seed31 --seeds 31 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8564, 0.6341], min area 6 px

## Measurements
- components: final 22, mean 11.9, max 22; occupancy final 0.09
- tracks: 45; persistent (alive >= 50% of run): 6; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 42.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 23, 21], H1 [1, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0457/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.111, nucleations 7
- channel total drift (end/start - 1): [-0.4988, -0.2265, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 91: holes 0, rim-vs-core 0.41, rim-vs-outside 0.75, heterogeneity 0.15; core [0.943, 0.749, 0.409, 0.86] rim [0.806, 0.564, 0.734, 0.754]
  - track 9 at frame 145: holes 0, rim-vs-core 0.45, rim-vs-outside 0.50, heterogeneity 0.15; core [0.947, 0.889, 0.442, 0.738] rim [0.777, 0.665, 0.775, 0.61]
  - track 10 at frame 145: holes 0, rim-vs-core 0.49, rim-vs-outside 0.44, heterogeneity 0.15; core [0.917, 0.758, 0.528, 0.848] rim [0.732, 0.538, 0.878, 0.653]
  - track 25 at frame 166: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.15; core [0.915, 0.812, 0.506, 0.784] rim [0.778, 0.647, 0.744, 0.675]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 3.86 (aggregate of 81 individuals; 7/81 membrane-like individually; rim level 0.615)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 5.74 (aggregate of 81 individuals; 9/81 membrane-like individually; rim level 0.521)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 2.19 (aggregate of 81 individuals; 31/81 membrane-like individually; rim level 0.556)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 2.49 (aggregate of 81 individuals; 8/81 membrane-like individually; rim level 0.545)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=455, R_eq 8.23, ring): ['phi (droplet)', 'order |Q|', 'shell s', 'fuel f']; #9 (t=725, R_eq 4.48): none; #10 (t=725, R_eq 6, ring): none; #25 (t=830, R_eq 4.18): none

## Warnings
- radial: 19 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
