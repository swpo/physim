# Evidence pack: active-nematic-marangoni-two-kinds (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 446s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0630-c34-marangoni-two-kinds/world.py --out collective/contrib/20261026T0630-c34-marangoni-two-kinds/sel --seeds 0 --no-movie`
- segmentation: matter > 0.54 of robust range [-0.8362, 0.6986], min area 6 px

## Measurements
- components: final 33, mean 21.0, max 34; occupancy final 0.09
- tracks: 99; persistent (alive >= 50% of run): 10; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 33, 32], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.284/time; max body lengths 6.0
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 5, merges 11, merge/split ratio 0.275, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.2763, 11.5887, 7.278]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 131: holes 0, rim-vs-core 0.74, rim-vs-outside 0.35, heterogeneity 0.20; core [0.982, 0.68, 0.026, 0.266] rim [0.752, 0.468, 0.09, 0.936]
  - track 18 at frame 109: holes 0, rim-vs-core 0.41, rim-vs-outside 0.35, heterogeneity 0.10; core [0.904, 0.796, 0.005, 0.32] rim [0.724, 0.557, 0.009, 0.594]
  - track 20 at frame 111: holes 0, rim-vs-core 0.52, rim-vs-outside 0.32, heterogeneity 0.13; core [0.932, 0.839, 0.007, 0.303] rim [0.727, 0.547, 0.019, 0.675]
  - track 78 at frame 180: holes 0, rim-vs-core 0.54, rim-vs-outside 0.37, heterogeneity 0.14; core [0.929, 0.862, 0.355, 0.026] rim [0.735, 0.559, 0.75, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 144 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 5 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.728)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 9.24 (aggregate of 144 individuals; 5/144 membrane-like individually; rim level 0.587)
  - radial surfactant A: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 3.17 (aggregate of 144 individuals; 79/144 membrane-like individually; rim level 0.371)
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 3 (aggregate of 144 individuals; 83/144 membrane-like individually; rim level 0.252)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant B
- membrane-like channels per top track at mid-life: #28 (t=655, R_eq 4.11): ['surfactant A', 'surfactant B']; #18 (t=545, R_eq 3.61): ['surfactant B']; #20 (t=555, R_eq 2.93): ['surfactant A', 'surfactant B']; #78 (t=900, R_eq 3.83): ['surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 144 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
