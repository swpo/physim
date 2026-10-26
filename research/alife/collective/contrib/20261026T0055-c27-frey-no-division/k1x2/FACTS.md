# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 290s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27r/world.py --out collective/contrib/wip-c27r/k1x2 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [0.0318, 0.9941], min area 6 px

## Measurements
- components: final 6, mean 12.9, max 102; occupancy final 0.32
- tracks: 204; persistent (alive >= 50% of run): 7; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.953/time; max body lengths 7.8
- replication (lineage window K = 20 frames = time 40, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 72, merge/split ratio 3.43, nucleations 103
- channel total drift (end/start - 1): [0.0, -0.7236]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 195 at frame 58: holes 0, rim-vs-core 0.19, rim-vs-outside 0.64, heterogeneity 0.09; core [0.986, 0.007] rim [0.802, 0.056]
  - track 196 at frame 59: holes 0, rim-vs-core 0.15, rim-vs-outside 0.71, heterogeneity 0.08; core [0.981, 0.002] rim [0.837, 0.039]
  - track 197 at frame 59: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.09; core [0.976, 0.007] rim [0.728, 0.063]
  - track 163 at frame 38: holes 0, rim-vs-core 0.15, rim-vs-outside 0.60, heterogeneity 0.10; core [0.974, 0.017] rim [0.828, 0.041]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 6.17 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.814)
  - radial substrate s: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 12, rim/outside 0.865 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.219)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #195 (t=116, R_eq 11.13): none; #196 (t=118, R_eq 17.18): none; #197 (t=118, R_eq 9.41): none; #163 (t=76, R_eq 9.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
