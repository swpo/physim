# Evidence pack: active-nematic-marangoni-two-kinds (seed 20)

- world: `../../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 723s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/Bswims/s20 --seeds 20 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.841, 0.6817], min area 6 px

## Measurements
- components: final 30, mean 23.1, max 31; occupancy final 0.09
- tracks: 90; persistent (alive >= 50% of run): 14; longest 170 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.363/time; max body lengths 11.1
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 11, merge/split ratio 0.314, nucleations 9
- channel total drift (end/start - 1): [-0.494, -0.3555, 4.5689, 15.1979]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 116: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.14; core [0.934, 0.754, 0.41, 0.027] rim [0.724, 0.516, 0.852, 0.064]
  - track 22 at frame 119: holes 0, rim-vs-core 0.78, rim-vs-outside 0.43, heterogeneity 0.19; core [0.993, 0.943, 0.256, 0.023] rim [0.777, 0.661, 0.946, 0.097]
  - track 24 at frame 121: holes 0, rim-vs-core 0.50, rim-vs-outside 0.30, heterogeneity 0.14; core [0.926, 0.583, 0.011, 0.437] rim [0.731, 0.4, 0.026, 0.862]
  - track 72 at frame 168: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.15; core [0.928, 0.668, 0.009, 0.43] rim [0.718, 0.404, 0.021, 0.903]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 156 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 4.98 (aggregate of 156 individuals; 0/156 membrane-like individually; rim level 0.727)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 9.72 (aggregate of 156 individuals; 5/156 membrane-like individually; rim level 0.56)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 2.86 (aggregate of 156 individuals; 61/156 membrane-like individually; rim level 0.147)  MEMBRANE-LIKE
  - radial surfactant B: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 3.26 (aggregate of 156 individuals; 80/156 membrane-like individually; rim level 0.475)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant A
- membrane-like channels per top track at mid-life: #13 (t=580, R_eq 4.07): none; #22 (t=595, R_eq 4.37): ['surfactant A', 'surfactant B']; #24 (t=605, R_eq 4.41): ['order |Q|']; #72 (t=840, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
