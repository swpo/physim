# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 718s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z35/shell --seeds 0 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8618, 0.6789], min area 6 px

## Measurements
- components: final 19, mean 11.5, max 19; occupancy final 0.09
- tracks: 39; persistent (alive >= 50% of run): 10; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 19, 19], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0371/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.143, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.1747, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 97: holes 0, rim-vs-core 0.47, rim-vs-outside 0.43, heterogeneity 0.16; core [0.905, 0.706, 0.507, 0.861] rim [0.724, 0.502, 0.851, 0.683]
  - track 6 at frame 96: holes 0, rim-vs-core 0.43, rim-vs-outside 0.75, heterogeneity 0.15; core [0.935, 0.792, 0.399, 0.893] rim [0.792, 0.615, 0.734, 0.76]
  - track 9 at frame 129: holes 0, rim-vs-core 0.57, rim-vs-outside 0.44, heterogeneity 0.15; core [0.949, 0.929, 0.381, 0.832] rim [0.74, 0.63, 0.788, 0.684]
  - track 23 at frame 182: holes 0, rim-vs-core 0.70, rim-vs-outside 0.57, heterogeneity 0.18; core [0.979, 0.938, 0.366, 1.0] rim [0.735, 0.586, 0.918, 0.926]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 3.8 (aggregate of 78 individuals; 5/78 membrane-like individually; rim level 0.601)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 5.6 (aggregate of 78 individuals; 7/78 membrane-like individually; rim level 0.501)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 2.27 (aggregate of 78 individuals; 36/78 membrane-like individually; rim level 0.56)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 2.7 (aggregate of 78 individuals; 6/78 membrane-like individually; rim level 0.549)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=485, R_eq 5.01): none; #6 (t=480, R_eq 7.55, ring): none; #9 (t=645, R_eq 3.87): ['shell s']; #23 (t=910, R_eq 4.51): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
