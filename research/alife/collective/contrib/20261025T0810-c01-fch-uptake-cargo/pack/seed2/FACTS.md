# Evidence pack: fch-uptake-micelles (seed 2)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 85s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out collective/contrib/20261025T0810-c01-fch-uptake-cargo/pack --seeds 0 1 2 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1138, 2.9836], min area 6 px

## Measurements
- components: final 59, mean 40.0, max 59; occupancy final 0.27
- tracks: 107; persistent (alive >= 50% of run): 37; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 8.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 59, 59], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 39, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.026, nucleations 17
- channel total drift (end/start - 1): [0.6575, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 50: holes 0, rim-vs-core 0.49, rim-vs-outside 0.10, heterogeneity 0.28; core [0.609, 0.214] rim [0.162, 0.001]
  - track 16 at frame 51: holes 0, rim-vs-core 0.50, rim-vs-outside 0.11, heterogeneity 0.29; core [0.611, 0.232] rim [0.168, 0.002]
  - track 22 at frame 51: holes 0, rim-vs-core 0.49, rim-vs-outside 0.16, heterogeneity 0.28; core [0.654, 0.239] rim [0.228, 0.004]
  - track 54 at frame 71: holes 0, rim-vs-core 0.48, rim-vs-outside 0.10, heterogeneity 0.25; core [0.609, 0.155] rim [0.157, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 263 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.508, rim/outside 10.5 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.482)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.034, rim/outside 2 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.0142)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=200, R_eq 5.01): none; #16 (t=204, R_eq 4.92): none; #22 (t=204, R_eq 4.98): none; #54 (t=284, R_eq 5.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
