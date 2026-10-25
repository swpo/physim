# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 490s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1727-c19-review-fuelring-slowd/slowD03/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8601, 0.6276], min area 6 px

## Measurements
- components: final 18, mean 11.4, max 19; occupancy final 0.09
- tracks: 34; persistent (alive >= 50% of run): 10; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 41.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 19, 18], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0388/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 100, default): splits 13, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.2693, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 114: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.12; core [0.97, 0.889, 0.992, 1.0] rim [0.721, 0.508, 0.921, 0.924]
  - track 9 at frame 116: holes 0, rim-vs-core 0.31, rim-vs-outside 0.65, heterogeneity 0.09; core [0.97, 0.882, 0.968, 0.959] rim [0.821, 0.639, 0.946, 0.831]
  - track 8 at frame 111: holes 0, rim-vs-core 0.39, rim-vs-outside 0.42, heterogeneity 0.11; core [0.921, 0.861, 0.928, 0.881] rim [0.713, 0.589, 0.862, 0.701]
  - track 16 at frame 166: holes 0, rim-vs-core 0.35, rim-vs-outside 0.61, heterogeneity 0.10; core [0.97, 0.818, 0.958, 0.922] rim [0.812, 0.55, 0.926, 0.771]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 3.42 (aggregate of 79 individuals; 6/79 membrane-like individually; rim level 0.593)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 4.94 (aggregate of 79 individuals; 7/79 membrane-like individually; rim level 0.477)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 1.43 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.827)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 2.4 (aggregate of 79 individuals; 2/79 membrane-like individually; rim level 0.654)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=570, R_eq 4.33): none; #9 (t=580, R_eq 7.82, ring): none; #8 (t=555, R_eq 4.82): none; #16 (t=830, R_eq 7.16, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
