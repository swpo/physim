# Evidence pack: eating-flocks (seed 5)

- world: `../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T1457-c58-review-toner-tu/pack_v0 --seeds 5 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0007, 0.6479], min area 6 px

## Measurements
- components: final 168, mean 146.2, max 168; occupancy final 0.37
- tracks: 362; persistent (alive >= 50% of run): 156; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.97 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [169, 169, 168], H1 [74, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 400, default): splits 136, persistent splits 67 (0 more failed only because the siblings re-merged within K), max generation 3, merges 22, merge/split ratio 0.162, nucleations 2
- channel total drift (end/start - 1): [0.8002, -0.5923, -0.1782, -2.0572]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 77: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.15; core [0.807, 0.08, 0.854, 0.828] rim [0.454, 0.215, 0.624, 0.687]
  - track 47 at frame 77: holes 0, rim-vs-core 0.45, rim-vs-outside 0.32, heterogeneity 0.18; core [0.79, 0.086, 0.835, 0.57] rim [0.43, 0.223, 0.601, 0.549]
  - track 62 at frame 77: holes 0, rim-vs-core 0.49, rim-vs-outside 0.35, heterogeneity 0.16; core [0.802, 0.079, 0.835, 0.118] rim [0.441, 0.227, 0.599, 0.284]
  - track 330 at frame 100: holes 0, rim-vs-core 0.45, rim-vs-outside 0.33, heterogeneity 0.17; core [0.818, 0.08, 0.841, 0.468] rim [0.458, 0.212, 0.609, 0.474]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 930 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.743, rim/outside 4.37 (aggregate of 930 individuals; 4/930 membrane-like individually; rim level 0.678)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.15, rim/outside 0.937 (aggregate of 930 individuals; 0/930 membrane-like individually; rim level 0.33)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 3.52 (aggregate of 930 individuals; 8/930 membrane-like individually; rim level 0.777)
  - radial p_x: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1 (aggregate of 930 individuals; 6/930 membrane-like individually; rim level 0.489)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=1540, R_eq 3.39): none; #47 (t=1540, R_eq 3.48): none; #62 (t=1540, R_eq 3.66): none; #330 (t=2000, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 930 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
