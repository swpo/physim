# Evidence pack: nematic-fuelcell (seed 5)

- world: `../../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 200 steps x dt 0.025 (--dt; world META dt 0.05) = time 1000; grid [128, 128]; wall 629s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2039-c23-audit-fuelcell/dt2/seed5 --seeds 5 --spf 200 --dt 0.025 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8579, 0.6534], min area 6 px

## Measurements
- components: final 28, mean 16.1, max 29; occupancy final 0.09
- tracks: 51; persistent (alive >= 50% of run): 12; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 33.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 28, 28], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.0488/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.05, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.1429, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.14; core [0.895, 0.657, 0.54, 0.82] rim [0.714, 0.475, 0.864, 0.633]
  - track 2 at frame 108: holes 0, rim-vs-core 0.48, rim-vs-outside 0.42, heterogeneity 0.14; core [0.92, 0.777, 0.479, 0.818] rim [0.74, 0.564, 0.826, 0.652]
  - track 5 at frame 87: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.15; core [0.899, 0.713, 0.537, 0.867] rim [0.73, 0.524, 0.863, 0.68]
  - track 26 at frame 160: holes 0, rim-vs-core 0.58, rim-vs-outside 0.44, heterogeneity 0.16; core [0.953, 0.94, 0.369, 0.789] rim [0.738, 0.638, 0.795, 0.648]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 110 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 4.21 (aggregate of 110 individuals; 5/110 membrane-like individually; rim level 0.652)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 6.79 (aggregate of 110 individuals; 6/110 membrane-like individually; rim level 0.555)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 2.28 (aggregate of 110 individuals; 59/110 membrane-like individually; rim level 0.587)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 2.58 (aggregate of 110 individuals; 6/110 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 5.64, ring): none; #2 (t=540, R_eq 5.01): none; #5 (t=435, R_eq 5.84): none; #26 (t=800, R_eq 3.43): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.025 only relabels time (world META dt 0.05): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 14 of 110 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
