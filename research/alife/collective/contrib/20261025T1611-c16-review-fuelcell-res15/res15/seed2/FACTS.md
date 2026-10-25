# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 1216s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1611-c16-review-fuelcell-res15/res15/seed2 --seeds 2 --size 192 192 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.823, 0.5738], min area 6 px

## Measurements
- components: final 6, mean 2.9, max 7; occupancy final 0.04
- tracks: 15; persistent (alive >= 50% of run): 0; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 7, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5029, -0.6906, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 114: holes 0, rim-vs-core 0.40, rim-vs-outside 0.89, heterogeneity 0.16; core [1.0, 0.89, 0.498, 0.935] rim [0.868, 0.705, 0.796, 0.809]
  - track 0 at frame 47: holes 0, rim-vs-core 0.43, rim-vs-outside 0.75, heterogeneity 0.15; core [0.998, 0.989, 0.487, 0.87] rim [0.844, 0.835, 0.835, 0.728]
  - track 5 at frame 170: holes 0, rim-vs-core 0.38, rim-vs-outside 0.75, heterogeneity 0.15; core [0.997, 0.983, 0.483, 0.888] rim [0.866, 0.868, 0.794, 0.76]
  - track 6 at frame 170: holes 0, rim-vs-core 0.59, rim-vs-outside 0.83, heterogeneity 0.17; core [1.0, 1.0, 0.341, 1.0] rim [0.854, 0.838, 0.88, 0.891]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 3.22 (aggregate of 20 individuals; 2/20 membrane-like individually; rim level 0.568)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 3.86 (aggregate of 20 individuals; 2/20 membrane-like individually; rim level 0.471)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 2.03 (aggregate of 20 individuals; 3/20 membrane-like individually; rim level 0.559)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.734, rim/outside 2.79 (aggregate of 20 individuals; 2/20 membrane-like individually; rim level 0.495)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=570, R_eq 11.73): none; #0 (t=235, R_eq 9.49): none; #5 (t=850, R_eq 8.48): none; #6 (t=850, R_eq 6.65): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
