# Evidence pack: active-nematic-marangoni-two-kinds (seed 21)

- world: `../../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 736s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/Aswims/s21 --seeds 21 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8412, 0.6973], min area 6 px

## Measurements
- components: final 29, mean 23.8, max 33; occupancy final 0.09
- tracks: 76; persistent (alive >= 50% of run): 16; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 28], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.346/time; max body lengths 10.2
- replication (lineage window K = 20 frames = time 100, default): splits 29, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.241, nucleations 11
- channel total drift (end/start - 1): [-0.5032, -0.3244, 11.4403, 7.764]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 114: holes 0, rim-vs-core 0.65, rim-vs-outside 0.39, heterogeneity 0.17; core [0.932, 0.961, 0.031, 0.413] rim [0.714, 0.706, 0.088, 0.962]
  - track 18 at frame 118: holes 0, rim-vs-core 0.52, rim-vs-outside 0.29, heterogeneity 0.14; core [0.924, 0.46, 0.496, 0.026] rim [0.727, 0.292, 0.941, 0.06]
  - track 20 at frame 118: holes 0, rim-vs-core 0.56, rim-vs-outside 0.30, heterogeneity 0.14; core [0.925, 0.565, 0.392, 0.022] rim [0.745, 0.365, 0.878, 0.058]
  - track 46 at frame 155: holes 0, rim-vs-core 0.61, rim-vs-outside 0.39, heterogeneity 0.16; core [0.966, 0.907, 0.019, 0.218] rim [0.767, 0.616, 0.065, 0.708]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.95 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.721)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 9.02 (aggregate of 155 individuals; 8/155 membrane-like individually; rim level 0.56)
  - radial surfactant A: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.23 (aggregate of 155 individuals; 91/155 membrane-like individually; rim level 0.382)
  - radial surfactant B: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 2.98 (aggregate of 155 individuals; 93/155 membrane-like individually; rim level 0.243)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant B
- membrane-like channels per top track at mid-life: #15 (t=570, R_eq 4.69): none; #18 (t=590, R_eq 4.58): none; #20 (t=590, R_eq 4.11): none; #46 (t=775, R_eq 3.52): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
