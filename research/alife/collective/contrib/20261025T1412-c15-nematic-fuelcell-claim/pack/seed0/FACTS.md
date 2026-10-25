# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 718s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/shell_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8544, 0.6687], min area 6 px

## Measurements
- components: final 25, mean 13.8, max 26; occupancy final 0.08
- tracks: 49; persistent (alive >= 50% of run): 7; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 29.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 25, 25], H1 [1, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0662/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 100, default): splits 19, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.105, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.2256, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 103: holes 0, rim-vs-core 0.44, rim-vs-outside 0.72, heterogeneity 0.15; core [0.939, 0.783, 0.419, 0.862] rim [0.784, 0.558, 0.743, 0.744]
  - track 11 at frame 129: holes 0, rim-vs-core 0.57, rim-vs-outside 0.42, heterogeneity 0.16; core [0.947, 0.922, 0.394, 0.737] rim [0.726, 0.612, 0.802, 0.61]
  - track 6 at frame 92: holes 0, rim-vs-core 0.42, rim-vs-outside 0.71, heterogeneity 0.15; core [0.93, 0.748, 0.432, 0.864] rim [0.781, 0.554, 0.749, 0.735]
  - track 34 at frame 183: holes 0, rim-vs-core 0.61, rim-vs-outside 0.46, heterogeneity 0.17; core [0.959, 0.946, 0.372, 0.815] rim [0.734, 0.622, 0.807, 0.661]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 4.53 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.674)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 7.43 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.579)
  - radial shell s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 2.31 (aggregate of 97 individuals; 61/97 membrane-like individually; rim level 0.594)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 2.72 (aggregate of 97 individuals; 4/97 membrane-like individually; rim level 0.576)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=515, R_eq 7.02): none; #11 (t=645, R_eq 3.87): ['shell s']; #6 (t=460, R_eq 7.44, ring): none; #34 (t=915, R_eq 3.74): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
