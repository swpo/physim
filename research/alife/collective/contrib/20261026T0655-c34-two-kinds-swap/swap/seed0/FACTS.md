# Evidence pack: active-nematic-marangoni-two-kinds (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 463s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/20261026T0655-c34-two-kinds-swap/swap --seeds 0 1 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8401, 0.6457], min area 6 px

## Measurements
- components: final 33, mean 23.0, max 33; occupancy final 0.09
- tracks: 93; persistent (alive >= 50% of run): 17; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 32], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.277/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 100, default): splits 37, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 10, merge/split ratio 0.27, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.3353, 3.4563, 15.5516]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 119: holes 0, rim-vs-core 0.66, rim-vs-outside 0.41, heterogeneity 0.16; core [0.967, 0.965, 0.299, 0.021] rim [0.759, 0.693, 0.863, 0.069]
  - track 21 at frame 121: holes 0, rim-vs-core 0.63, rim-vs-outside 0.36, heterogeneity 0.15; core [0.956, 0.778, 0.002, 0.28] rim [0.757, 0.435, 0.007, 0.763]
  - track 22 at frame 121: holes 0, rim-vs-core 0.67, rim-vs-outside 0.37, heterogeneity 0.16; core [0.957, 0.938, 0.318, 0.019] rim [0.724, 0.607, 0.846, 0.058]
  - track 75 at frame 163: holes 0, rim-vs-core 0.65, rim-vs-outside 0.38, heterogeneity 0.15; core [0.965, 0.842, 0.004, 0.269] rim [0.762, 0.477, 0.011, 0.768]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 157 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 5.09 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.735)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 9.71 (aggregate of 157 individuals; 7/157 membrane-like individually; rim level 0.556)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.07, rim/outside 3.18 (aggregate of 157 individuals; 69/157 membrane-like individually; rim level 0.168)  MEMBRANE-LIKE
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 3.44 (aggregate of 157 individuals; 87/157 membrane-like individually; rim level 0.491)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant A
- membrane-like channels per top track at mid-life: #16 (t=595, R_eq 3.74): ['surfactant A', 'surfactant B']; #21 (t=605, R_eq 2.93): ['surfactant B']; #22 (t=605, R_eq 3.29): ['surfactant A', 'surfactant B']; #75 (t=815, R_eq 3.09): ['surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
