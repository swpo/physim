# Evidence pack: fch-uptake-micelles (seed 14)

- world: `../../../20261025T0810-c01-fch-uptake-cargo/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 201 frames x 400 steps x dt 0.01 (--dt; world META dt 0.02) = time 800; grid [128, 128]; wall 478s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out collective/contrib/20261025T0845-c09-review-fch-uptake/rerun_dt2/seed14 --seeds 14 --spf 400 --dt 0.01 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1187, 2.9951], min area 6 px

## Measurements
- components: final 78, mean 52.5, max 78; occupancy final 0.41
- tracks: 157; persistent (alive >= 50% of run): 41; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.23 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 83, 82], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0155/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 80, default): splits 71, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.028, nucleations 8
- channel total drift (end/start - 1): [1.3183, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 103: holes 0, rim-vs-core 0.50, rim-vs-outside 0.10, heterogeneity 0.28; core [0.604, 0.216] rim [0.156, 0.001]
  - track 32 at frame 104: holes 0, rim-vs-core 0.51, rim-vs-outside 0.10, heterogeneity 0.29; core [0.621, 0.228] rim [0.166, 0.001]
  - track 33 at frame 104: holes 0, rim-vs-core 0.49, rim-vs-outside 0.10, heterogeneity 0.27; core [0.613, 0.186] rim [0.16, 0.001]
  - track 123 at frame 171: holes 0, rim-vs-core 0.47, rim-vs-outside 0.10, heterogeneity 0.24; core [0.609, 0.134] rim [0.157, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 337 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 5.78 (aggregate of 337 individuals; 2/337 membrane-like individually; rim level 0.485)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.037, rim/outside 1.84 (aggregate of 337 individuals; 3/337 membrane-like individually; rim level 0.0149)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #29 (t=412, R_eq 5.08): none; #32 (t=416, R_eq 5.14): none; #33 (t=416, R_eq 5.17): none; #123 (t=684, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
