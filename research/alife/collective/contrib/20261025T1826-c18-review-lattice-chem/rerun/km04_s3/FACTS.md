# Evidence pack: lattice-chem (seed 3)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 405s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev7/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev7/km04 --seeds 3 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 43, mean 58.7, max 141; occupancy final 0.15
- tracks: 651; persistent (alive >= 50% of run): 38; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 45, 42], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 127, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 240, merge/split ratio 1.89, nucleations 170
- channel total drift (end/start - 1): [2.3223, None, -0.6005, -0.2837]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 101: holes 0, rim-vs-core 0.18, rim-vs-outside 0.39, heterogeneity 0.15; core [0.689, 0.136, 0.054, 0.338] rim [0.604, 0.268, 0.062, 0.263]
  - track 63 at frame 101: holes 0, rim-vs-core 0.23, rim-vs-outside 0.41, heterogeneity 0.14; core [0.718, 0.137, 0.089, 0.289] rim [0.631, 0.16, 0.064, 0.5]
  - track 138 at frame 103: holes 0, rim-vs-core 0.28, rim-vs-outside 0.37, heterogeneity 0.17; core [0.739, 0.141, 0.04, 0.4] rim [0.509, 0.261, 0.079, 0.3]
  - track 145 at frame 103: holes 0, rim-vs-core 0.23, rim-vs-outside 0.42, heterogeneity 0.16; core [0.736, 0.149, 0.047, 0.347] rim [0.569, 0.227, 0.093, 0.48]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 325 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 7.95 (aggregate of 325 individuals; 8/325 membrane-like individually; rim level 0.527)
  - radial M (membrane): peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 2.31, rim/outside 2.61 (aggregate of 325 individuals; 296/325 membrane-like individually; rim level 0.38)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.4, rim/outside 0.697 (aggregate of 325 individuals; 0/325 membrane-like individually; rim level 0.249)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #26 (t=10100, R_eq 3.04): ['M (membrane)']; #63 (t=10100, R_eq 2.71): ['M (membrane)']; #138 (t=10300, R_eq 3.04): ['M (membrane)']; #145 (t=10300, R_eq 3.09): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 325 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
