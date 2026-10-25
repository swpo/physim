# Evidence pack: nrch (seed 6)

- world: `../../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1097s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1254-c12-review-crystal-growth/world.py --out collective/contrib/20261025T1254-c12-review-crystal-growth/default/seed6 --seeds 6 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9167, 0.9008], min area 6 px

## Measurements
- components: final 22, mean 21.9, max 42; occupancy final 0.21
- tracks: 270; persistent (alive >= 50% of run): 22; longest 214 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 76.2
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 52, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 30, merge/split ratio 0.577, nucleations 138
- channel total drift (end/start - 1): [-0.0782, 7.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 134 at frame 135: holes 0, rim-vs-core 0.16, rim-vs-outside 0.47, heterogeneity 0.20; core [0.908, 0.3] rim [0.783, 0.403]
  - track 158 at frame 137: holes 0, rim-vs-core 0.20, rim-vs-outside 0.34, heterogeneity 0.20; core [0.882, 0.331] rim [0.695, 0.405]
  - track 166 at frame 137: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.932, 0.366] rim [0.678, 0.404]
  - track 261 at frame 163: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.933, 0.377] rim [0.676, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 134 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 7.82 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.779)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.95 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #134 (t=3375, R_eq 11.38): none; #158 (t=3425, R_eq 8.83): none; #166 (t=3425, R_eq 10.33): none; #261 (t=4075, R_eq 11.28): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
