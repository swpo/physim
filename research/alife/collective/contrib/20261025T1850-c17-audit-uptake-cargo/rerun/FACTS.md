# Evidence pack: fch-uptake-micelles (seed 7)

- world: `../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 241s; status ok
- command: `python -m labkit.run world.py --out rerun --seeds 7 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1152, 2.9949], min area 6 px

## Measurements
- components: final 80, mean 52.3, max 80; occupancy final 0.40
- tracks: 137; persistent (alive >= 50% of run): 41; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.59 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [80, 80, 80], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0159/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 80, default): splits 54, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [1.3416, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.10, heterogeneity 0.31; core [0.625, 0.286] rim [0.17, 0.002]
  - track 10 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.09, heterogeneity 0.30; core [0.61, 0.243] rim [0.157, 0.001]
  - track 13 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.11, heterogeneity 0.29; core [0.624, 0.236] rim [0.173, 0.001]
  - track 119 at frame 188: holes 0, rim-vs-core 0.46, rim-vs-outside 0.11, heterogeneity 0.20; core [0.625, 0.091] rim [0.171, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 335 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.514, rim/outside 7.14 (aggregate of 335 individuals; 1/335 membrane-like individually; rim level 0.487)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.034, rim/outside 1.9 (aggregate of 335 individuals; 0/335 membrane-like individually; rim level 0.013)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=404, R_eq 5.14): none; #10 (t=404, R_eq 5.17): none; #13 (t=404, R_eq 5.11): none; #119 (t=752, R_eq 5.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
