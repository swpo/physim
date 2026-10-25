# Evidence pack: nematic-fuelcell-outslow (seed 12)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 380s; status ok
- command: `python -m labkit.run world.py --out outslow03/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8683, 0.676], min area 6 px

## Measurements
- components: final 17, mean 10.5, max 17; occupancy final 0.10
- tracks: 27; persistent (alive >= 50% of run): 7; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 37.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 17, 17], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0392/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.0316, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 113: holes 0, rim-vs-core 0.20, rim-vs-outside 0.63, heterogeneity 0.09; core [0.929, 0.776, 0.972, 0.924] rim [0.8, 0.64, 0.93, 0.883]
  - track 7 at frame 124: holes 0, rim-vs-core 0.32, rim-vs-outside 0.37, heterogeneity 0.10; core [0.917, 0.782, 0.96, 0.926] rim [0.722, 0.556, 0.889, 0.845]
  - track 5 at frame 97: holes 0, rim-vs-core 0.36, rim-vs-outside 0.66, heterogeneity 0.10; core [0.989, 0.944, 0.961, 0.934] rim [0.801, 0.65, 0.923, 0.881]
  - track 15 at frame 156: holes 0, rim-vs-core 0.34, rim-vs-outside 0.46, heterogeneity 0.11; core [0.962, 0.931, 0.91, 0.942] rim [0.773, 0.673, 0.835, 0.84]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 3.68 (aggregate of 72 individuals; 7/72 membrane-like individually; rim level 0.585)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 5.2 (aggregate of 72 individuals; 8/72 membrane-like individually; rim level 0.491)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 1.53 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.828)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 1.82 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.817)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=565, R_eq 7.48): none; #7 (t=620, R_eq 5.94, ring): none; #5 (t=485, R_eq 6.48): none; #15 (t=780, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 72 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
