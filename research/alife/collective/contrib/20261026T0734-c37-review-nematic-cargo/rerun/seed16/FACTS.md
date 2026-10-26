# Evidence pack: active-nematic-cargo (seed 16)

- world: `../../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 639s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/wip-c37/cargo/rerun/seed16 --seeds 16 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8168, 0.585], min area 6 px

## Measurements
- components: final 21, mean 12.1, max 22; occupancy final 0.05
- tracks: 64; persistent (alive >= 50% of run): 2; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 20], H1 [1, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0729/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.308, nucleations 3
- channel total drift (end/start - 1): [-0.4968, -0.6065, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 151: holes 0, rim-vs-core 0.74, rim-vs-outside 0.34, heterogeneity 0.21; core [0.945, 0.836, 0.416, 0.605] rim [0.755, 0.574, 0.751, 0.032]
  - track 28 at frame 151: holes 0, rim-vs-core 0.72, rim-vs-outside 0.38, heterogeneity 0.22; core [0.972, 0.895, 0.325, 0.495] rim [0.79, 0.605, 0.739, 0.018]
  - track 30 at frame 151: holes 0, rim-vs-core 0.76, rim-vs-outside 0.38, heterogeneity 0.22; core [0.969, 0.971, 0.329, 0.568] rim [0.754, 0.671, 0.719, 0.024]
  - track 57 at frame 190: holes 0, rim-vs-core 0.80, rim-vs-outside 0.39, heterogeneity 0.24; core [0.964, 0.952, 0.381, 0.524] rim [0.735, 0.628, 0.853, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 4.86 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.787)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 8.29 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.697)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 2.9 (aggregate of 85 individuals; 66/85 membrane-like individually; rim level 0.621)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.368, rim/outside 1.73 (aggregate of 85 individuals; 7/85 membrane-like individually; rim level 0.245)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #27 (t=755, R_eq 3.57): none; #28 (t=755, R_eq 3.09): ['surfactant s']; #30 (t=755, R_eq 3.24): ['surfactant s']; #57 (t=950, R_eq 3.57): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
