# Evidence pack: lcn-colony (seed 6)

- world: `../../world_colony.py`, family `lenia`
- parent: world.py; mutation: lcn started from one noise-formed founder in an empty food-filled domain
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 113s; status ok
- command: `python -m labkit.run world_colony.py --out colony --seeds 4 5 6 7 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 0, mean 0.2, max 4; occupancy final 0.00
- tracks: 7; persistent (alive >= 50% of run): 0; longest 39 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.74/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, 0.0079, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 40: holes 0, rim-vs-core 0.38, rim-vs-outside 0.63, heterogeneity 0.18; core [0.952, 0.112, 0.0, 0.722] rim [0.631, 0.312, 0.003, 0.782]
  - track 4 at frame 40: holes 0, rim-vs-core 0.36, rim-vs-outside 0.67, heterogeneity 0.18; core [0.969, 0.205, 0.0, 0.723] rim [0.62, 0.236, 0.001, 0.798]
  - track 1 at frame 39: holes 0, rim-vs-core 0.23, rim-vs-outside 0.82, heterogeneity 0.16; core [0.978, 0.0, 0.0, 0.731] rim [0.769, 0.081, 0.001, 0.79]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [34]):
  - radial A0: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 18.6, rim/outside 1.26 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.176)
  - radial A1: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 31.1, rim/outside 3.27 (aggregate of 1 individuals; 1/1 membrane-like individually; rim level 0.301)  MEMBRANE-LIKE
  - radial F: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 3.14 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.944)
  - radial W: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 24.8, rim/outside 0.376 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #0 (t=90, R_eq 25.72, ring): ['W']; #2 (t=200, R_eq 7.74): ['A1']; #4 (t=200, R_eq 6.98): ['A1']; #1 (t=195, R_eq 19.24, ring): ['A0']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
