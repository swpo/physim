# Evidence pack: active-nematic-marangoni-two-kinds (seed 2)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 466s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/20261026T0655-c34-two-kinds-swap/swap_s2 --seeds 2 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8409, 0.6097], min area 6 px

## Measurements
- components: final 31, mean 23.2, max 33; occupancy final 0.09
- tracks: 114; persistent (alive >= 50% of run): 11; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 30], H1 [0, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.337/time; max body lengths 7.1
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 5, merges 18, merge/split ratio 0.409, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.393, 2.0231, 16.3274]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 119: holes 0, rim-vs-core 0.52, rim-vs-outside 0.34, heterogeneity 0.13; core [0.93, 0.745, 0.003, 0.445] rim [0.753, 0.511, 0.006, 0.872]
  - track 24 at frame 123: holes 0, rim-vs-core 0.66, rim-vs-outside 0.41, heterogeneity 0.16; core [0.963, 0.972, 0.442, 0.022] rim [0.737, 0.664, 0.984, 0.063]
  - track 29 at frame 124: holes 0, rim-vs-core 0.69, rim-vs-outside 0.37, heterogeneity 0.17; core [0.957, 0.915, 0.442, 0.05] rim [0.722, 0.571, 0.983, 0.137]
  - track 80 at frame 170: holes 0, rim-vs-core 0.58, rim-vs-outside 0.37, heterogeneity 0.14; core [0.951, 0.876, 0.012, 0.354] rim [0.745, 0.53, 0.03, 0.777]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 156 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 4.68 (aggregate of 156 individuals; 0/156 membrane-like individually; rim level 0.715)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 8.9 (aggregate of 156 individuals; 10/156 membrane-like individually; rim level 0.538)
  - radial surfactant A: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.92, rim/outside 2.89 (aggregate of 156 individuals; 55/156 membrane-like individually; rim level 0.0947)  MEMBRANE-LIKE
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.21 (aggregate of 156 individuals; 87/156 membrane-like individually; rim level 0.543)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant A
- membrane-like channels per top track at mid-life: #20 (t=595, R_eq 4.3): none; #24 (t=615, R_eq 3.87): ['surfactant A', 'surfactant B']; #29 (t=620, R_eq 2.88): ['surfactant A', 'surfactant B']; #80 (t=850, R_eq 3.52): ['surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 156 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
