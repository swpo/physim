# Evidence pack: chiral-eating-flocks (seed 42)

- world: `../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c57-w14/chi0.2 --seeds 42 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5125], min area 6 px

## Measurements
- components: final 64, mean 53.8, max 64; occupancy final 0.43
- tracks: 580; persistent (alive >= 50% of run): 55; longest 281 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.61 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 65, 65], H1 [35, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 200, default): splits 187, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 158, merge/split ratio 0.845, nucleations 1
- channel total drift (end/start - 1): [1.0814, -0.4994, -0.2673, -0.8005]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 171 at frame 161: holes 0, rim-vs-core 0.25, rim-vs-outside 0.76, heterogeneity 0.15; core [0.814, 0.106, 0.894, 0.104] rim [0.679, 0.188, 0.736, 0.218]
  - track 173 at frame 161: holes 0, rim-vs-core 0.22, rim-vs-outside 0.77, heterogeneity 0.14; core [0.794, 0.096, 0.865, 0.037] rim [0.686, 0.193, 0.731, 0.124]
  - track 181 at frame 161: holes 0, rim-vs-core 0.45, rim-vs-outside 0.59, heterogeneity 0.14; core [0.848, 0.073, 0.914, 0.033] rim [0.591, 0.257, 0.64, 0.19]
  - track 526 at frame 232: holes 0, rim-vs-core 0.49, rim-vs-outside 0.31, heterogeneity 0.14; core [0.79, 0.125, 0.846, 0.09] rim [0.489, 0.301, 0.54, 0.235]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 343 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 2.83 (aggregate of 343 individuals; 1/343 membrane-like individually; rim level 0.742)
  - radial food c: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 9.07, rim/outside 1.06 (aggregate of 343 individuals; 0/343 membrane-like individually; rim level 0.46)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 3.04 (aggregate of 343 individuals; 1/343 membrane-like individually; rim level 0.799)
  - radial p_x: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 343 individuals; 0/343 membrane-like individually; rim level 0.504)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #171 (t=1610, R_eq 6.36): none; #173 (t=1610, R_eq 6.02): none; #181 (t=1610, R_eq 6.08): none; #526 (t=2320, R_eq 5.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 343 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
