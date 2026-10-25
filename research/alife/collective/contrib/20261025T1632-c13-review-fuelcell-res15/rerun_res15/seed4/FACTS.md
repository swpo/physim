# Evidence pack: nematic-fuelcell (seed 4)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 936s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1632-c13-review-fuelcell-res15/world.py --out collective/contrib/20261025T1632-c13-review-fuelcell-res15/rerun_res15/seed4 --seeds 4 --size 192 192 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8179, 0.5693], min area 6 px

## Measurements
- components: final 6, mean 3.0, max 7; occupancy final 0.04
- tracks: 16; persistent (alive >= 50% of run): 0; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 6, 6], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0554/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.143, nucleations 1
- channel total drift (end/start - 1): [-0.5014, -0.7089, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 155: holes 0, rim-vs-core 0.57, rim-vs-outside 0.69, heterogeneity 0.17; core [0.985, 0.888, 0.467, 0.985] rim [0.82, 0.579, 0.888, 0.847]
  - track 4 at frame 143: holes 0, rim-vs-core 0.43, rim-vs-outside 0.71, heterogeneity 0.15; core [0.997, 0.933, 0.528, 0.927] rim [0.842, 0.753, 0.85, 0.775]
  - track 0 at frame 55: holes 0, rim-vs-core 0.45, rim-vs-outside 0.73, heterogeneity 0.15; core [0.99, 0.963, 0.546, 0.952] rim [0.816, 0.78, 0.879, 0.778]
  - track 7 at frame 173: holes 0, rim-vs-core 0.43, rim-vs-outside 0.67, heterogeneity 0.16; core [0.991, 0.919, 0.527, 0.873] rim [0.846, 0.69, 0.849, 0.772]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 3.78 (aggregate of 20 individuals; 1/20 membrane-like individually; rim level 0.616)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 4.45 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.549)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 2.26 (aggregate of 20 individuals; 4/20 membrane-like individually; rim level 0.609)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 3.17 (aggregate of 20 individuals; 2/20 membrane-like individually; rim level 0.594)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=775, R_eq 7.82): none; #4 (t=715, R_eq 7.82, ring): none; #0 (t=275, R_eq 9.27): none; #7 (t=865, R_eq 7.31): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
