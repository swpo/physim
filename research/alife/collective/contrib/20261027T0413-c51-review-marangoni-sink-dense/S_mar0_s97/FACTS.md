# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 97)

- world: `../../20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 426s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out collective/contrib/20261027T0413-c51-review-marangoni-sink-dense/S_mar0_s97 --seeds 97 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0075, 0.5527], min area 6 px

## Measurements
- components: final 2, mean 7.8, max 22; occupancy final 0.01
- tracks: 54; persistent (alive >= 50% of run): 0; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 2], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0914/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.1, nucleations 11
- channel total drift (end/start - 1): [-0.8543, -0.9536, None, -0.076]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 113: holes 0, rim-vs-core 0.53, rim-vs-outside 0.44, heterogeneity 0.12; core [0.997, 0.998, 0.295, 1.0] rim [0.883, 0.866, 0.799, 1.0]
  - track 17 at frame 99: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.10; core [1.0, 0.998, 0.348, 1.0] rim [0.875, 0.809, 0.741, 1.0]
  - track 40 at frame 161: holes 0, rim-vs-core 0.54, rim-vs-outside 0.39, heterogeneity 0.13; core [0.99, 0.981, 0.411, 1.0] rim [0.816, 0.711, 0.842, 1.0]
  - track 51 at frame 280: holes 0, rim-vs-core 0.49, rim-vs-outside 0.40, heterogeneity 0.13; core [0.987, 0.957, 0.467, 1.0] rim [0.834, 0.724, 0.868, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 3.07 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.858)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 8.06 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.794)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.86, rim/outside 3.15 (aggregate of 46 individuals; 37/46 membrane-like individually; rim level 0.727)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.04 (aggregate of 46 individuals; 1/46 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #29 (t=565, R_eq 2.99): ['surfactant s']; #17 (t=495, R_eq 3.29): ['surfactant s']; #40 (t=805, R_eq 2.93): ['surfactant s']; #51 (t=1400, R_eq 3.66): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
