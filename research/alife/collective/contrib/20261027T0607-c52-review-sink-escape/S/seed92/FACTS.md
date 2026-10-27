# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 92)

- world: `../../../../collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 458s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py --out collective/contrib/20261027T0607-c52-review-sink-escape/S/seed92 --seeds 92 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9503, 0.5739], min area 6 px

## Measurements
- components: final 28, mean 22.9, max 28; occupancy final 0.08
- tracks: 136; persistent (alive >= 50% of run): 12; longest 286 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.48 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 27], H1 [0, 0, 0]
- motion: 74 long-lived tracks moved >= 1 body length; max speed 0.308/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 100, default): splits 49, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 5, merges 25, merge/split ratio 0.51, nucleations 12
- channel total drift (end/start - 1): [-0.5487, -0.4694, None, -0.0199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 169: holes 0, rim-vs-core 0.61, rim-vs-outside 0.34, heterogeneity 0.15; core [0.957, 0.751, 0.373, 1.0] rim [0.759, 0.452, 0.865, 1.0]
  - track 26 at frame 177: holes 0, rim-vs-core 0.49, rim-vs-outside 0.34, heterogeneity 0.12; core [0.917, 0.79, 0.479, 1.0] rim [0.749, 0.54, 0.87, 1.0]
  - track 53 at frame 196: holes 0, rim-vs-core 0.59, rim-vs-outside 0.34, heterogeneity 0.14; core [0.947, 0.796, 0.417, 1.0] rim [0.756, 0.482, 0.875, 1.0]
  - track 114 at frame 277: holes 0, rim-vs-core 0.52, rim-vs-outside 0.32, heterogeneity 0.13; core [0.953, 0.69, 0.363, 1.0] rim [0.776, 0.442, 0.786, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 3.33 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.731)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 8.86 (aggregate of 151 individuals; 16/151 membrane-like individually; rim level 0.528)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.14 (aggregate of 151 individuals; 67/151 membrane-like individually; rim level 0.583)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=845, R_eq 4.62): none; #26 (t=885, R_eq 5.01): none; #53 (t=980, R_eq 4.03): none; #114 (t=1385, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 151 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
