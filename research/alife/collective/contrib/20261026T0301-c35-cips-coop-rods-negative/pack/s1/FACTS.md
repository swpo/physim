# Evidence pack: cips-turnover (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 241 frames x 500 steps x dt 0.1 = time 12000; grid [256, 256]; wall 876s; status ok
- command: `python -m labkit.run collective/work_c35/world.py --out collective/work_c35/lkB/s1 --seeds 1 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0097, 0.9812], min area 6 px

## Measurements
- components: final 16, mean 9.8, max 16; occupancy final 0.11
- tracks: 16; persistent (alive >= 50% of run): 16; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 16
- channel total drift (end/start - 1): [0.0013, -0.5688, 0.6136]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 157: holes 0, rim-vs-core 0.30, rim-vs-outside 0.73, heterogeneity 0.11; core [0.981, 0.92, 0.031] rim [0.806, 0.738, 0.184]
  - track 1 at frame 159: holes 0, rim-vs-core 0.30, rim-vs-outside 0.72, heterogeneity 0.11; core [0.979, 0.911, 0.026] rim [0.802, 0.73, 0.183]
  - track 2 at frame 159: holes 0, rim-vs-core 0.22, rim-vs-outside 0.81, heterogeneity 0.11; core [0.98, 0.922, 0.034] rim [0.852, 0.794, 0.163]
  - track 3 at frame 163: holes 0, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.12; core [0.984, 0.947, 0.054] rim [0.809, 0.758, 0.211]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [81, 121, 159, 200, 240]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 18.2 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.716)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 10.3 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.731)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.9, rim/outside 0.657 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.515)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=7850, R_eq 13.75): none; #1 (t=7950, R_eq 13.95): none; #2 (t=7950, R_eq 12.18): none; #3 (t=8150, R_eq 11.45): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
