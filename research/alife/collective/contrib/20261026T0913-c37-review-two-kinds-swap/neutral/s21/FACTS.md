# Evidence pack: active-nematic-marangoni-two-kinds (seed 21)

- world: `../../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 739s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/neutral/s21 --seeds 21 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8408, 0.5698], min area 6 px

## Measurements
- components: final 31, mean 24.5, max 32; occupancy final 0.09
- tracks: 112; persistent (alive >= 50% of run): 12; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 31], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.309/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 3, merges 19, merge/split ratio 0.463, nucleations 11
- channel total drift (end/start - 1): [-0.5032, -0.418, 7.5306, 10.9341]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 123: holes 0, rim-vs-core 0.56, rim-vs-outside 0.31, heterogeneity 0.15; core [0.934, 0.616, 0.028, 0.501] rim [0.726, 0.387, 0.06, 0.969]
  - track 36 at frame 128: holes 0, rim-vs-core 0.63, rim-vs-outside 0.38, heterogeneity 0.16; core [0.941, 0.884, 0.042, 0.413] rim [0.707, 0.475, 0.094, 0.824]
  - track 37 at frame 129: holes 0, rim-vs-core 0.54, rim-vs-outside 0.35, heterogeneity 0.14; core [0.942, 0.806, 0.02, 0.392] rim [0.756, 0.52, 0.043, 0.81]
  - track 40 at frame 131: holes 0, rim-vs-core 0.55, rim-vs-outside 0.37, heterogeneity 0.14; core [0.941, 0.88, 0.015, 0.387] rim [0.755, 0.583, 0.033, 0.807]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.75 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.726)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 9.49 (aggregate of 163 individuals; 8/163 membrane-like individually; rim level 0.555)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 3.09 (aggregate of 163 individuals; 81/163 membrane-like individually; rim level 0.27)
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 3.22 (aggregate of 163 individuals; 91/163 membrane-like individually; rim level 0.383)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=615, R_eq 4.33): none; #36 (t=640, R_eq 3.52): ['surfactant A', 'surfactant B']; #37 (t=645, R_eq 3.74): ['surfactant A']; #40 (t=655, R_eq 3.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
