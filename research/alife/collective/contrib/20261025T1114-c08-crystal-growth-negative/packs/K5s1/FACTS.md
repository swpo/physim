# Evidence pack: nrch (seed 1)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 726s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/K5s1 --seeds 1 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9183, 0.9004], min area 6 px

## Measurements
- components: final 20, mean 21.2, max 38; occupancy final 0.21
- tracks: 276; persistent (alive >= 50% of run): 17; longest 205 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.276/time; max body lengths 71.5
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 52, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 34, merge/split ratio 0.654, nucleations 135
- channel total drift (end/start - 1): [-0.0779, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 201 at frame 139: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.926, 0.378] rim [0.674, 0.421]
  - track 209 at frame 139: holes 0, rim-vs-core 0.27, rim-vs-outside 0.25, heterogeneity 0.20; core [0.888, 0.366] rim [0.62, 0.425]
  - track 211 at frame 141: holes 0, rim-vs-core 0.25, rim-vs-outside 0.35, heterogeneity 0.19; core [0.902, 0.314] rim [0.662, 0.401]
  - track 271 at frame 200: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.932, 0.373] rim [0.671, 0.412]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 6.8 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.757)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.937 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.55)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #201 (t=3475, R_eq 10.33): none; #209 (t=3475, R_eq 9.67): none; #211 (t=3525, R_eq 12.13): none; #271 (t=5000, R_eq 11.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
