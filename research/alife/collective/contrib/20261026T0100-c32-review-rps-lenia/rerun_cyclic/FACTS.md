# Evidence pack: rps-lenia-cyclic (seed 4)

- world: `../world.py`, family `lenia`
- parent: collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py; mutation: three MIRd+ kinds with cyclic / transitive / no predation between kinds
- run: 201 frames x 20 steps x dt 0.1 = time 400; grid [160, 160]; wall 165s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0100-c32-review-rps-lenia/world.py --out collective/contrib/20261026T0100-c32-review-rps-lenia/rerun_cyclic --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0724], min area 6 px

## Measurements
- components: final 43, mean 34.4, max 52; occupancy final 0.34
- tracks: 780; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.45, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [82, 52, 41], H1 [4, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.914/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 40, default): splits 266, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 172, merge/split ratio 0.647, nucleations 95
- channel total drift (end/start - 1): [9.5408, 6.9275, 5.9472, 13.5756, 10.1649, 8.035, 11.8278, 8.3959, 7.2785, -0.5812]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 59 at frame 76: holes 0, rim-vs-core 0.31, rim-vs-outside 0.89, heterogeneity 0.16; core [0.0, 0.0, 0.0, 0.001, 0.024, 0.208, 0.918, 0.66, 0.219, 0.298] rim [0.0, 0.0, 0.001, 0.001, 0.158, 0.116, 0.783, 0.885, 0.182, 0.308]
  - track 495 at frame 165: holes 0, rim-vs-core 0.19, rim-vs-outside 0.88, heterogeneity 0.14; core [0.0, 0.0, 0.0, 0.008, 0.012, 0.095, 0.97, 0.758, 0.167, 0.312] rim [0.0, 0.0, 0.0, 0.002, 0.04, 0.088, 0.805, 0.815, 0.114, 0.337]
  - track 129 at frame 84: holes 0, rim-vs-core 0.28, rim-vs-outside 0.80, heterogeneity 0.14; core [0.0, 0.06, 0.075, 0.953, 0.882, 0.235, 0.0, 0.0, 0.0, 0.098] rim [0.0, 0.04, 0.14, 0.732, 0.726, 0.25, 0.0, 0.0, 0.001, 0.125]
  - track 484 at frame 156: holes 0, rim-vs-core 0.29, rim-vs-outside 0.93, heterogeneity 0.16; core [0.932, 0.784, 0.127, 0.0, 0.0, 0.0, 0.0, 0.082, 0.211, 0.16] rim [0.748, 0.883, 0.25, 0.0, 0.0, 0.0, 0.01, 0.019, 0.065, 0.197]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 218 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial K0c0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 6.22 (aggregate of 218 individuals; 9/218 membrane-like individually; rim level 0.277)
  - radial K0c1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 2.25 (aggregate of 218 individuals; 44/218 membrane-like individually; rim level 0.262)  MEMBRANE-LIKE
  - radial K0c2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 1.14 (aggregate of 218 individuals; 49/218 membrane-like individually; rim level 0.112)
  - radial K1c0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 6.66 (aggregate of 218 individuals; 6/218 membrane-like individually; rim level 0.332)
  - radial K1c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 2.54 (aggregate of 218 individuals; 56/218 membrane-like individually; rim level 0.325)  MEMBRANE-LIKE
  - radial K1c2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 1.2 (aggregate of 218 individuals; 27/218 membrane-like individually; rim level 0.126)
  - radial K2c0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 5.98 (aggregate of 218 individuals; 10/218 membrane-like individually; rim level 0.289)
  - radial K2c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 2.4 (aggregate of 218 individuals; 46/218 membrane-like individually; rim level 0.279)  MEMBRANE-LIKE
  - radial K2c2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 1.18 (aggregate of 218 individuals; 45/218 membrane-like individually; rim level 0.115)
  - radial F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.907 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.327)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): K0c1, K1c1, K2c1
- membrane-like channels per top track at mid-life: #59 (t=152, R_eq 6.89): ['K1c1', 'K1c2', 'K2c1']; #495 (t=330, R_eq 6.91): ['K2c1']; #129 (t=168, R_eq 7.33): ['K0c2', 'K1c2']; #484 (t=312, R_eq 7.23): ['K0c1']
- species `k0` (channels ['K0c0'], own threshold): components final 15, mean 11.9, max 20; tracks 165, persistent 2; splits 61, persistent splits 17 (K=20), max generation 5, merges 19, merge/split 0.311; moving tracks 20
- species `k1` (channels ['K1c0'], own threshold): components final 22, mean 13.7, max 23; tracks 208, persistent 2; splits 65, persistent splits 9 (K=20), max generation 4, merges 32, merge/split 0.492; moving tracks 21
- species `k2` (channels ['K2c0'], own threshold): components final 19, mean 12.7, max 21; tracks 193, persistent 1; splits 67, persistent splits 17 (K=20), max generation 5, merges 30, merge/split 0.448; moving tracks 22

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 218 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
