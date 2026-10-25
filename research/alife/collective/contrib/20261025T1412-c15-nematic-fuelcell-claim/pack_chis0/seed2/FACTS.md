# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 650s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/chis0_s2 --seeds 2 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8796, 0.709], min area 6 px

## Measurements
- components: final 15, mean 9.9, max 15; occupancy final 0.10
- tracks: 25; persistent (alive >= 50% of run): 8; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 17, 15], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0378/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.125, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.0069, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.36, rim-vs-outside 0.61, heterogeneity 0.10; core [0.962, 0.868, 0.962, 0.931] rim [0.779, 0.573, 0.918, 0.866]
  - track 1 at frame 106: holes 0, rim-vs-core 0.26, rim-vs-outside 0.66, heterogeneity 0.10; core [0.961, 0.876, 0.987, 0.976] rim [0.81, 0.679, 0.93, 0.903]
  - track 8 at frame 129: holes 0, rim-vs-core 0.44, rim-vs-outside 0.39, heterogeneity 0.12; core [0.943, 0.908, 0.894, 0.954] rim [0.695, 0.58, 0.798, 0.848]
  - track 13 at frame 163: holes 0, rim-vs-core 0.23, rim-vs-outside 0.45, heterogeneity 0.10; core [0.903, 0.809, 0.92, 0.939] rim [0.766, 0.65, 0.862, 0.875]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 3.33 (aggregate of 67 individuals; 7/67 membrane-like individually; rim level 0.534)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.67 (aggregate of 67 individuals; 8/67 membrane-like individually; rim level 0.446)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 1.5 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.8)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 1.48 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.815)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 8.1, ring): ['phi (droplet)', 'order |Q|']; #1 (t=530, R_eq 6.84, ring): ['phi (droplet)', 'order |Q|']; #8 (t=645, R_eq 4.11): none; #13 (t=815, R_eq 4.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 21 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
