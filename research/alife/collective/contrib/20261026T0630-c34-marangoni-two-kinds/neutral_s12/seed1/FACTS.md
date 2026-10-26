# Evidence pack: active-nematic-marangoni-two-kinds (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 450s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0630-c34-marangoni-two-kinds/world.py --out collective/contrib/20261026T0630-c34-marangoni-two-kinds/neutral_s12 --seeds 1 2 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8343, 0.5623], min area 6 px

## Measurements
- components: final 29, mean 17.7, max 32; occupancy final 0.09
- tracks: 86; persistent (alive >= 50% of run): 6; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.32 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 29, 28], H1 [0, 0, 0]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.433/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 10, merge/split ratio 0.278, nucleations 4
- channel total drift (end/start - 1): [-0.4928, -0.3995, 12.6808, 5.6678]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 136: holes 0, rim-vs-core 0.59, rim-vs-outside 0.33, heterogeneity 0.16; core [0.965, 0.649, 0.011, 0.455] rim [0.767, 0.42, 0.027, 0.96]
  - track 22 at frame 141: holes 0, rim-vs-core 0.57, rim-vs-outside 0.34, heterogeneity 0.15; core [0.952, 0.745, 0.422, 0.007] rim [0.758, 0.485, 0.886, 0.02]
  - track 24 at frame 141: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.12; core [0.918, 0.861, 0.407, 0.016] rim [0.745, 0.594, 0.74, 0.033]
  - track 49 at frame 166: holes 0, rim-vs-core 0.64, rim-vs-outside 0.40, heterogeneity 0.16; core [0.95, 0.889, 0.38, 0.021] rim [0.727, 0.501, 0.835, 0.051]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 4.73 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.724)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 9.11 (aggregate of 123 individuals; 6/123 membrane-like individually; rim level 0.564)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.29 (aggregate of 123 individuals; 59/123 membrane-like individually; rim level 0.449)
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.03 (aggregate of 123 individuals; 47/123 membrane-like individually; rim level 0.219)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=680, R_eq 4.62): ['order |Q|']; #22 (t=705, R_eq 4.3): none; #24 (t=705, R_eq 4.15): none; #49 (t=830, R_eq 3.39): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
