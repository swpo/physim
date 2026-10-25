# Evidence pack: nematic-fuelcell (seed 13)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 542s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1727-c19-review-fuelring-slowd/slowD03/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8476, 0.6598], min area 6 px

## Measurements
- components: final 26, mean 12.8, max 26; occupancy final 0.08
- tracks: 52; persistent (alive >= 50% of run): 7; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 26, 25], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0697/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.045, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.2721, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.45, rim-vs-outside 0.40, heterogeneity 0.12; core [0.953, 0.939, 0.877, 0.869] rim [0.729, 0.619, 0.807, 0.655]
  - track 8 at frame 123: holes 0, rim-vs-core 0.38, rim-vs-outside 0.41, heterogeneity 0.11; core [0.94, 0.883, 0.906, 0.824] rim [0.75, 0.609, 0.845, 0.657]
  - track 12 at frame 141: holes 0, rim-vs-core 0.34, rim-vs-outside 0.37, heterogeneity 0.10; core [0.918, 0.722, 0.907, 0.759] rim [0.728, 0.489, 0.853, 0.614]
  - track 42 at frame 190: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.13; core [0.946, 0.931, 0.896, 0.871] rim [0.723, 0.627, 0.824, 0.646]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 4.42 (aggregate of 86 individuals; 2/86 membrane-like individually; rim level 0.679)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 6.92 (aggregate of 86 individuals; 5/86 membrane-like individually; rim level 0.58)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 1.48 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.852)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 2.68 (aggregate of 86 individuals; 1/86 membrane-like individually; rim level 0.697)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=570, R_eq 3.43): none; #8 (t=615, R_eq 4.07): none; #12 (t=705, R_eq 4.51): none; #42 (t=950, R_eq 3.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
