# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 97)

- world: `../../20261026T2053-c45-marangoni-sink-escape/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 436s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py --out collective/contrib/20261027T0357-c51-review-marangoni-sink/I_s97 --seeds 97 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.63 of robust range [-0.9629, 0.5674], min area 6 px

## Measurements
- components: final 27, mean 18.7, max 27; occupancy final 0.08
- tracks: 137; persistent (alive >= 50% of run): 4; longest 219 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 27], H1 [0, 0, 0]
- motion: 74 long-lived tracks moved >= 1 body length; max speed 0.344/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 100, default): splits 56, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 7, merges 14, merge/split ratio 0.25, nucleations 11
- channel total drift (end/start - 1): [-0.5418, -0.4627, None, -0.0302]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 56 at frame 212: holes 0, rim-vs-core 0.58, rim-vs-outside 0.31, heterogeneity 0.16; core [0.96, 0.658, 0.419, 1.0] rim [0.777, 0.433, 0.917, 1.0]
  - track 22 at frame 126: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.16; core [0.976, 0.65, 0.358, 1.0] rim [0.797, 0.437, 0.869, 1.0]
  - track 14 at frame 110: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.12; core [0.942, 0.856, 0.385, 1.0] rim [0.783, 0.603, 0.74, 1.0]
  - track 104 at frame 282: holes 0, rim-vs-core 0.62, rim-vs-outside 0.34, heterogeneity 0.15; core [0.962, 0.829, 0.328, 1.0] rim [0.76, 0.44, 0.764, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 3.26 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.734)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 8.84 (aggregate of 123 individuals; 8/123 membrane-like individually; rim level 0.554)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.34 (aggregate of 123 individuals; 56/123 membrane-like individually; rim level 0.613)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.997)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #56 (t=1060, R_eq 4.55): none; #22 (t=630, R_eq 4.26): ['order |Q|']; #14 (t=550, R_eq 4.03): none; #104 (t=1410, R_eq 2.93): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
