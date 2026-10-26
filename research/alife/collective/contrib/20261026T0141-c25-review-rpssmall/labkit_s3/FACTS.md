# Evidence pack: rps-lenia-cyclic (seed 3)

- world: `../../20261025T2349-c26-rps-lenia/world.py`, family `lenia`
- parent: collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py; mutation: three MIRd+ kinds with cyclic / transitive / no predation between kinds
- run: 31 frames x 20 steps x dt 0.1 = time 60; grid [96, 96]; wall 15s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2349-c26-rps-lenia/world.py --out collective/contrib/20261026T0141-c25-review-rpssmall/labkit_s3 --seeds 3 --frames 30 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 10, mean 7.5, max 10; occupancy final 0.15
- tracks: 35; persistent (alive >= 50% of run): 3; longest 30 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.40 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 13, 9], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.336/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 40, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.727, nucleations 5
- channel total drift (end/start - 1): [1.3042, 1.3231, 1.1958, 1.3779, 1.042, 0.8611, 0.5196, 0.4137, 0.5383, -0.5275]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 16: holes 0, rim-vs-core 0.29, rim-vs-outside 0.69, heterogeneity 0.10; core [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.952, 0.602, 0.141, 0.045] rim [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.703, 0.66, 0.232, 0.14]
  - track 6 at frame 13: holes 0, rim-vs-core 0.24, rim-vs-outside 0.85, heterogeneity 0.11; core [0.0, 0.0, 0.0, 0.992, 0.502, 0.055, 0.0, 0.0, 0.0, 0.679] rim [0.0, 0.0, 0.0, 0.833, 0.641, 0.178, 0.0, 0.003, 0.008, 0.674]
  - track 9 at frame 10: holes 0, rim-vs-core 0.27, rim-vs-outside 0.74, heterogeneity 0.11; core [0.994, 0.732, 0.141, 0.0, 0.0, 0.0, 0.0, 0.0, 0.033, 0.438] rim [0.746, 0.665, 0.079, 0.0, 0.0, 0.0, 0.0, 0.011, 0.068, 0.49]
  - track 18 at frame 23: holes 0, rim-vs-core 0.25, rim-vs-outside 0.84, heterogeneity 0.09; core [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.732, 0.094, 0.357] rim [0.0, 0.0, 0.005, 0.0, 0.0, 0.0, 0.81, 0.576, 0.125, 0.358]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [5, 10, 15, 20, 25, 30]):
  - radial K0c0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 11.9 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.331)
  - radial K0c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 2.3 (aggregate of 45 individuals; 7/45 membrane-like individually; rim level 0.283)  MEMBRANE-LIKE
  - radial K0c2: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 1.12 (aggregate of 45 individuals; 9/45 membrane-like individually; rim level 0.0993)
  - radial K1c0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 14.4 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.306)
  - radial K1c1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.33 (aggregate of 45 individuals; 4/45 membrane-like individually; rim level 0.268)
  - radial K1c2: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.9, rim/outside 1.19 (aggregate of 45 individuals; 12/45 membrane-like individually; rim level 0.0959)
  - radial K2c0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 12 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.25)
  - radial K2c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 1.87 (aggregate of 45 individuals; 7/45 membrane-like individually; rim level 0.176)  MEMBRANE-LIKE
  - radial K2c2: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 2.27, rim/outside 1.11 (aggregate of 45 individuals; 6/45 membrane-like individually; rim level 0.0897)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.829 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.398)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): K0c1, K2c1
- membrane-like channels per top track at mid-life: #10 (t=32, R_eq 7.27): ['K2c2']; #6 (t=26, R_eq 7.46): none; #9 (t=20, R_eq 7.09): ['K0c1']; #18 (t=46, R_eq 7.29): none
- species `k0` (channels ['K0c0'], own threshold): components final 4, mean 2.7, max 4; tracks 15, persistent 1; splits 5, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 0.8; moving tracks 0
- species `k1` (channels ['K1c0'], own threshold): components final 4, mean 2.8, max 4; tracks 12, persistent 2; splits 3, persistent splits 0 (K=20), max generation 0, merges 3, merge/split 1; moving tracks 1
- species `k2` (channels ['K2c0'], own threshold): components final 2, mean 2.0, max 3; tracks 6, persistent 1; splits 2, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.5; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
