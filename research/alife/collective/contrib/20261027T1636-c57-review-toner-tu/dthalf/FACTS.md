# Evidence pack: eating-flocks (seed 41)

- world: `../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 160 steps x dt 0.25 = time 6000; grid [128, 128]; wall 52s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/c57-w13/dthalf --seeds 41 --frames 150 --spf 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.8469], min area 6 px

## Measurements
- components: final 5, mean 6.3, max 30; occupancy final 0.26
- tracks: 512; persistent (alive >= 50% of run): 0; longest 9 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 7, 5], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 800, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 0.636, nucleations 441
- channel total drift (end/start - 1): [0.8042, -0.5241, -0.2948, 22.7169]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 116 at frame 21: holes 0, rim-vs-core 0.32, rim-vs-outside 0.57, heterogeneity 0.15; core [0.857, 0.01, 0.885, 0.271] rim [0.576, 0.122, 0.793, 0.248]
  - track 258 at frame 61: holes 0, rim-vs-core 0.24, rim-vs-outside 0.31, heterogeneity 0.12; core [0.646, 0.17, 0.841, 0.754] rim [0.484, 0.287, 0.73, 0.67]
  - track 320 at frame 82: holes 0, rim-vs-core 0.19, rim-vs-outside 0.30, heterogeneity 0.12; core [0.63, 0.194, 0.827, 0.678] rim [0.499, 0.283, 0.733, 0.646]
  - track 323 at frame 83: holes 0, rim-vs-core 0.22, rim-vs-outside 0.58, heterogeneity 0.13; core [0.754, 0.069, 0.894, 0.652] rim [0.589, 0.179, 0.805, 0.613]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 1.5 (aggregate of 45 individuals; 3/45 membrane-like individually; rim level 0.331)
  - radial food c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.82, rim/outside 1 (aggregate of 45 individuals; 1/45 membrane-like individually; rim level 0.435)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 1.51 (aggregate of 45 individuals; 3/45 membrane-like individually; rim level 0.46)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 1.12 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.494)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #116 (t=840, R_eq 13.05, ring): none; #258 (t=2440, R_eq 5.38): none; #320 (t=3280, R_eq 5.92): none; #323 (t=3320, R_eq 9.72): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
