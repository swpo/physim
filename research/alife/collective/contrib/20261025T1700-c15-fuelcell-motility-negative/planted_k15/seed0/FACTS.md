# Evidence pack: nematic-fuelcell-planted (seed 0)

- world: `../../world_plant.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 669s; status ok
- command: `python -m labkit.run /root/w/world_plant.py --out /root/w/plant/k15_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.51 of robust range [-0.8485, 0.8117], min area 6 px

## Measurements
- components: final 16, mean 11.5, max 16; occupancy final 0.08
- tracks: 65; persistent (alive >= 50% of run): 11; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 16, 16], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.0639/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 12, merge/split ratio 0.462, nucleations 0
- channel total drift (end/start - 1): [-0.117, -0.3074, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 111: holes 0, rim-vs-core 0.53, rim-vs-outside 0.38, heterogeneity 0.14; core [0.912, 0.874, 0.455, 0.653] rim [0.697, 0.568, 0.812, 0.521]
  - track 43 at frame 114: holes 0, rim-vs-core 0.56, rim-vs-outside 0.44, heterogeneity 0.16; core [0.957, 0.938, 0.334, 0.629] rim [0.757, 0.667, 0.768, 0.534]
  - track 44 at frame 114: holes 0, rim-vs-core 0.53, rim-vs-outside 0.37, heterogeneity 0.15; core [0.909, 0.85, 0.461, 0.606] rim [0.694, 0.551, 0.83, 0.496]
  - track 47 at frame 129: holes 0, rim-vs-core 0.57, rim-vs-outside 0.47, heterogeneity 0.18; core [0.957, 0.754, 0.401, 0.961] rim [0.731, 0.579, 0.848, 0.763]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 4.3 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.639)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 6.67 (aggregate of 77 individuals; 3/77 membrane-like individually; rim level 0.543)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 2.16 (aggregate of 77 individuals; 35/77 membrane-like individually; rim level 0.602)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 2.48 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.511)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=555, R_eq 4.15): ['shell s']; #43 (t=570, R_eq 3.34): ['shell s']; #44 (t=570, R_eq 3.87): ['shell s']; #47 (t=645, R_eq 4.37): ['shell s']

## Warnings
- radial: 9 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
