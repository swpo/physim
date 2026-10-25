# Evidence pack: lattice-chem (seed 0)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 280s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py --out collective/contrib/20261025T1518-c19-lattice-chem-sighting/pack --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 66, mean 77.5, max 149; occupancy final 0.15
- tracks: 872; persistent (alive >= 50% of run): 62; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 66, 64], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00139/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 1000, default): splits 202, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 300, merge/split ratio 1.49, nucleations 185
- channel total drift (end/start - 1): [2.4623, None, -0.6073, 1.2361]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.15, rim-vs-outside 0.48, heterogeneity 0.16; core [0.695, 0.104, 0.044, 0.479] rim [0.636, 0.23, 0.067, 0.415]
  - track 2 at frame 101: holes 0, rim-vs-core 0.17, rim-vs-outside 0.48, heterogeneity 0.13; core [0.734, 0.094, 0.038, 0.513] rim [0.597, 0.111, 0.073, 0.415]
  - track 10 at frame 103: holes 0, rim-vs-core 0.28, rim-vs-outside 0.51, heterogeneity 0.16; core [0.875, 0.0, 0.0, 0.407] rim [0.652, 0.076, 0.082, 0.525]
  - track 12 at frame 103: holes 0, rim-vs-core 0.20, rim-vs-outside 0.37, heterogeneity 0.14; core [0.708, 0.042, 0.013, 0.611] rim [0.611, 0.139, 0.067, 0.472]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 439 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 9.87 (aggregate of 439 individuals; 18/439 membrane-like individually; rim level 0.564)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 3.63, rim/outside 4.66 (aggregate of 439 individuals; 403/439 membrane-like individually; rim level 0.37)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.37, rim/outside 0.693 (aggregate of 439 individuals; 3/439 membrane-like individually; rim level 0.237)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #1 (t=5050, R_eq 3.14): ['M (membrane)']; #2 (t=5050, R_eq 2.99): ['M (membrane)']; #10 (t=5150, R_eq 2.82): ['M (membrane)']; #12 (t=5150, R_eq 2.52): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 29 of 439 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
