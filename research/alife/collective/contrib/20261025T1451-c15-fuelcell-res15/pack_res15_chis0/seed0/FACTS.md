# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 1523s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/r15/chis0_s0 --seeds 0 --size 192 192 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8486, 0.669], min area 6 px

## Measurements
- components: final 7, mean 2.0, max 7; occupancy final 0.05
- tracks: 13; persistent (alive >= 50% of run): 1; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 122.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 6], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0561/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 100, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5018, -0.4819, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 77: holes 0, rim-vs-core 0.25, rim-vs-outside 0.78, heterogeneity 0.11; core [1.0, 1.0, 0.995, 0.975] rim [0.851, 0.823, 0.948, 0.892]
  - track 4 at frame 170: holes 0, rim-vs-core 0.37, rim-vs-outside 0.54, heterogeneity 0.12; core [0.99, 0.985, 0.953, 0.939] rim [0.783, 0.712, 0.866, 0.822]
  - track 6 at frame 171: holes 0, rim-vs-core 0.38, rim-vs-outside 0.54, heterogeneity 0.12; core [0.99, 0.982, 0.959, 0.946] rim [0.777, 0.701, 0.87, 0.83]
  - track 5 at frame 166: holes 0, rim-vs-core 0.32, rim-vs-outside 0.71, heterogeneity 0.11; core [0.998, 0.97, 0.991, 0.95] rim [0.829, 0.721, 0.933, 0.855]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 3.45 (aggregate of 15 individuals; 3/15 membrane-like individually; rim level 0.529)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 5.13 (aggregate of 15 individuals; 3/15 membrane-like individually; rim level 0.493)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.58 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.814)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.83 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.829)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=385, R_eq 12.21): none; #4 (t=850, R_eq 7.69): none; #6 (t=855, R_eq 7.76): none; #5 (t=830, R_eq 12.72, ring): ['phi (droplet)', 'order |Q|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 15 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
