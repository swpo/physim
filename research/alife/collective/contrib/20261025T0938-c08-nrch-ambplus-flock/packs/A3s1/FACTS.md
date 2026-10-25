# Evidence pack: nrch (seed 1)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 977s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/A3s1 --seeds 1 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0581, 1.0816], min area 6 px

## Measurements
- components: final 17, mean 12.2, max 20; occupancy final 0.20
- tracks: 379; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.248/time; max body lengths 26.0
- replication (lineage window K = 20 frames = time 1000, default): splits 54, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio 0.519, nucleations 255
- channel total drift (end/start - 1): [-0.0872, -69.6207]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 192 at frame 93: holes 0, rim-vs-core 0.17, rim-vs-outside 0.53, heterogeneity 0.20; core [0.932, 0.346] rim [0.773, 0.41]
  - track 248 at frame 98: holes 0, rim-vs-core 0.26, rim-vs-outside 0.41, heterogeneity 0.20; core [0.947, 0.337] rim [0.687, 0.385]
  - track 236 at frame 95: holes 0, rim-vs-core 0.26, rim-vs-outside 0.40, heterogeneity 0.19; core [0.934, 0.344] rim [0.672, 0.378]
  - track 276 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.41, heterogeneity 0.20; core [0.944, 0.322] rim [0.682, 0.38]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 8.13 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.827)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.996 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #192 (t=4650, R_eq 14.08): none; #248 (t=4900, R_eq 10.54): none; #236 (t=4750, R_eq 11.75): none; #276 (t=5050, R_eq 11.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
