# Evidence pack: eating-flocks (seed 1)

- world: `../../world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/pack_v0 --seeds 0 1 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6453], min area 6 px

## Measurements
- components: final 163, mean 144.6, max 163; occupancy final 0.37
- tracks: 385; persistent (alive >= 50% of run): 157; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.08 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [163, 163, 163], H1 [66, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 400, default): splits 145, persistent splits 62 (0 more failed only because the siblings re-merged within K), max generation 3, merges 30, merge/split ratio 0.207, nucleations 7
- channel total drift (end/start - 1): [1.4969, -0.5904, -0.1865, 0.2074]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 77: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.17; core [0.836, 0.067, 0.72, 0.346] rim [0.532, 0.193, 0.715, 0.568]
  - track 80 at frame 77: holes 0, rim-vs-core 0.37, rim-vs-outside 0.37, heterogeneity 0.17; core [0.833, 0.068, 0.716, 0.443] rim [0.491, 0.208, 0.697, 0.476]
  - track 91 at frame 77: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.15; core [0.835, 0.068, 0.861, 0.112] rim [0.498, 0.204, 0.65, 0.246]
  - track 290 at frame 88: holes 0, rim-vs-core 0.48, rim-vs-outside 0.36, heterogeneity 0.16; core [0.822, 0.077, 0.851, 0.103] rim [0.461, 0.216, 0.618, 0.254]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 922 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 4.45 (aggregate of 922 individuals; 1/922 membrane-like individually; rim level 0.688)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.3, rim/outside 0.939 (aggregate of 922 individuals; 0/922 membrane-like individually; rim level 0.334)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 3.63 (aggregate of 922 individuals; 15/922 membrane-like individually; rim level 0.781)
  - radial p_x: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.996 (aggregate of 922 individuals; 5/922 membrane-like individually; rim level 0.484)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #51 (t=1540, R_eq 3.57): ['|p|', 'p_x']; #80 (t=1540, R_eq 3.48): ['|p|']; #91 (t=1540, R_eq 3.43): none; #290 (t=1760, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 922 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
