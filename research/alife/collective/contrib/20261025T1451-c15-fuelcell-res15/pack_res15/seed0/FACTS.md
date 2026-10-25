# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 1530s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/r15/shell_s0 --seeds 0 --size 192 192 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8242, 0.5442], min area 6 px

## Measurements
- components: final 7, mean 2.5, max 7; occupancy final 0.04
- tracks: 16; persistent (alive >= 50% of run): 0; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 7, 6], H1 [1, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0424/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.143, nucleations 1
- channel total drift (end/start - 1): [-0.5018, -0.6989, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 156: holes 0, rim-vs-core 0.44, rim-vs-outside 0.68, heterogeneity 0.15; core [0.99, 0.963, 0.49, 0.878] rim [0.831, 0.765, 0.827, 0.74]
  - track 2 at frame 123: holes 0, rim-vs-core 0.39, rim-vs-outside 0.91, heterogeneity 0.16; core [1.0, 0.935, 0.496, 0.94] rim [0.879, 0.734, 0.795, 0.833]
  - track 0 at frame 54: holes 0, rim-vs-core 0.42, rim-vs-outside 0.76, heterogeneity 0.15; core [0.999, 0.995, 0.497, 0.889] rim [0.852, 0.858, 0.841, 0.747]
  - track 8 at frame 178: holes 0, rim-vs-core 0.44, rim-vs-outside 0.71, heterogeneity 0.14; core [0.995, 0.991, 0.456, 0.795] rim [0.852, 0.849, 0.825, 0.669]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 19 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 2.97 (aggregate of 19 individuals; 2/19 membrane-like individually; rim level 0.543)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 3.32 (aggregate of 19 individuals; 2/19 membrane-like individually; rim level 0.464)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 2.12 (aggregate of 19 individuals; 1/19 membrane-like individually; rim level 0.573)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 2.7 (aggregate of 19 individuals; 2/19 membrane-like individually; rim level 0.499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=780, R_eq 7.98): none; #2 (t=615, R_eq 11.81, ring): none; #0 (t=270, R_eq 9.42): none; #8 (t=890, R_eq 7.31): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 19 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
