# Evidence pack: fch-cargo-micelles-lowD (seed 4)

- world: `../world_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0726-c03-fch-protocell/world.py; mutation: micelle-fission regime (eta1=4, eta2=5, amphiphile feed 5e-4) and chi=-3: the self-made solute partitions INTO amphiphile-rich bodies (cargo)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 118s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0901-c01-slowD-containment-law/world_lowD.py --out collective/contrib/20261025T0901-c01-slowD-containment-law/s4_D01 --seeds 4 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1165, 2.988], min area 6 px

## Measurements
- components: final 52, mean 38.9, max 52; occupancy final 0.26
- tracks: 92; persistent (alive >= 50% of run): 36; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 80, default): splits 35, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 16
- channel total drift (end/start - 1): [0.6592, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.47, rim-vs-outside 0.12, heterogeneity 0.19; core [0.621, 0.64] rim [0.175, 0.505]
  - track 7 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.11, heterogeneity 0.19; core [0.6, 0.635] rim [0.156, 0.502]
  - track 11 at frame 51: holes 0, rim-vs-core 0.17, rim-vs-outside 0.36, heterogeneity 0.18; core [0.573, 0.573] rim [0.409, 0.528]
  - track 74 at frame 89: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.16; core [0.604, 0.996] rim [0.154, 0.957]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 253 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.514, rim/outside 9.28 (aggregate of 253 individuals; 1/253 membrane-like individually; rim level 0.487)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 1.48 (aggregate of 253 individuals; 0/253 membrane-like individually; rim level 0.62)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=200, R_eq 4.92): none; #7 (t=204, R_eq 4.98): none; #11 (t=204, R_eq 4.79): none; #74 (t=356, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
