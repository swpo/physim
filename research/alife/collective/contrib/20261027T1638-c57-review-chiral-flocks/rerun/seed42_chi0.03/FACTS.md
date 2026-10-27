# Evidence pack: chiral-eating-flocks (seed 42)

- world: `../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c57-w14/chi0.03 --seeds 42 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.758], min area 6 px

## Measurements
- components: final 13, mean 14.7, max 28; occupancy final 0.24
- tracks: 2441; persistent (alive >= 50% of run): 0; longest 10 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 17, 10], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 200, default): splits 863, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 828, merge/split ratio 0.959, nucleations 41
- channel total drift (end/start - 1): [0.8909, -0.4327, -0.3682, 1.1554]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 13: holes 0, rim-vs-core 0.31, rim-vs-outside 0.64, heterogeneity 0.17; core [0.743, 0.074, 0.9, 0.775] rim [0.58, 0.258, 0.796, 0.612]
  - track 426 at frame 63: holes 0, rim-vs-core 0.23, rim-vs-outside 0.64, heterogeneity 0.16; core [0.738, 0.103, 0.894, 0.77] rim [0.582, 0.233, 0.793, 0.711]
  - track 45 at frame 8: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.13; core [0.73, 0.075, 0.902, 0.223] rim [0.547, 0.215, 0.779, 0.221]
  - track 65 at frame 10: holes 0, rim-vs-core 0.11, rim-vs-outside 0.20, heterogeneity 0.06; core [0.551, 0.357, 0.713, 0.528] rim [0.478, 0.397, 0.637, 0.514]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.9 (aggregate of 94 individuals; 10/94 membrane-like individually; rim level 0.472)
  - radial food c: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.92, rim/outside 0.823 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.449)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 3.07 (aggregate of 94 individuals; 6/94 membrane-like individually; rim level 0.67)
  - radial p_x: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.994 (aggregate of 94 individuals; 1/94 membrane-like individually; rim level 0.482)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=130, R_eq 9.85, ring): none; #426 (t=630, R_eq 8.33, ring): ['density rho']; #45 (t=80, R_eq 6.23): none; #65 (t=100, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
