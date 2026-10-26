# Evidence pack: active-nematic-marangoni-two-kinds (seed 21)

- world: `../../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 749s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/Bswims/s21 --seeds 21 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8412, 0.6649], min area 6 px

## Measurements
- components: final 28, mean 23.0, max 30; occupancy final 0.09
- tracks: 81; persistent (alive >= 50% of run): 20; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 28], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.324/time; max body lengths 7.7
- replication (lineage window K = 20 frames = time 100, default): splits 30, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 5, merges 10, merge/split ratio 0.333, nucleations 11
- channel total drift (end/start - 1): [-0.5032, -0.3862, 3.585, 14.6752]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 111: holes 0, rim-vs-core 0.60, rim-vs-outside 0.50, heterogeneity 0.17; core [0.975, 0.992, 0.337, 0.025] rim [0.795, 0.826, 0.881, 0.077]
  - track 9 at frame 111: holes 0, rim-vs-core 0.61, rim-vs-outside 0.41, heterogeneity 0.16; core [0.947, 0.956, 0.418, 0.032] rim [0.741, 0.7, 0.929, 0.086]
  - track 17 at frame 116: holes 0, rim-vs-core 0.66, rim-vs-outside 0.36, heterogeneity 0.17; core [0.956, 0.924, 0.378, 0.029] rim [0.731, 0.635, 0.92, 0.087]
  - track 70 at frame 183: holes 0, rim-vs-core 0.57, rim-vs-outside 0.40, heterogeneity 0.15; core [0.95, 0.853, 0.01, 0.308] rim [0.755, 0.505, 0.023, 0.721]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 4.77 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.71)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 8.81 (aggregate of 152 individuals; 10/152 membrane-like individually; rim level 0.539)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 2.83 (aggregate of 152 individuals; 74/152 membrane-like individually; rim level 0.169)  MEMBRANE-LIKE
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.2 (aggregate of 152 individuals; 83/152 membrane-like individually; rim level 0.455)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant A
- membrane-like channels per top track at mid-life: #6 (t=555, R_eq 4.48): ['surfactant A', 'surfactant B']; #9 (t=555, R_eq 5.01): none; #17 (t=580, R_eq 3.99): ['surfactant A', 'surfactant B']; #70 (t=915, R_eq 3.34): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
