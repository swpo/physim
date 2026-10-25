# Evidence pack: neural-field (seed 5)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: new class: Amari neural field with an oscillatory Laing-Troy kernel and linear adaptation
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 2s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev13/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev13/rerun --seeds 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 14, mean 15.7, max 60; occupancy final 0.11
- tracks: 94; persistent (alive >= 50% of run): 15; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 24.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.466/time; max body lengths 40.5
- replication (lineage window K = 20 frames = time 60, default): splits 16, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.125, nucleations 1
- channel total drift (end/start - 1): [-1.0, None, -0.4192]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.88, heterogeneity 0.17; core [0.931, 0.651, 1.0] rim [0.679, 0.441, 0.909]
  - track 14 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.88, heterogeneity 0.15; core [0.947, 0.629, 1.0] rim [0.717, 0.517, 0.953]
  - track 32 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.16; core [0.94, 0.596, 1.0] rim [0.71, 0.481, 0.931]
  - track 88 at frame 145: holes 0, rim-vs-core 0.17, rim-vs-outside 1.03, heterogeneity 0.15; core [0.958, 0.515, 1.0] rim [0.796, 0.475, 0.958]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 2.64 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.68)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 1.96 (aggregate of 88 individuals; 2/88 membrane-like individually; rim level 0.548)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 14.3 (aggregate of 88 individuals; 2/88 membrane-like individually; rim level 0.71)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=303, R_eq 3.29): none; #14 (t=303, R_eq 3.39): none; #32 (t=303, R_eq 3.7): none; #88 (t=435, R_eq 8.57, ring): ['firing f(u)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
