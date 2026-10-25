# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 653s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/shell_s2 --seeds 2 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.861, 0.6461], min area 6 px

## Measurements
- components: final 22, mean 11.0, max 22; occupancy final 0.09
- tracks: 44; persistent (alive >= 50% of run): 9; longest 180 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 22, 22], H1 [1, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0742/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 100, default): splits 17, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.118, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.1754, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 99: holes 0, rim-vs-core 0.44, rim-vs-outside 0.74, heterogeneity 0.16; core [0.952, 0.794, 0.409, 0.89] rim [0.804, 0.596, 0.739, 0.726]
  - track 3 at frame 86: holes 0, rim-vs-core 0.56, rim-vs-outside 0.75, heterogeneity 0.15; core [0.981, 0.92, 0.314, 0.792] rim [0.809, 0.601, 0.743, 0.743]
  - track 8 at frame 128: holes 0, rim-vs-core 0.58, rim-vs-outside 0.42, heterogeneity 0.16; core [0.958, 0.936, 0.38, 0.625] rim [0.732, 0.624, 0.802, 0.514]
  - track 28 at frame 183: holes 0, rim-vs-core 0.50, rim-vs-outside 0.41, heterogeneity 0.15; core [0.932, 0.854, 0.48, 0.769] rim [0.744, 0.604, 0.841, 0.631]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 3.56 (aggregate of 77 individuals; 8/77 membrane-like individually; rim level 0.588)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 5.31 (aggregate of 77 individuals; 10/77 membrane-like individually; rim level 0.483)
  - radial shell s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 2.14 (aggregate of 77 individuals; 34/77 membrane-like individually; rim level 0.544)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 2.46 (aggregate of 77 individuals; 9/77 membrane-like individually; rim level 0.511)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=495, R_eq 6.63, ring): ['phi (droplet)', 'order |Q|', 'shell s', 'fuel f']; #3 (t=430, R_eq 8.18, ring): none; #8 (t=640, R_eq 3.66): ['shell s']; #28 (t=915, R_eq 4.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 21 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
