# Evidence pack: nematic-fuelcell (seed 31)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 513s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2105-c25-review-fuelring-slowd/controls/slowD03_s31 --seeds 31 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8615, 0.6106], min area 6 px

## Measurements
- components: final 22, mean 9.8, max 22; occupancy final 0.09
- tracks: 49; persistent (alive >= 50% of run): 4; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 45.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 24, 21], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.041/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.1, nucleations 7
- channel total drift (end/start - 1): [-0.4988, -0.2506, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 104: holes 0, rim-vs-core 0.39, rim-vs-outside 0.67, heterogeneity 0.10; core [0.992, 0.944, 0.933, 0.953] rim [0.827, 0.616, 0.92, 0.82]
  - track 1 at frame 96: holes 0, rim-vs-core 0.23, rim-vs-outside 0.69, heterogeneity 0.09; core [0.951, 0.765, 0.987, 0.947] rim [0.82, 0.624, 0.947, 0.829]
  - track 2 at frame 82: holes 0, rim-vs-core 0.28, rim-vs-outside 0.65, heterogeneity 0.10; core [0.959, 0.794, 0.979, 0.948] rim [0.817, 0.596, 0.94, 0.815]
  - track 32 at frame 190: holes 0, rim-vs-core 0.30, rim-vs-outside 0.57, heterogeneity 0.12; core [0.961, 0.945, 0.868, 0.906] rim [0.808, 0.743, 0.821, 0.76]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 3.13 (aggregate of 69 individuals; 8/69 membrane-like individually; rim level 0.546)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 4.39 (aggregate of 69 individuals; 8/69 membrane-like individually; rim level 0.451)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 1.42 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.81)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 2.31 (aggregate of 69 individuals; 5/69 membrane-like individually; rim level 0.642)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=520, R_eq 6.33): none; #1 (t=480, R_eq 8.52, ring): ['phi (droplet)', 'order |Q|', 'fuel f']; #2 (t=410, R_eq 7.74, ring): ['phi (droplet)', 'order |Q|']; #32 (t=950, R_eq 3.34): none

## Warnings
- radial: 16 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
