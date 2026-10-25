# Evidence pack: lattice-chem-gate (seed 3)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev14/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev14/nogate --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 14.0], min area 6 px

## Measurements
- components: final 71, mean 66.1, max 93; occupancy final 0.18
- tracks: 8168; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.69, final 1; holes at thresholds 0.2/0.35/0.5 final [43, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [106, 31, 3], H1 [53, 7, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 1000, default): splits 2530, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2461, merge/split ratio 0.973, nucleations 1379
- channel total drift (end/start - 1): [2.4124, None, -0.6141, 1.3028]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3732 at frame 118: holes 0, rim-vs-core 0.25, rim-vs-outside 0.12, heterogeneity 0.21; core [0.649, 0.202, 0.105, 0.461] rim [0.448, 0.257, 0.163, 0.333]
  - track 34 at frame 15: holes 0, rim-vs-core 0.10, rim-vs-outside 0.30, heterogeneity 0.20; core [0.553, 0.312, 0.114, 0.461] rim [0.527, 0.34, 0.167, 0.385]
  - track 154 at frame 29: holes 1, rim-vs-core 0.13, rim-vs-outside 0.25, heterogeneity 0.19; core [0.592, 0.242, 0.106, 0.462] rim [0.51, 0.318, 0.169, 0.42]
  - track 33 at frame 15: holes 0, rim-vs-core 0.17, rim-vs-outside 0.28, heterogeneity 0.20; core [0.656, 0.284, 0.073, 0.42] rim [0.523, 0.362, 0.13, 0.402]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 348 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.6 (aggregate of 348 individuals; 34/348 membrane-like individually; rim level 0.466)
  - radial M (membrane): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 1.44 (aggregate of 348 individuals; 168/348 membrane-like individually; rim level 0.31)
  - radial X (food): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.891 (aggregate of 348 individuals; 23/348 membrane-like individually; rim level 0.2)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3732 (t=5900, R_eq 3.7): ['M (membrane)']; #34 (t=750, R_eq 8.99): none; #154 (t=1450, R_eq 8.57, ring): ['A (autocatalyst)']; #33 (t=750, R_eq 6.46): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 31 of 348 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
