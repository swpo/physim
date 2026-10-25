# Evidence pack: lattice-chem-gate (seed 3)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 213s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev14/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev14/slowA --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 20.0], min area 6 px

## Measurements
- components: final 95, mean 98.1, max 138; occupancy final 0.07
- tracks: 4742; persistent (alive >= 50% of run): 0; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [157, 89, 22], H1 [67, 15, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.0078/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 1000, default): splits 535, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 548, merge/split ratio 1.02, nucleations 3195
- channel total drift (end/start - 1): [2.6677, None, -0.6781, 1.5041]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1051 at frame 76: holes 0, rim-vs-core 0.19, rim-vs-outside 0.24, heterogeneity 0.19; core [0.605, 0.163, 0.157, 0.438] rim [0.514, 0.263, 0.089, 0.329]
  - track 2719 at frame 145: holes 0, rim-vs-core 0.29, rim-vs-outside 0.28, heterogeneity 0.17; core [0.725, 0.0, 0.033, 0.375] rim [0.526, 0.185, 0.124, 0.346]
  - track 3158 at frame 165: holes 0, rim-vs-core 0.25, rim-vs-outside 0.29, heterogeneity 0.15; core [0.612, 0.0, 0.06, 0.425] rim [0.583, 0.25, 0.1, 0.427]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 271 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 2.64 (aggregate of 271 individuals; 49/271 membrane-like individually; rim level 0.525)
  - radial M (membrane): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 2.29, rim/outside 1.85 (aggregate of 271 individuals; 230/271 membrane-like individually; rim level 0.353)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.78, rim/outside 0.732 (aggregate of 271 individuals; 19/271 membrane-like individually; rim level 0.188)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #1051 (t=3800, R_eq 3.24): ['M (membrane)']; #1125 (t=3850, R_eq 2.03): ['A (autocatalyst)', 'M (membrane)']; #2719 (t=7250, R_eq 2.52): ['M (membrane)']; #3158 (t=8250, R_eq 2.33): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 271 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
