# Evidence pack: nematic-fuelcell (seed 24)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 667s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1834-c24-review-fuelring/world/seed24 --seeds 24 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8592, 0.6228], min area 6 px

## Measurements
- components: final 15, mean 8.1, max 15; occupancy final 0.08
- tracks: 29; persistent (alive >= 50% of run): 3; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 15, 14], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.034/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.091, nucleations 6
- channel total drift (end/start - 1): [-0.5028, -0.3593, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.55, rim-vs-outside 0.74, heterogeneity 0.14; core [0.987, 0.961, 0.347, 0.817] rim [0.822, 0.625, 0.747, 0.736]
  - track 5 at frame 114: holes 0, rim-vs-core 0.38, rim-vs-outside 0.77, heterogeneity 0.15; core [0.952, 0.737, 0.463, 0.947] rim [0.826, 0.618, 0.74, 0.754]
  - track 23 at frame 190: holes 0, rim-vs-core 0.60, rim-vs-outside 0.46, heterogeneity 0.16; core [0.976, 0.967, 0.383, 0.786] rim [0.766, 0.666, 0.836, 0.642]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 3.13 (aggregate of 56 individuals; 11/56 membrane-like individually; rim level 0.561)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 4.25 (aggregate of 56 individuals; 11/56 membrane-like individually; rim level 0.451)
  - radial shell s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.04 (aggregate of 56 individuals; 24/56 membrane-like individually; rim level 0.532)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 2.54 (aggregate of 56 individuals; 12/56 membrane-like individually; rim level 0.537)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 6.68, ring): none; #3 (t=545, R_eq 6.21, ring): none; #5 (t=570, R_eq 7.36, ring): ['phi (droplet)', 'order |Q|', 'shell s', 'fuel f']; #23 (t=950, R_eq 3.14): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 56 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
