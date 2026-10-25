# Evidence pack: nematic-fuelcell-srcin (seed 5)

- world: `../world_srcin.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 497s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2005-c21-audit-fuelcell/world_srcin.py --out collective/contrib/20261025T2005-c21-audit-fuelcell/srcin_ks074 --seeds 5 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8655, 0.6869], min area 6 px

## Measurements
- components: final 21, mean 13.1, max 22; occupancy final 0.10
- tracks: 42; persistent (alive >= 50% of run): 9; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 54.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 23, 21], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0452/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.133, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.0734, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.42, rim-vs-outside 0.39, heterogeneity 0.14; core [0.886, 0.686, 0.636, 0.781] rim [0.698, 0.489, 0.899, 0.602]
  - track 2 at frame 108: holes 0, rim-vs-core 0.44, rim-vs-outside 0.39, heterogeneity 0.15; core [0.91, 0.767, 0.594, 0.812] rim [0.726, 0.552, 0.884, 0.635]
  - track 9 at frame 108: holes 0, rim-vs-core 0.46, rim-vs-outside 0.67, heterogeneity 0.15; core [0.946, 0.827, 0.476, 0.788] rim [0.778, 0.562, 0.795, 0.7]
  - track 16 at frame 160: holes 0, rim-vs-core 0.54, rim-vs-outside 0.41, heterogeneity 0.15; core [0.947, 0.924, 0.512, 0.796] rim [0.723, 0.603, 0.847, 0.641]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.06 (aggregate of 91 individuals; 5/91 membrane-like individually; rim level 0.612)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 6.25 (aggregate of 91 individuals; 6/91 membrane-like individually; rim level 0.509)
  - radial shell s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 2.96 (aggregate of 91 individuals; 34/91 membrane-like individually; rim level 0.628)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 2.04 (aggregate of 91 individuals; 1/91 membrane-like individually; rim level 0.574)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 5.92, ring): none; #2 (t=540, R_eq 5.14): none; #9 (t=540, R_eq 9.3, ring): ['phi (droplet)', 'order |Q|']; #16 (t=800, R_eq 3.61): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 91 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
