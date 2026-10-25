# Evidence pack: nematic-fuelcell-res15 (seed 6)

- world: `../world_res15.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 1101s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2005-c21-audit-fuelcell/world_res15.py --out collective/contrib/20261025T2005-c21-audit-fuelcell/res15_noise03_s6 --seeds 6 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8523, 0.6428], min area 6 px

## Measurements
- components: final 21, mean 10.2, max 21; occupancy final 0.08
- tracks: 71; persistent (alive >= 50% of run): 7; longest 129 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 22, 20], H1 [1, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.1/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.286, nucleations 6
- channel total drift (end/start - 1): [-0.4991, -0.5312, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.42, rim-vs-outside 0.80, heterogeneity 0.15; core [0.949, 0.813, 0.473, 0.797] rim [0.804, 0.548, 0.757, 0.78]
  - track 10 at frame 138: holes 0, rim-vs-core 0.53, rim-vs-outside 0.32, heterogeneity 0.15; core [0.935, 0.923, 0.469, 0.597] rim [0.711, 0.636, 0.84, 0.471]
  - track 7 at frame 106: holes 0, rim-vs-core 0.47, rim-vs-outside 0.58, heterogeneity 0.15; core [0.961, 0.776, 0.475, 0.757] rim [0.778, 0.539, 0.807, 0.627]
  - track 59 at frame 188: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.17; core [0.944, 0.922, 0.468, 0.717] rim [0.72, 0.597, 0.897, 0.58]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 3.57 (aggregate of 72 individuals; 5/72 membrane-like individually; rim level 0.609)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 5.47 (aggregate of 72 individuals; 7/72 membrane-like individually; rim level 0.506)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 2.1 (aggregate of 72 individuals; 29/72 membrane-like individually; rim level 0.572)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 2.83 (aggregate of 72 individuals; 10/72 membrane-like individually; rim level 0.467)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=380, R_eq 12.79, ring): none; #10 (t=690, R_eq 6): ['shell s']; #7 (t=530, R_eq 7.67): none; #59 (t=940, R_eq 4.98): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 72 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
