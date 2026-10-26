# Evidence pack: rps-lenia-cyclic (seed 3)

- world: `../world.py`, family `lenia`
- parent: collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py; mutation: three MIRd+ kinds with cyclic / transitive / no predation between kinds
- run: 81 frames x 20 steps x dt 0.1 = time 160; grid [160, 160]; wall 78s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27s/world.py --out collective/contrib/wip-c27s/pack_cyclic --seeds 3 --frames 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 40, mean 21.0, max 40; occupancy final 0.25
- tracks: 234; persistent (alive >= 50% of run): 2; longest 49 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.62 (1 = constant size)
- enclosures: components with a hole mean 0.30, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [68, 45, 38], H1 [4, 1, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.659/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 40, default): splits 80, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 47, merge/split ratio 0.588, nucleations 44
- channel total drift (end/start - 1): [2.5818, 1.8167, 1.7432, 13.4778, 9.8026, 8.1242, 8.3263, 5.7354, 4.9702, -0.6454]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 56: holes 0, rim-vs-core 0.24, rim-vs-outside 0.96, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.736, 0.23, 0.0, 0.0, 0.0, 0.572] rim [0.0, 0.0, 0.0, 0.875, 0.922, 0.144, 0.0, 0.0, 0.0, 0.564]
  - track 62 at frame 55: holes 0, rim-vs-core 0.26, rim-vs-outside 0.84, heterogeneity 0.14; core [0.0, 0.0, 0.0, 0.001, 0.022, 0.197, 0.93, 0.918, 0.144, 0.032] rim [0.0, 0.0, 0.0, 0.0, 0.074, 0.183, 0.739, 0.807, 0.265, 0.079]
  - track 34 at frame 41: holes 0, rim-vs-core 0.35, rim-vs-outside 0.81, heterogeneity 0.11; core [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.914, 0.884, 0.44, 0.305] rim [0.0, 0.0, 0.0, 0.0, 0.0, 0.005, 0.723, 0.746, 0.194, 0.367]
  - track 87 at frame 52: holes 0, rim-vs-core 0.52, rim-vs-outside 0.86, heterogeneity 0.13; core [0.0, 0.0, 0.009, 0.997, 0.669, 0.604, 0.0, 0.0, 0.0, 0.261] rim [0.0, 0.0, 0.058, 0.793, 0.987, 0.254, 0.0, 0.0, 0.0, 0.279]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial K0c0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 6.41 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.122)
  - radial K0c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 2.4 (aggregate of 133 individuals; 10/133 membrane-like individually; rim level 0.111)
  - radial K0c2: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 1.01 (aggregate of 133 individuals; 10/133 membrane-like individually; rim level 0.0438)
  - radial K1c0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 13.2 (aggregate of 133 individuals; 1/133 membrane-like individually; rim level 0.427)
  - radial K1c1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.79, rim/outside 3.91 (aggregate of 133 individuals; 41/133 membrane-like individually; rim level 0.428)  MEMBRANE-LIKE
  - radial K1c2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.653, rim/outside 1.44 (aggregate of 133 individuals; 22/133 membrane-like individually; rim level 0.128)
  - radial K2c0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 10.7 (aggregate of 133 individuals; 4/133 membrane-like individually; rim level 0.328)
  - radial K2c1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.46 (aggregate of 133 individuals; 27/133 membrane-like individually; rim level 0.304)
  - radial K2c2: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.25 (aggregate of 133 individuals; 31/133 membrane-like individually; rim level 0.104)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.829 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.347)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): K1c1
- membrane-like channels per top track at mid-life: #63 (t=112, R_eq 6.96): ['K1c1']; #62 (t=110, R_eq 7.23): none; #34 (t=82, R_eq 7.8): ['K2c2']; #87 (t=104, R_eq 6.84): ['K1c1']
- species `k0` (channels ['K0c0'], own threshold): components final 5, mean 3.4, max 6; tracks 30, persistent 1; splits 10, persistent splits 1 (K=20), max generation 1, merges 5, merge/split 0.5; moving tracks 4
- species `k1` (channels ['K1c0'], own threshold): components final 21, mean 9.7, max 22; tracks 111, persistent 1; splits 39, persistent splits 5 (K=20), max generation 2, merges 21, merge/split 0.538; moving tracks 0
- species `k2` (channels ['K2c0'], own threshold): components final 16, mean 8.6, max 16; tracks 72, persistent 2; splits 24, persistent splits 5 (K=20), max generation 2, merges 10, merge/split 0.417; moving tracks 5

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
