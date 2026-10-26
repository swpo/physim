# Evidence pack: rps-lenia-cyclic (seed 6)

- world: `../world.py`, family `lenia`
- parent: collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py; mutation: three MIRd+ kinds with cyclic / transitive / no predation between kinds
- run: 401 frames x 20 steps x dt 0.1 = time 800; grid [96, 96]; wall 129s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0218-c32-review-rps-small/world.py --out collective/contrib/20261026T0218-c32-review-rps-small/pack96 --seeds 6 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.2477], min area 6 px

## Measurements
- components: final 16, mean 15.3, max 21; occupancy final 0.33
- tracks: 597; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 20, 14], H1 [4, 1, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.744/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 40, default): splits 211, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 7, merges 154, merge/split ratio 0.73, nucleations 44
- channel total drift (end/start - 1): [4.5134, 2.9944, 2.5208, 3.1937, 2.2385, 1.7893, 3.3875, 2.0514, 1.9149, -0.6294]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 199 at frame 178: holes 0, rim-vs-core 0.20, rim-vs-outside 0.71, heterogeneity 0.10; core [0.0, 0.085, 0.0, 0.928, 0.863, 0.167, 0.0, 0.0, 0.0, 0.003] rim [0.003, 0.18, 0.0, 0.757, 0.855, 0.176, 0.0, 0.0, 0.0, 0.042]
  - track 99 at frame 128: holes 0, rim-vs-core 0.52, rim-vs-outside 1.04, heterogeneity 0.10; core [1.0, 0.702, 0.52, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.495] rim [0.921, 1.0, 0.104, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.486]
  - track 243 at frame 205: holes 0, rim-vs-core 0.32, rim-vs-outside 1.04, heterogeneity 0.13; core [0.002, 0.0, 0.131, 0.892, 0.712, 0.226, 0.0, 0.0, 0.0, 0.256] rim [0.002, 0.036, 0.033, 0.924, 0.984, 0.099, 0.0, 0.0, 0.0, 0.265]
  - track 448 at frame 333: holes 0, rim-vs-core 0.28, rim-vs-outside 0.93, heterogeneity 0.09; core [0.0, 0.0, 0.0, 0.998, 0.963, 0.13, 0.0, 0.0, 0.0, 0.598] rim [0.0, 0.0, 0.012, 0.912, 0.692, 0.131, 0.0, 0.0, 0.0, 0.603]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial K0c0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 5.65 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.261)
  - radial K0c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.63, rim/outside 2.3 (aggregate of 97 individuals; 18/97 membrane-like individually; rim level 0.257)  MEMBRANE-LIKE
  - radial K0c2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 1.21 (aggregate of 97 individuals; 19/97 membrane-like individually; rim level 0.122)
  - radial K1c0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 5.67 (aggregate of 97 individuals; 6/97 membrane-like individually; rim level 0.358)
  - radial K1c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 2.61 (aggregate of 97 individuals; 26/97 membrane-like individually; rim level 0.367)  MEMBRANE-LIKE
  - radial K1c2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.754, rim/outside 1.33 (aggregate of 97 individuals; 22/97 membrane-like individually; rim level 0.151)
  - radial K2c0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 4.84 (aggregate of 97 individuals; 5/97 membrane-like individually; rim level 0.27)
  - radial K2c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 2.21 (aggregate of 97 individuals; 21/97 membrane-like individually; rim level 0.266)  MEMBRANE-LIKE
  - radial K2c2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.959, rim/outside 1.12 (aggregate of 97 individuals; 19/97 membrane-like individually; rim level 0.129)
  - radial F: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.934 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.341)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): K0c1, K1c1, K2c1
- membrane-like channels per top track at mid-life: #199 (t=356, R_eq 6.86): none; #99 (t=256, R_eq 6.68): ['K0c1']; #243 (t=410, R_eq 6.63): ['K1c1']; #448 (t=666, R_eq 6.96): none
- species `k0` (channels ['K0c0'], own threshold): components final 8, mean 5.9, max 11; tracks 124, persistent 2; splits 38, persistent splits 4 (K=20), max generation 2, merges 25, merge/split 0.658; moving tracks 14
- species `k1` (channels ['K1c0'], own threshold): components final 6, mean 6.7, max 10; tracks 154, persistent 0; splits 46, persistent splits 6 (K=20), max generation 4, merges 31, merge/split 0.674; moving tracks 16
- species `k2` (channels ['K2c0'], own threshold): components final 8, mean 6.0, max 11; tracks 127, persistent 0; splits 35, persistent splits 6 (K=20), max generation 3, merges 27, merge/split 0.771; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
