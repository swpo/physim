# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 97)

- world: `../../20261026T2053-c45-marangoni-sink-escape/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 420s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py --out collective/contrib/20261027T0357-c51-review-marangoni-sink/S_mar0_s97 --seeds 97 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.9582, 0.6013], min area 6 px

## Measurements
- components: final 22, mean 18.5, max 26; occupancy final 0.05
- tracks: 106; persistent (alive >= 50% of run): 3; longest 269 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 22, 22], H1 [1, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.0985/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 35 (0 more failed only because the siblings re-merged within K), max generation 6, merges 6, merge/split ratio 0.136, nucleations 11
- channel total drift (end/start - 1): [-0.5352, -0.5183, None, -0.0302]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 159: holes 0, rim-vs-core 0.54, rim-vs-outside 0.38, heterogeneity 0.14; core [0.952, 0.912, 0.35, 1.0] rim [0.748, 0.605, 0.752, 1.0]
  - track 22 at frame 159: holes 0, rim-vs-core 0.50, rim-vs-outside 0.36, heterogeneity 0.13; core [0.959, 0.926, 0.331, 1.0] rim [0.78, 0.651, 0.71, 1.0]
  - track 30 at frame 113: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.13; core [0.962, 0.948, 0.32, 1.0] rim [0.766, 0.638, 0.729, 1.0]
  - track 90 at frame 304: holes 0, rim-vs-core 0.55, rim-vs-outside 0.38, heterogeneity 0.14; core [0.954, 0.924, 0.349, 1.0] rim [0.754, 0.617, 0.756, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 3.36 (aggregate of 123 individuals; 1/123 membrane-like individually; rim level 0.803)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.04 (aggregate of 123 individuals; 1/123 membrane-like individually; rim level 0.679)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.05, rim/outside 2.95 (aggregate of 123 individuals; 106/123 membrane-like individually; rim level 0.618)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #11 (t=795, R_eq 3.24): ['surfactant s']; #22 (t=795, R_eq 3.14): ['surfactant s']; #30 (t=565, R_eq 3.14): ['surfactant s']; #90 (t=1520, R_eq 3.43): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
