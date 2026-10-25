# Evidence pack: nematic-fuelcell-res15 (seed 5)

- world: `../world_res15.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 1104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2005-c21-audit-fuelcell/world_res15.py --out collective/contrib/20261025T2005-c21-audit-fuelcell/res15_noise03 --seeds 5 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8488, 0.7019], min area 6 px

## Measurements
- components: final 26, mean 13.6, max 26; occupancy final 0.08
- tracks: 47; persistent (alive >= 50% of run): 6; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 26, 25], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0624/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 100, default): splits 19, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.053, nucleations 8
- channel total drift (end/start - 1): [-0.5091, -0.5163, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 106: holes 0, rim-vs-core 0.60, rim-vs-outside 0.73, heterogeneity 0.19; core [0.986, 0.938, 0.334, 0.997] rim [0.778, 0.668, 0.807, 0.855]
  - track 4 at frame 108: holes 0, rim-vs-core 0.54, rim-vs-outside 0.78, heterogeneity 0.18; core [0.986, 0.986, 0.349, 1.0] rim [0.793, 0.77, 0.778, 0.841]
  - track 8 at frame 141: holes 0, rim-vs-core 0.51, rim-vs-outside 0.71, heterogeneity 0.19; core [0.981, 0.75, 0.36, 0.988] rim [0.767, 0.632, 0.78, 0.836]
  - track 37 at frame 182: holes 0, rim-vs-core 0.55, rim-vs-outside 0.31, heterogeneity 0.16; core [0.922, 0.91, 0.446, 0.6] rim [0.699, 0.611, 0.831, 0.494]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 4.3 (aggregate of 93 individuals; 2/93 membrane-like individually; rim level 0.651)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 6.57 (aggregate of 93 individuals; 3/93 membrane-like individually; rim level 0.538)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 2.3 (aggregate of 93 individuals; 45/93 membrane-like individually; rim level 0.589)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 3.21 (aggregate of 93 individuals; 3/93 membrane-like individually; rim level 0.499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=530, R_eq 6.79): ['shell s']; #4 (t=540, R_eq 6.53): ['shell s']; #8 (t=705, R_eq 6.91): ['shell s']; #37 (t=910, R_eq 5.17): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
