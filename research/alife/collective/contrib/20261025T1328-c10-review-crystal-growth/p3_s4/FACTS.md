# Evidence pack: nrch (seed 4)

- world: `../../20261025T1114-c08-crystal-growth-negative/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 890s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1114-c08-crystal-growth-negative/world.py --out collective/contrib/20261025T1328-c10-review-crystal-growth/p3_s4 --seeds 4 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9202, 0.9347], min area 6 px

## Measurements
- components: final 27, mean 26.2, max 47; occupancy final 0.27
- tracks: 275; persistent (alive >= 50% of run): 27; longest 221 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 27, 27], H1 [0, 0, 0]
- motion: 37 long-lived tracks moved >= 1 body length; max speed 0.289/time; max body lengths 79.9
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 67, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 61, merge/split ratio 0.91, nucleations 87
- channel total drift (end/start - 1): [0.1589, 49.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 172 at frame 131: holes 0, rim-vs-core 0.25, rim-vs-outside 0.38, heterogeneity 0.20; core [0.929, 0.396] rim [0.678, 0.42]
  - track 178 at frame 131: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.928, 0.403] rim [0.665, 0.431]
  - track 199 at frame 133: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.928, 0.404] rim [0.666, 0.425]
  - track 240 at frame 145: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.93, 0.403] rim [0.673, 0.423]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 158 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 7.87 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.807)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.96 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.584)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #172 (t=3275, R_eq 10.42): none; #178 (t=3275, R_eq 10.72): none; #199 (t=3325, R_eq 11.38): none; #240 (t=3625, R_eq 11.16): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
