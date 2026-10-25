# Evidence pack: ambplus-ab (seed 3)

- world: `../../20261025T0811-c08-ambplus-reaction-morphology/world.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 101 frames x 1000 steps x dt 0.03 = time 3000; grid [128, 128]; wall 272s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0811-c08-ambplus-reaction-morphology/world.py --out collective/contrib/20261025T1039-c01-review-ambplus/P --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.7988, 0.8906], min area 6 px

## Measurements
- components: final 23, mean 21.2, max 34; occupancy final 0.32
- tracks: 46; persistent (alive >= 50% of run): 22; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 24, 23], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 600, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio n/a, nucleations 35
- channel total drift (end/start - 1): [0.4215]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 60: holes 0, rim-vs-core 0.28, rim-vs-outside 0.28, heterogeneity 0.16; core [0.907] rim [0.627]
  - track 1 at frame 60: holes 0, rim-vs-core 0.29, rim-vs-outside 0.28, heterogeneity 0.16; core [0.906] rim [0.619]
  - track 2 at frame 60: holes 0, rim-vs-core 0.15, rim-vs-outside 0.41, heterogeneity 0.16; core [0.903] rim [0.751]
  - track 5 at frame 60: holes 0, rim-vs-core 0.27, rim-vs-outside 0.28, heterogeneity 0.15; core [0.905] rim [0.638]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 132 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 6.92 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.78)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1800, R_eq 7.07): none; #1 (t=1800, R_eq 7.57): none; #2 (t=1800, R_eq 7.65): none; #5 (t=1800, R_eq 6.82): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
