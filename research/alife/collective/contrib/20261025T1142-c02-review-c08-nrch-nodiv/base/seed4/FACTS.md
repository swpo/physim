# run with WORLD_P='{"Dt":-0.3}'
# Evidence pack: nrch (seed 4)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1062s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py --out collective/contrib/20261025T1142-c02-review-c08-nrch-nodiv/base/seed4 --seeds 4 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0472, 1.0728], min area 6 px

## Measurements
- components: final 4, mean 5.1, max 12; occupancy final 0.22
- tracks: 62; persistent (alive >= 50% of run): 2; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 57.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.207/time; max body lengths 19.1
- replication (lineage window K = 20 frames = time 500, default): splits 14, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 16, merge/split ratio 1.14, nucleations 18
- channel total drift (end/start - 1): [0.0, 129.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 155: holes 0, rim-vs-core 0.24, rim-vs-outside 0.43, heterogeneity 0.17; core [0.931, 0.359] rim [0.692, 0.366]
  - track 5 at frame 127: holes 0, rim-vs-core 0.25, rim-vs-outside 0.42, heterogeneity 0.18; core [0.94, 0.361] rim [0.689, 0.321]
  - track 49 at frame 192: holes 0, rim-vs-core 0.21, rim-vs-outside 0.43, heterogeneity 0.18; core [0.908, 0.355] rim [0.697, 0.387]
  - track 38 at frame 129: holes 0, rim-vs-core 0.23, rim-vs-outside 0.50, heterogeneity 0.18; core [0.95, 0.392] rim [0.726, 0.367]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 6.69 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.827)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 1 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.544)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=3875, R_eq 15.77): none; #5 (t=3175, R_eq 17.32): none; #49 (t=4800, R_eq 15): none; #38 (t=3225, R_eq 19.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
