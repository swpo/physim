# Evidence pack: rps-gs-cyclic (seed 3)

- world: `../../../20261025T2027-c26-rps-control/world.py`, family `reaction-diffusion`
- parent: examples/gray_scott_mitosis; mutation: three autocatalyst kinds on one feed with cyclic predation
- run: 301 frames x 100 steps x dt 1.0 = time 30000; grid [192, 192]; wall 80s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2027-c26-rps-control/world.py --out collective/contrib/20261025T2141-c23-review-rps/pack_cyclic --seeds 3 --frames 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0015, 0.4163], min area 6 px

## Measurements
- components: final 150, mean 160.2, max 184; occupancy final 0.30
- tracks: 2457; persistent (alive >= 50% of run): 21; longest 264 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.19 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [170, 157, 146], H1 [2, 0, 0]
- motion: 126 long-lived tracks moved >= 1 body length; max speed 0.00522/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 2000, default): splits 969, persistent splits 201 (0 more failed only because the siblings re-merged within K), max generation 9, merges 417, merge/split ratio 0.43, nucleations 0
- channel total drift (end/start - 1): [-0.3274, 1.0208, 1.4029, 1.9031]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 519 at frame 169: holes 0, rim-vs-core 0.21, rim-vs-outside 0.44, heterogeneity 0.08; core [0.148, 0.856, 0.0, 0.001] rim [0.261, 0.674, 0.0, 0.001]
  - track 182 at frame 126: holes 0, rim-vs-core 0.37, rim-vs-outside 0.26, heterogeneity 0.07; core [0.123, 0.812, 0.0, 0.0] rim [0.351, 0.522, 0.0, 0.001]
  - track 237 at frame 131: holes 0, rim-vs-core 0.39, rim-vs-outside 0.28, heterogeneity 0.08; core [0.115, 0.001, 0.859, 0.0] rim [0.34, 0.001, 0.544, 0.0]
  - track 2176 at frame 282: holes 0, rim-vs-core 0.37, rim-vs-outside 0.29, heterogeneity 0.07; core [0.097, 0.0, 0.0, 0.858] rim [0.332, 0.0, 0.0, 0.576]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 964 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.6, rim/outside 0.849 (aggregate of 964 individuals; 0/964 membrane-like individually; rim level 0.563)
  - radial v0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 6.44 (aggregate of 964 individuals; 0/964 membrane-like individually; rim level 0.265)
  - radial v1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 5.86 (aggregate of 964 individuals; 0/964 membrane-like individually; rim level 0.273)
  - radial v2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 6.2 (aggregate of 964 individuals; 0/964 membrane-like individually; rim level 0.237)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #519 (t=16900, R_eq 4.33): none; #182 (t=12600, R_eq 5.17): none; #237 (t=13100, R_eq 4.55): none; #2176 (t=28200, R_eq 5.26): none
- species `k0` (channels ['v0'], own threshold): components final 45, mean 56.0, max 68; tracks 926, persistent 6; splits 352, persistent splits 61 (K=20), max generation 5, merges 175, merge/split 0.497; moving tracks 40
- species `k1` (channels ['v1'], own threshold): components final 46, mean 56.8, max 67; tracks 895, persistent 4; splits 346, persistent splits 69 (K=20), max generation 5, merges 161, merge/split 0.465; moving tracks 39
- species `k2` (channels ['v2'], own threshold): components final 58, mean 46.6, max 66; tracks 912, persistent 5; splits 344, persistent splits 54 (K=20), max generation 9, merges 180, merge/split 0.523; moving tracks 33

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
