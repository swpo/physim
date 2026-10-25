# Evidence pack: lattice-chem (seed 1)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 274s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py --out (c19 run of research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py) --seeds 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 56, mean 71.6, max 157; occupancy final 0.17
- tracks: 2020; persistent (alive >= 50% of run): 38; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [79, 55, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 588, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 697, merge/split ratio 1.19, nucleations 213
- channel total drift (end/start - 1): [2.5929, None, -0.6271, 1.3377]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 103: holes 0, rim-vs-core 0.21, rim-vs-outside 0.48, heterogeneity 0.18; core [0.639, 0.238, 0.067, 0.407] rim [0.684, 0.417, 0.075, 0.509]
  - track 81 at frame 103: holes 0, rim-vs-core 0.09, rim-vs-outside 0.23, heterogeneity 0.18; core [0.667, 0.329, 0.04, 0.5] rim [0.586, 0.339, 0.075, 0.5]
  - track 98 at frame 103: holes 0, rim-vs-core 0.36, rim-vs-outside 0.43, heterogeneity 0.19; core [0.648, 0.206, 0.056, 0.414] rim [0.647, 0.555, 0.135, 0.359]
  - track 107 at frame 103: holes 0, rim-vs-core 0.11, rim-vs-outside 0.25, heterogeneity 0.15; core [0.676, 0.27, 0.056, 0.37] rim [0.604, 0.345, 0.067, 0.407]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 391 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 7.86 (aggregate of 391 individuals; 28/391 membrane-like individually; rim level 0.506)
  - radial M (membrane): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 2.83 (aggregate of 391 individuals; 164/391 membrane-like individually; rim level 0.339)
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.68, rim/outside 0.694 (aggregate of 391 individuals; 1/391 membrane-like individually; rim level 0.227)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #65 (t=5150, R_eq 2.59): ['M (membrane)']; #81 (t=5150, R_eq 2.88): ['M (membrane)']; #98 (t=5150, R_eq 3.34): ['M (membrane)']; #107 (t=5150, R_eq 2.59): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 391 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
