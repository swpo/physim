# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 653s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z6/shell_s2 --seeds 2 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8467, 0.6329], min area 6 px

## Measurements
- components: final 24, mean 13.5, max 25; occupancy final 0.08
- tracks: 57; persistent (alive >= 50% of run): 9; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 37.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 25, 24], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0448/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.174, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.2959, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 109: holes 0, rim-vs-core 0.42, rim-vs-outside 0.40, heterogeneity 0.13; core [0.927, 0.743, 0.511, 0.69] rim [0.757, 0.545, 0.815, 0.573]
  - track 9 at frame 106: holes 0, rim-vs-core 0.54, rim-vs-outside 0.44, heterogeneity 0.14; core [0.972, 0.967, 0.372, 0.629] rim [0.763, 0.691, 0.769, 0.532]
  - track 13 at frame 129: holes 0, rim-vs-core 0.57, rim-vs-outside 0.40, heterogeneity 0.15; core [0.958, 0.909, 0.417, 0.659] rim [0.74, 0.591, 0.827, 0.559]
  - track 27 at frame 171: holes 0, rim-vs-core 0.54, rim-vs-outside 0.39, heterogeneity 0.15; core [0.946, 0.929, 0.428, 0.654] rim [0.717, 0.61, 0.788, 0.545]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.12 (aggregate of 95 individuals; 1/95 membrane-like individually; rim level 0.662)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 6.55 (aggregate of 95 individuals; 5/95 membrane-like individually; rim level 0.555)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2.24 (aggregate of 95 individuals; 49/95 membrane-like individually; rim level 0.605)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 2.39 (aggregate of 95 individuals; 1/95 membrane-like individually; rim level 0.531)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=545, R_eq 3.99): none; #9 (t=530, R_eq 3.57): ['shell s']; #13 (t=645, R_eq 2.88): ['shell s']; #27 (t=855, R_eq 3.29): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
