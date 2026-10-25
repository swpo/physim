# Evidence pack: lcn-colony (seed 0)

- world: `../../world_colony.py`, family `lenia`
- parent: world.py; mutation: lcn started from one noise-formed founder in an empty food-filled domain
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 115s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/lcn/world_colony.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/lcn/cpack --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 0, mean 0.3, max 5; occupancy final 0.00
- tracks: 20; persistent (alive >= 50% of run): 0; longest 41 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.676/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.571, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, 0.0085, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 42: holes 0, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.16; core [1.0, 0.0, 0.0, 0.681] rim [0.784, 0.097, 0.003, 0.748]
  - track 10 at frame 45: holes 0, rim-vs-core 0.36, rim-vs-outside 0.63, heterogeneity 0.19; core [0.947, 0.143, 0.0, 0.714] rim [0.618, 0.278, 0.001, 0.774]
  - track 11 at frame 45: holes 0, rim-vs-core 0.34, rim-vs-outside 0.38, heterogeneity 0.14; core [0.744, 0.431, 0.0, 0.893] rim [0.459, 0.249, 0.0, 0.891]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [34]):
  - radial A0: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.048 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0)
  - radial A1: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.07 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0)
  - radial F: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.03 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.941)
  - radial W: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 0.026 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.0001)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=100, R_eq 23.52, ring): ['A0', 'W']; #4 (t=210, R_eq 14.06): ['A1']; #10 (t=225, R_eq 9.08): ['A1']; #11 (t=225, R_eq 3.39): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
