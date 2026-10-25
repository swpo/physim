# Evidence pack: ambplus-ab (seed 3)

- world: `../../20261025T0811-c08-ambplus-reaction-morphology/world.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 101 frames x 1000 steps x dt 0.03 = time 3000; grid [128, 128]; wall 274s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0811-c08-ambplus-reaction-morphology/world.py --out collective/contrib/20261025T1039-c01-review-ambplus/B --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.46 of robust range [-0.9088, 1.0818], min area 6 px

## Measurements
- components: final 34, mean 27.0, max 36; occupancy final 0.32
- tracks: 41; persistent (alive >= 50% of run): 34; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 34], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 600, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 3, nucleations 36
- channel total drift (end/start - 1): [0.3845]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 59: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.16; core [0.916] rim [0.622]
  - track 1 at frame 60: holes 0, rim-vs-core 0.16, rim-vs-outside 0.45, heterogeneity 0.17; core [0.911] rim [0.754]
  - track 2 at frame 60: holes 0, rim-vs-core 0.17, rim-vs-outside 0.43, heterogeneity 0.17; core [0.897] rim [0.732]
  - track 3 at frame 60: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.16; core [0.921] rim [0.633]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 170 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 8.99 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.847)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1770, R_eq 7.55): none; #1 (t=1800, R_eq 7.51): none; #2 (t=1800, R_eq 7.59): none; #3 (t=1800, R_eq 7.48): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
