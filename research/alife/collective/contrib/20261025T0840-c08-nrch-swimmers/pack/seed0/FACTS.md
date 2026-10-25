# Evidence pack: nrch (seed 0)

- world: `../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 676s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/pack_s0 --seeds 0 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0452, 1.0592], min area 6 px

## Measurements
- components: final 6, mean 6.9, max 13; occupancy final 0.22
- tracks: 60; persistent (alive >= 50% of run): 5; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.72 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 5], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.202/time; max body lengths 25.3
- replication (lineage window K = 20 frames = time 1000, default): splits 10, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.5, nucleations 36
- channel total drift (end/start - 1): [0.0, -1023.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 34 at frame 77: holes 0, rim-vs-core 0.23, rim-vs-outside 0.42, heterogeneity 0.19; core [0.929, 0.453] rim [0.696, 0.461]
  - track 45 at frame 81: holes 0, rim-vs-core 0.25, rim-vs-outside 0.35, heterogeneity 0.18; core [0.908, 0.423] rim [0.657, 0.461]
  - track 48 at frame 82: holes 0, rim-vs-core 0.24, rim-vs-outside 0.43, heterogeneity 0.18; core [0.931, 0.324] rim [0.693, 0.36]
  - track 53 at frame 96: holes 0, rim-vs-core 0.20, rim-vs-outside 0.56, heterogeneity 0.17; core [0.953, 0.336] rim [0.756, 0.325]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 5.67 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.776)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.962 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.548)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #34 (t=3850, R_eq 17.63): none; #45 (t=4050, R_eq 13.79): none; #48 (t=4100, R_eq 17.55): none; #53 (t=4800, R_eq 23.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 38 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
