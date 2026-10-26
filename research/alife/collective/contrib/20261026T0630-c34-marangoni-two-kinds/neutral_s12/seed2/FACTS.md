# Evidence pack: active-nematic-marangoni-two-kinds (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 447s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0630-c34-marangoni-two-kinds/world.py --out collective/contrib/20261026T0630-c34-marangoni-two-kinds/neutral_s12 --seeds 1 2 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8387, 0.5696], min area 6 px

## Measurements
- components: final 31, mean 23.1, max 32; occupancy final 0.09
- tracks: 118; persistent (alive >= 50% of run): 11; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 31, 30], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.281/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 18, merge/split ratio 0.4, nucleations 10
- channel total drift (end/start - 1): [-0.5106, -0.382, 3.5467, 14.5484]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 118: holes 0, rim-vs-core 0.62, rim-vs-outside 0.35, heterogeneity 0.16; core [0.942, 0.798, 0.006, 0.445] rim [0.732, 0.474, 0.014, 0.93]
  - track 28 at frame 128: holes 0, rim-vs-core 0.61, rim-vs-outside 0.35, heterogeneity 0.15; core [0.95, 0.758, 0.02, 0.439] rim [0.753, 0.462, 0.048, 0.929]
  - track 33 at frame 128: holes 0, rim-vs-core 0.44, rim-vs-outside 0.29, heterogeneity 0.13; core [0.913, 0.587, 0.597, 0.031] rim [0.746, 0.421, 0.966, 0.061]
  - track 80 at frame 168: holes 0, rim-vs-core 0.61, rim-vs-outside 0.34, heterogeneity 0.18; core [0.959, 0.619, 0.45, 0.02] rim [0.742, 0.435, 0.993, 0.054]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.58 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.702)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 8.6 (aggregate of 152 individuals; 14/152 membrane-like individually; rim level 0.536)
  - radial surfactant A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 2.8 (aggregate of 152 individuals; 42/152 membrane-like individually; rim level 0.129)
  - radial surfactant B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.17 (aggregate of 152 individuals; 69/152 membrane-like individually; rim level 0.496)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=590, R_eq 3.99): none; #28 (t=640, R_eq 3.87): ['surfactant B']; #33 (t=640, R_eq 4.11): none; #80 (t=840, R_eq 4.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
