# run with WORLD_P='{"Dt":-0.3,"D":0.04}'
# Evidence pack: nrch (seed 4)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1361s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py --out collective/contrib/20261025T1142-c02-review-c08-nrch-nodiv/N2/seed4 --seeds 4 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.1096, 1.1258], min area 6 px

## Measurements
- components: final 5, mean 7.5, max 23; occupancy final 0.22
- tracks: 172; persistent (alive >= 50% of run): 4; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.32 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [1, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.216/time; max body lengths 13.7
- replication (lineage window K = 20 frames = time 500, default): splits 35, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 30, merge/split ratio 0.857, nucleations 74
- channel total drift (end/start - 1): [0.0, 33.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 150 at frame 161: holes 0, rim-vs-core 0.16, rim-vs-outside 0.52, heterogeneity 0.17; core [0.913, 0.347] rim [0.757, 0.393]
  - track 158 at frame 169: holes 0, rim-vs-core 0.16, rim-vs-outside 0.55, heterogeneity 0.17; core [0.931, 0.352] rim [0.77, 0.348]
  - track 162 at frame 171: holes 0, rim-vs-core 0.21, rim-vs-outside 0.49, heterogeneity 0.18; core [0.931, 0.404] rim [0.727, 0.38]
  - track 167 at frame 177: holes 0, rim-vs-core 0.22, rim-vs-outside 0.51, heterogeneity 0.19; core [0.941, 0.439] rim [0.73, 0.377]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 6.45 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.785)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.985 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.552)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #150 (t=4025, R_eq 22.02): none; #158 (t=4225, R_eq 23.43): none; #162 (t=4275, R_eq 19.53): none; #167 (t=4425, R_eq 23.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
