# Evidence pack: ambplus-ab (seed 7)

- world: `../../../../contrib/20261025T0811-c08-ambplus-reaction-morphology/world.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 101 frames x 1000 steps x dt 0.03 = time 3000; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0811-c08-ambplus-reaction-morphology/world.py --out collective/work_c05/rev_amb/rerun/seed7 --seeds 7 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.46 of robust range [-0.9129, 1.0914], min area 6 px

## Measurements
- components: final 38, mean 30.6, max 39; occupancy final 0.32
- tracks: 40; persistent (alive >= 50% of run): 39; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 27.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 600, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 39
- channel total drift (end/start - 1): [0.3881]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 59: holes 0, rim-vs-core 0.30, rim-vs-outside 0.33, heterogeneity 0.17; core [0.917] rim [0.622]
  - track 1 at frame 60: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.17; core [0.918] rim [0.628]
  - track 2 at frame 60: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.17; core [0.912] rim [0.619]
  - track 3 at frame 60: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.16; core [0.916] rim [0.632]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 194 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 9.15 (aggregate of 194 individuals; 0/194 membrane-like individually; rim level 0.843)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1770, R_eq 7.07): none; #1 (t=1800, R_eq 7.11): none; #2 (t=1800, R_eq 7.14): none; #3 (t=1800, R_eq 6.93): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
