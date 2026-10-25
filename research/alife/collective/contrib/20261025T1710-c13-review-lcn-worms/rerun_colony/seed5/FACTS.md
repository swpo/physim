# Evidence pack: lcn-colony (seed 5)

- world: `../../world_colony.py`, family `lenia`
- parent: world.py; mutation: lcn started from one noise-formed founder in an empty food-filled domain
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 114s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1710-c13-review-lcn-worms/world_colony.py --out collective/contrib/20261025T1710-c13-review-lcn-worms/rerun_colony/seed5 --seeds 5 --spf 50 --frames 200 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 2, mean 1.8, max 4; occupancy final 0.01
- tracks: 9; persistent (alive >= 50% of run): 2; longest 152 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.76 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [2, 2, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.576/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 100, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.333, nucleations 0
- channel total drift (end/start - 1): [0.2625, 0.3092, -0.003, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 124: holes 0, rim-vs-core 0.16, rim-vs-outside 1.08, heterogeneity 0.20; core [0.881, 0.302, 0.885, 0.027] rim [0.777, 0.181, 0.886, 0.022]
  - track 5 at frame 124: holes 0, rim-vs-core 0.10, rim-vs-outside 1.01, heterogeneity 0.20; core [0.862, 0.209, 0.857, 0.072] rim [0.794, 0.283, 0.865, 0.043]
  - track 0 at frame 24: holes 1, rim-vs-core 0.21, rim-vs-outside 0.92, heterogeneity 0.12; core [0.964, 0.0, 0.011, 0.708] rim [0.759, 0.021, 0.035, 0.727]
  - track 2 at frame 50: holes 0, rim-vs-core 0.29, rim-vs-outside 0.76, heterogeneity 0.17; core [0.985, 0.091, 0.0, 0.701] rim [0.709, 0.135, 0.002, 0.77]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.74, rim/outside 21.9 (aggregate of 11 individuals; 9/11 membrane-like individually; rim level 0.909)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 4.77 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.893)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 1.03 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.81)
  - radial W: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 1.15 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.128)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #4 (t=620, R_eq 6.13): ['A0']; #5 (t=620, R_eq 6.21): ['A0', 'A1']; #0 (t=120, R_eq 21.58, ring): ['A0', 'W']; #2 (t=250, R_eq 12.74): ['A1']

## Warnings
- radial: 1 of 11 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
