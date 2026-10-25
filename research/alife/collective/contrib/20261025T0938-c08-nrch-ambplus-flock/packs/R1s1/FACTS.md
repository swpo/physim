# Evidence pack: nrch (seed 1)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 806s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/R1s1 --seeds 1 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0223, 1.0091], min area 6 px

## Measurements
- components: final 8, mean 6.1, max 15; occupancy final 0.18
- tracks: 107; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.214/time; max body lengths 16.4
- replication (lineage window K = 20 frames = time 1000, default): splits 22, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.409, nucleations 55
- channel total drift (end/start - 1): [-0.0735, 53.9655]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 70: holes 0, rim-vs-core 0.24, rim-vs-outside 0.36, heterogeneity 0.18; core [0.882, 0.274] rim [0.666, 0.369]
  - track 74 at frame 99: holes 0, rim-vs-core 0.16, rim-vs-outside 0.54, heterogeneity 0.19; core [0.949, 0.374] rim [0.785, 0.387]
  - track 78 at frame 100: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.19; core [0.936, 0.306] rim [0.676, 0.351]
  - track 101 at frame 109: holes 0, rim-vs-core 0.24, rim-vs-outside 0.50, heterogeneity 0.20; core [0.965, 0.397] rim [0.732, 0.355]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 6.04 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.751)
  - radial psi: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.957 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.532)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=3500, R_eq 13.53): none; #74 (t=4950, R_eq 20.6): none; #78 (t=5000, R_eq 13.91): none; #101 (t=5450, R_eq 19.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
