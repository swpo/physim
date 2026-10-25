# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 806s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/N4s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0762, 1.1042], min area 6 px

## Measurements
- components: final 3, mean 7.7, max 36; occupancy final 0.28
- tracks: 226; persistent (alive >= 50% of run): 1; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.162/time; max body lengths 16.8
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 60, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 69, merge/split ratio 1.15, nucleations 52
- channel total drift (end/start - 1): [-0.0, 513.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 178 at frame 149: holes 0, rim-vs-core 0.23, rim-vs-outside 0.38, heterogeneity 0.17; core [0.911, 0.378] rim [0.678, 0.377]
  - track 196 at frame 131: holes 0, rim-vs-core 0.18, rim-vs-outside 0.55, heterogeneity 0.16; core [0.932, 0.339] rim [0.749, 0.351]
  - track 171 at frame 83: holes 0, rim-vs-core 0.15, rim-vs-outside 0.55, heterogeneity 0.17; core [0.935, 0.454] rim [0.787, 0.47]
  - track 206 at frame 157: holes 0, rim-vs-core 0.18, rim-vs-outside 0.53, heterogeneity 0.18; core [0.947, 0.406] rim [0.766, 0.408]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 4.54 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.741)
  - radial psi: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 0.935 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.534)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #178 (t=3725, R_eq 13.05): none; #196 (t=3275, R_eq 24.05): none; #171 (t=2075, R_eq 20.78): none; #206 (t=3925, R_eq 21.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
