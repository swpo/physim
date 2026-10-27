# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 92)

- world: `../../../../collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 459s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py --out collective/contrib/20261027T0607-c52-review-sink-escape/I/seed92 --seeds 92 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.945, 0.5713], min area 6 px

## Measurements
- components: final 20, mean 21.2, max 28; occupancy final 0.07
- tracks: 151; persistent (alive >= 50% of run): 8; longest 266 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 20, 18], H1 [0, 0, 0]
- motion: 82 long-lived tracks moved >= 1 body length; max speed 0.34/time; max body lengths 15.3
- replication (lineage window K = 20 frames = time 100, default): splits 59, persistent splits 38 (0 more failed only because the siblings re-merged within K), max generation 4, merges 21, merge/split ratio 0.356, nucleations 11
- channel total drift (end/start - 1): [-0.5718, -0.5654, None, -0.0199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 167: holes 0, rim-vs-core 0.62, rim-vs-outside 0.32, heterogeneity 0.15; core [0.959, 0.693, 0.406, 1.0] rim [0.759, 0.412, 0.924, 1.0]
  - track 49 at frame 196: holes 0, rim-vs-core 0.58, rim-vs-outside 0.35, heterogeneity 0.14; core [0.953, 0.874, 0.344, 1.0] rim [0.761, 0.535, 0.767, 1.0]
  - track 32 at frame 161: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.14; core [0.954, 0.786, 0.387, 1.0] rim [0.76, 0.477, 0.826, 1.0]
  - track 91 at frame 247: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.12; core [0.941, 0.856, 0.365, 1.0] rim [0.774, 0.587, 0.703, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 134 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 3.26 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.719)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 8.42 (aggregate of 134 individuals; 12/134 membrane-like individually; rim level 0.535)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.17 (aggregate of 134 individuals; 61/134 membrane-like individually; rim level 0.589)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=835, R_eq 4.3): none; #49 (t=980, R_eq 3.43): ['surfactant s']; #32 (t=805, R_eq 3.99): none; #91 (t=1235, R_eq 3.74): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 134 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
