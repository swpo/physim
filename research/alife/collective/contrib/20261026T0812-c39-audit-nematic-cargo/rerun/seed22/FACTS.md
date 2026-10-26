# Evidence pack: active-nematic-cargo (seed 22)

- world: `../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 384s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/c39-audit-wip/rerun/seed22 --seeds 22 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8262, 0.6242], min area 6 px

## Measurements
- components: final 31, mean 18.7, max 31; occupancy final 0.06
- tracks: 83; persistent (alive >= 50% of run): 11; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 31], H1 [1, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0926/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 9, merge/split ratio 0.273, nucleations 8
- channel total drift (end/start - 1): [-0.5066, -0.4224, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 116: holes 0, rim-vs-core 0.61, rim-vs-outside 0.30, heterogeneity 0.20; core [0.881, 0.746, 0.452, 0.503] rim [0.718, 0.534, 0.736, 0.03]
  - track 21 at frame 121: holes 0, rim-vs-core 0.64, rim-vs-outside 0.36, heterogeneity 0.20; core [0.93, 0.867, 0.35, 0.442] rim [0.732, 0.59, 0.681, 0.016]
  - track 13 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.32, heterogeneity 0.23; core [0.938, 0.701, 0.474, 0.485] rim [0.733, 0.48, 0.92, 0.016]
  - track 61 at frame 176: holes 0, rim-vs-core 0.74, rim-vs-outside 0.40, heterogeneity 0.23; core [0.963, 0.948, 0.315, 0.406] rim [0.724, 0.619, 0.792, 0.009]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.74 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.753)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 8.09 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.644)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 2.89 (aggregate of 129 individuals; 98/129 membrane-like individually; rim level 0.558)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.273, rim/outside 1.72 (aggregate of 129 individuals; 10/129 membrane-like individually; rim level 0.154)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #12 (t=580, R_eq 3.61): none; #21 (t=605, R_eq 3.29): ['surfactant s']; #13 (t=505, R_eq 4.72): none; #61 (t=880, R_eq 3.19): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
