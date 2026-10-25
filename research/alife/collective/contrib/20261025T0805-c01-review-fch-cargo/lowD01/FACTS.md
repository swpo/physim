# Evidence pack: fch-cargo-micelles-lowD (seed 3)

- world: `../world_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0726-c03-fch-protocell/world.py; mutation: micelle-fission regime (eta1=4, eta2=5, amphiphile feed 5e-4) and chi=-3: the self-made solute partitions INTO amphiphile-rich bodies (cargo)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 116s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0805-c01-review-fch-cargo/world_lowD.py --out collective/contrib/20261025T0805-c01-review-fch-cargo/lowD01 --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1153, 2.9878], min area 6 px

## Measurements
- components: final 52, mean 38.8, max 52; occupancy final 0.26
- tracks: 88; persistent (alive >= 50% of run): 38; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 80, default): splits 32, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.031, nucleations 20
- channel total drift (end/start - 1): [0.6636, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.47, rim-vs-outside 0.11, heterogeneity 0.19; core [0.613, 0.581] rim [0.165, 0.438]
  - track 6 at frame 51: holes 0, rim-vs-core 0.17, rim-vs-outside 0.34, heterogeneity 0.19; core [0.544, 0.586] rim [0.38, 0.538]
  - track 7 at frame 51: holes 0, rim-vs-core 0.48, rim-vs-outside 0.11, heterogeneity 0.19; core [0.612, 0.6] rim [0.159, 0.455]
  - track 44 at frame 69: holes 0, rim-vs-core 0.41, rim-vs-outside 0.22, heterogeneity 0.20; core [0.659, 0.796] rim [0.265, 0.674]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 10.1 (aggregate of 247 individuals; 1/247 membrane-like individually; rim level 0.487)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 1.5 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.64)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=200, R_eq 4.95): none; #6 (t=204, R_eq 5.01): none; #7 (t=204, R_eq 4.98): none; #44 (t=276, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
