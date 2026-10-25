# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 714s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/K3s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.51 of robust range [-0.9413, 0.9206], min area 6 px

## Measurements
- components: final 16, mean 14.6, max 27; occupancy final 0.20
- tracks: 93; persistent (alive >= 50% of run): 16; longest 217 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.69 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.233/time; max body lengths 57.0
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 18, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.556, nucleations 49
- channel total drift (end/start - 1): [-0.0731, 769.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 133: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.20; core [0.924, 0.34] rim [0.665, 0.394]
  - track 8 at frame 133: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.93, 0.389] rim [0.666, 0.402]
  - track 36 at frame 135: holes 0, rim-vs-core 0.26, rim-vs-outside 0.34, heterogeneity 0.20; core [0.911, 0.362] rim [0.658, 0.397]
  - track 89 at frame 153: holes 0, rim-vs-core 0.26, rim-vs-outside 0.33, heterogeneity 0.20; core [0.926, 0.347] rim [0.669, 0.395]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 8.21 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.777)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.947 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.55)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=3325, R_eq 12.02): none; #8 (t=3325, R_eq 12.23): none; #36 (t=3375, R_eq 12.17): none; #89 (t=3825, R_eq 11.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
