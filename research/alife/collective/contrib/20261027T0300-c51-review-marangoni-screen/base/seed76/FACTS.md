# Evidence pack: active-nematic-marangoni (seed 76)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 272s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261027T0300-c51-review-marangoni-screen/base/seed76 --seeds 76 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8411, 0.5689], min area 6 px

## Measurements
- components: final 31, mean 22.4, max 32; occupancy final 0.09
- tracks: 92; persistent (alive >= 50% of run): 14; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 33, 31], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.282/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 11, merge/split ratio 0.306, nucleations 8
- channel total drift (end/start - 1): [-0.495, -0.4417, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 111: holes 0, rim-vs-core 0.43, rim-vs-outside 0.41, heterogeneity 0.15; core [0.947, 0.661, 0.42, 0.0] rim [0.822, 0.428, 0.76, 0.0]
  - track 19 at frame 118: holes 0, rim-vs-core 0.58, rim-vs-outside 0.34, heterogeneity 0.14; core [0.959, 0.713, 0.385, 0.0] rim [0.756, 0.448, 0.865, 0.0]
  - track 26 at frame 126: holes 0, rim-vs-core 0.58, rim-vs-outside 0.34, heterogeneity 0.14; core [0.963, 0.728, 0.366, 0.0] rim [0.769, 0.468, 0.845, 0.0]
  - track 56 at frame 153: holes 0, rim-vs-core 0.47, rim-vs-outside 0.41, heterogeneity 0.15; core [0.932, 0.829, 0.436, 0.0] rim [0.762, 0.56, 0.782, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.71 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.711)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 9.45 (aggregate of 151 individuals; 10/151 membrane-like individually; rim level 0.555)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.32 (aggregate of 151 individuals; 62/151 membrane-like individually; rim level 0.606)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 151 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=555, R_eq 4.44): none; #19 (t=590, R_eq 4.22): none; #26 (t=630, R_eq 3.99): none; #56 (t=765, R_eq 3.87): ['surfactant s']

## Warnings
- radial: 4 of 151 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
