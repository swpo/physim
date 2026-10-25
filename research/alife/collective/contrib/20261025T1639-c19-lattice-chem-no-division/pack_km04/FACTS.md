# Evidence pack: lattice-chem (seed 1)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 545s; status ok
- command: `python -m labkit.run research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py --out research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/pack_km04 --seeds 1 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 41, mean 62.3, max 140; occupancy final 0.14
- tracks: 587; persistent (alive >= 50% of run): 50; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 43, 40], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 103, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 221, merge/split ratio 2.15, nucleations 173
- channel total drift (end/start - 1): [2.3277, None, -0.5949, -0.2856]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 101: holes 0, rim-vs-core 0.14, rim-vs-outside 0.36, heterogeneity 0.15; core [0.697, 0.139, 0.037, 0.295] rim [0.598, 0.239, 0.047, 0.294]
  - track 97 at frame 101: holes 0, rim-vs-core 0.13, rim-vs-outside 0.26, heterogeneity 0.16; core [0.641, 0.158, 0.044, 0.412] rim [0.542, 0.209, 0.044, 0.356]
  - track 100 at frame 103: holes 0, rim-vs-core 0.23, rim-vs-outside 0.38, heterogeneity 0.16; core [0.655, 0.118, 0.055, 0.545] rim [0.619, 0.197, 0.075, 0.33]
  - track 113 at frame 103: holes 0, rim-vs-core 0.19, rim-vs-outside 0.39, heterogeneity 0.15; core [0.654, 0.18, 0.056, 0.412] rim [0.6, 0.265, 0.072, 0.256]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 340 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 9.07 (aggregate of 340 individuals; 8/340 membrane-like individually; rim level 0.552)
  - radial M (membrane): peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 2.5, rim/outside 2.72 (aggregate of 340 individuals; 318/340 membrane-like individually; rim level 0.394)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.27, rim/outside 0.668 (aggregate of 340 individuals; 1/340 membrane-like individually; rim level 0.242)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #30 (t=10100, R_eq 3.39): ['M (membrane)']; #97 (t=10100, R_eq 3.29): ['M (membrane)']; #100 (t=10300, R_eq 3.14): ['M (membrane)']; #113 (t=10300, R_eq 3.29): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 340 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
