# Evidence pack: lattice-chem (seed 4)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 207s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev11/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev11/lam0 --seeds 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 27.0], min area 6 px

## Measurements
- components: final 55, mean 75.0, max 155; occupancy final 0.18
- tracks: 1407; persistent (alive >= 50% of run): 46; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 56, 52], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000606/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 1000, default): splits 380, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 497, merge/split ratio 1.31, nucleations 182
- channel total drift (end/start - 1): [2.6406, None, -0.6276, 1.3235]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.15, rim-vs-outside 0.51, heterogeneity 0.17; core [0.628, 0.319, 0.031, 0.538] rim [0.706, 0.395, 0.059, 0.444]
  - track 73 at frame 103: holes 0, rim-vs-core 0.17, rim-vs-outside 0.35, heterogeneity 0.19; core [0.662, 0.429, 0.011, 0.481] rim [0.619, 0.316, 0.121, 0.508]
  - track 75 at frame 103: holes 0, rim-vs-core 0.19, rim-vs-outside 0.27, heterogeneity 0.17; core [0.667, 0.429, 0.013, 0.569] rim [0.593, 0.319, 0.054, 0.436]
  - track 140 at frame 103: holes 0, rim-vs-core 0.18, rim-vs-outside 0.29, heterogeneity 0.16; core [0.62, 0.286, 0.033, 0.642] rim [0.592, 0.381, 0.06, 0.489]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 408 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 9.46 (aggregate of 408 individuals; 23/408 membrane-like individually; rim level 0.526)
  - radial M (membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 3.04 (aggregate of 408 individuals; 197/408 membrane-like individually; rim level 0.341)
  - radial X (food): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.19, rim/outside 0.715 (aggregate of 408 individuals; 1/408 membrane-like individually; rim level 0.237)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=5050, R_eq 3.09): ['M (membrane)']; #73 (t=5150, R_eq 2.71): none; #75 (t=5150, R_eq 2.59): none; #140 (t=5150, R_eq 2.76): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 26 of 408 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
