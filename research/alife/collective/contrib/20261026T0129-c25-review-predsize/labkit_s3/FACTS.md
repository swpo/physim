# Evidence pack: eco-lenia2 (seed 3)

- world: `../../20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 31 frames x 10 steps x dt 0.1 = time 30; grid [192, 192]; wall 33s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out collective/contrib/20261026T0129-c25-review-predsize/labkit_s3 --seeds 3 --frames 30 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 2, mean 2.0, max 3; occupancy final 0.01
- tracks: 7; persistent (alive >= 50% of run): 2; longest 29 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.34 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 2, 2], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.57/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 20, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [0.651, 0.4719, 0.47, None, None, None, -0.0355]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 16: holes 0, rim-vs-core 0.23, rim-vs-outside 0.79, heterogeneity 0.13; core [0.972, 0.105, 0.116, 0.0, 0.0, 0.0, 0.06] rim [0.769, 0.199, 0.107, 0.0, 0.0, 0.0, 0.097]
  - track 3 at frame 14: holes 0, rim-vs-core 0.24, rim-vs-outside 0.84, heterogeneity 0.14; core [1.0, 0.712, 0.099, 0.0, 0.0, 0.0, 0.25] rim [0.841, 0.589, 0.04, 0.0, 0.0, 0.0, 0.364]
  - track 6 at frame 29: holes 0, rim-vs-core 0.31, rim-vs-outside 0.67, heterogeneity 0.14; core [0.996, 0.603, 0.241, 0.0, 0.0, 0.0, 0.0] rim [0.712, 0.677, 0.137, 0.0, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [5, 10, 15, 20, 25, 30]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 45.7 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.9)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 1.86 (aggregate of 12 individuals; 6/12 membrane-like individually; rim level 0.51)  MEMBRANE-LIKE
  - radial A2: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.88, rim/outside 1.44 (aggregate of 12 individuals; 3/12 membrane-like individually; rim level 0.25)
  - radial B0: flat profile (no radial structure; level 0; aggregate of 12 individuals)
  - radial B1: flat profile (no radial structure; level 0; aggregate of 12 individuals)
  - radial B2: flat profile (no radial structure; level 0; aggregate of 12 individuals)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.02, rim/outside 0.629 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.252)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #4 (t=16, R_eq 7.25): none; #3 (t=14, R_eq 7.46): none; #6 (t=29, R_eq 7.2): none; #5 (t=28, R_eq 3.14): ['A2']
- species `A` (channels ['A0'], own threshold): components final 2, mean 2.0, max 3; tracks 7, persistent 2; splits 2, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.5; moving tracks 1
- species `B` (channels ['B0'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
