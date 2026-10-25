# Evidence pack: fch-uptake-micelles (seed 7)

- world: `../../../20261025T0810-c01-fch-uptake-cargo/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 162s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out collective/contrib/_c07rev6/rerun/seed7 --seeds 7 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1136, 2.987], min area 6 px

## Measurements
- components: final 51, mean 38.6, max 51; occupancy final 0.26
- tracks: 79; persistent (alive >= 50% of run): 35; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 51, 51], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 80, default): splits 25, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.6708, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 51: holes 0, rim-vs-core 0.47, rim-vs-outside 0.18, heterogeneity 0.27; core [0.65, 0.234] rim [0.239, 0.006]
  - track 7 at frame 51: holes 0, rim-vs-core 0.18, rim-vs-outside 0.34, heterogeneity 0.27; core [0.563, 0.137] rim [0.378, 0.129]
  - track 8 at frame 51: holes 0, rim-vs-core 0.52, rim-vs-outside 0.10, heterogeneity 0.31; core [0.611, 0.276] rim [0.164, 0.002]
  - track 61 at frame 89: holes 0, rim-vs-core 0.48, rim-vs-outside 0.10, heterogeneity 0.23; core [0.626, 0.123] rim [0.166, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.511, rim/outside 10.8 (aggregate of 247 individuals; 1/247 membrane-like individually; rim level 0.484)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.035, rim/outside 1.98 (aggregate of 247 individuals; 1/247 membrane-like individually; rim level 0.0147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=204, R_eq 4.98): none; #7 (t=204, R_eq 4.98): none; #8 (t=204, R_eq 4.98): none; #61 (t=356, R_eq 5.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
