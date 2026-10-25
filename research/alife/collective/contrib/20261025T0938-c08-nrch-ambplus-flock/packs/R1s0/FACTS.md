# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 800s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/R1s0 --seeds 0 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0163, 1.0106], min area 6 px

## Measurements
- components: final 9, mean 5.8, max 11; occupancy final 0.18
- tracks: 50; persistent (alive >= 50% of run): 5; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.18/time; max body lengths 26.4
- replication (lineage window K = 20 frames = time 1000, default): splits 7, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.714, nucleations 32
- channel total drift (end/start - 1): [-0.0746, 257.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 79: holes 0, rim-vs-core 0.25, rim-vs-outside 0.42, heterogeneity 0.19; core [0.94, 0.36] rim [0.686, 0.371]
  - track 9 at frame 79: holes 0, rim-vs-core 0.19, rim-vs-outside 0.51, heterogeneity 0.19; core [0.956, 0.361] rim [0.765, 0.362]
  - track 7 at frame 78: holes 0, rim-vs-core 0.24, rim-vs-outside 0.41, heterogeneity 0.19; core [0.921, 0.327] rim [0.689, 0.387]
  - track 36 at frame 96: holes 0, rim-vs-core 0.24, rim-vs-outside 0.44, heterogeneity 0.19; core [0.936, 0.328] rim [0.695, 0.368]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 6.88 (aggregate of 42 individuals; 1/42 membrane-like individually; rim level 0.773)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.954 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.536)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=3950, R_eq 17.96): none; #9 (t=3950, R_eq 19.41): none; #7 (t=3900, R_eq 14.8): none; #36 (t=4800, R_eq 17.21): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 42 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
