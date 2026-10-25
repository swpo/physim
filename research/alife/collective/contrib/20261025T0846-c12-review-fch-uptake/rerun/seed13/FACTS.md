# Evidence pack: fch-uptake-micelles (seed 13)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 405s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0846-c12-review-fch-uptake/world.py --out collective/contrib/20261025T0846-c12-review-fch-uptake/rerun/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1166, 2.9941], min area 6 px

## Measurements
- components: final 81, mean 52.5, max 81; occupancy final 0.41
- tracks: 148; persistent (alive >= 50% of run): 39; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [81, 81, 81], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0194/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 80, default): splits 59, persistent splits 46 (0 more failed only because the siblings re-merged within K), max generation 5, merges 2, merge/split ratio 0.034, nucleations 21
- channel total drift (end/start - 1): [1.3297, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.10, heterogeneity 0.30; core [0.611, 0.24] rim [0.157, 0.001]
  - track 10 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.11, heterogeneity 0.28; core [0.639, 0.216] rim [0.176, 0.001]
  - track 11 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.10, heterogeneity 0.28; core [0.614, 0.201] rim [0.158, 0.001]
  - track 124 at frame 183: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.21; core [0.608, 0.098] rim [0.159, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 340 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 6.25 (aggregate of 340 individuals; 4/340 membrane-like individually; rim level 0.481)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.039, rim/outside 1.93 (aggregate of 340 individuals; 6/340 membrane-like individually; rim level 0.0149)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=404, R_eq 5.26): none; #10 (t=404, R_eq 5.14): none; #11 (t=404, R_eq 5.26): none; #124 (t=732, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
