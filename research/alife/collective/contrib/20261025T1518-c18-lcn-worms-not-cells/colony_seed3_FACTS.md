# Evidence pack: lcn-colony (seed 3)

- world: `../../world_colony.py`, family `lenia`
- parent: world.py; mutation: lcn started from one noise-formed founder in an empty food-filled domain
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 112s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/lcn/world_colony.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/lcn/cpack --seeds 2 3 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 1, mean 1.1, max 5; occupancy final 0.00
- tracks: 11; persistent (alive >= 50% of run): 1; longest 151 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.62 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [1, 1, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.826/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 100, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6198, -0.545, 0.0051, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 126: holes 0, rim-vs-core 0.16, rim-vs-outside 1.10, heterogeneity 0.20; core [0.864, 0.29, 0.862, 0.043] rim [0.745, 0.183, 0.863, 0.04]
  - track 0 at frame 8: holes 1, rim-vs-core 0.31, rim-vs-outside 0.80, heterogeneity 0.22; core [1.0, 0.305, 0.69, 0.308] rim [0.692, 0.314, 0.692, 0.294]
  - track 6 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.59, heterogeneity 0.16; core [0.953, 0.083, 0.0, 0.716] rim [0.58, 0.192, 0.003, 0.796]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.65, rim/outside 12.3 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.833)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 5.15 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.825)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 1.11 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.805)
  - radial W: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 1.09 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.168)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #10 (t=630, R_eq 6.18): ['A0']; #3 (t=160, R_eq 28.92, ring): ['W']; #0 (t=40, R_eq 8.14, ring): ['A0', 'A1']; #6 (t=250, R_eq 8.74): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 6 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
