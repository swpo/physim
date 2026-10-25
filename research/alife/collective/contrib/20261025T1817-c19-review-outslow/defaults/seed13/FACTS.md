# Evidence pack: nematic-fuelcell-outslow (seed 13)

- world: `../../../20261025T1713-c15-fuelcell-outslow-twin/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 532s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1713-c15-fuelcell-outslow-twin/world.py --out collective/contrib/20261025T1817-c19-review-outslow/outslow/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8478, 0.691], min area 6 px

## Measurements
- components: final 18, mean 11.7, max 19; occupancy final 0.08
- tracks: 37; persistent (alive >= 50% of run): 9; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 20, 18], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0497/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.2826, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.55, rim-vs-outside 0.40, heterogeneity 0.15; core [0.94, 0.903, 0.41, 0.682] rim [0.727, 0.602, 0.8, 0.568]
  - track 6 at frame 118: holes 0, rim-vs-core 0.48, rim-vs-outside 0.42, heterogeneity 0.15; core [0.908, 0.728, 0.52, 0.809] rim [0.715, 0.518, 0.861, 0.622]
  - track 7 at frame 126: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.16; core [0.9, 0.719, 0.52, 0.725] rim [0.713, 0.499, 0.851, 0.567]
  - track 25 at frame 171: holes 0, rim-vs-core 0.49, rim-vs-outside 0.51, heterogeneity 0.16; core [0.949, 0.939, 0.424, 0.724] rim [0.767, 0.69, 0.777, 0.596]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 3.99 (aggregate of 78 individuals; 3/78 membrane-like individually; rim level 0.618)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 5.88 (aggregate of 78 individuals; 5/78 membrane-like individually; rim level 0.511)
  - radial shell s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 2.22 (aggregate of 78 individuals; 31/78 membrane-like individually; rim level 0.58)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 2.61 (aggregate of 78 individuals; 3/78 membrane-like individually; rim level 0.549)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=570, R_eq 3.83): ['shell s']; #6 (t=590, R_eq 5.38): none; #7 (t=630, R_eq 5.14, ring): none; #25 (t=855, R_eq 4.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
