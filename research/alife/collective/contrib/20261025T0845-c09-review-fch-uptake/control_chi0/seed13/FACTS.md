# Evidence pack: fch-uptake-micelles (seed 13)

- world: `../../../20261025T0810-c01-fch-uptake-cargo/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 121s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out collective/contrib/20261025T0845-c09-review-fch-uptake/control_chi0/seed13 --seeds 13 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1163, 2.9882], min area 6 px

## Measurements
- components: final 50, mean 38.6, max 50; occupancy final 0.26
- tracks: 82; persistent (alive >= 50% of run): 30; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 50, 50], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 28, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 21
- channel total drift (end/start - 1): [0.6648, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.14; core [0.624, 0.593] rim [0.166, 0.593]
  - track 10 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.15; core [0.618, 0.602] rim [0.162, 0.602]
  - track 11 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.15; core [0.619, 0.602] rim [0.164, 0.602]
  - track 68 at frame 85: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.14; core [0.609, 0.894] rim [0.158, 0.894]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 246 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.518, rim/outside 10.3 (aggregate of 246 individuals; 4/246 membrane-like individually; rim level 0.482)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 1 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.686)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=200, R_eq 5.08): none; #10 (t=204, R_eq 5.11): none; #11 (t=204, R_eq 5.11): none; #68 (t=340, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
