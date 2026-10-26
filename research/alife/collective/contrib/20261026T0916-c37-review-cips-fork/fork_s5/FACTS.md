# Evidence pack: cips-turnover (seed 5)

- world: `../../../20261026T0704-c35-cips-coop-fork-lsc5/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 91 frames x 1000 steps x dt 0.1 = time 9000; grid [192, 192]; wall 913s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5/world.py --out collective/contrib/wip-c37/cips/fork_s5 --seeds 5 --size 192 192 --spf 1000 --frames 90 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0077, 0.9826], min area 6 px

## Measurements
- components: final 0, mean 5.6, max 11; occupancy final 0.00
- tracks: 11; persistent (alive >= 50% of run): 5; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.0008, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 54: holes 0, rim-vs-core 0.14, rim-vs-outside 0.88, heterogeneity 0.09; core [0.95, 0.85, 0.232] rim [0.867, 0.775, 0.31]
  - track 1 at frame 56: holes 0, rim-vs-core 0.27, rim-vs-outside 0.72, heterogeneity 0.10; core [0.97, 0.889, 0.244] rim [0.813, 0.736, 0.396]
  - track 2 at frame 56: holes 0, rim-vs-core 0.28, rim-vs-outside 0.74, heterogeneity 0.10; core [0.981, 0.92, 0.252] rim [0.816, 0.747, 0.403]
  - track 3 at frame 57: holes 0, rim-vs-core 0.28, rim-vs-outside 0.73, heterogeneity 0.10; core [0.978, 0.909, 0.251] rim [0.812, 0.74, 0.399]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [30, 45, 60, 75]):
  - radial e: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 66.2 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.932)
  - radial p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 21.5 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.903)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.66, rim/outside 0.763 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.642)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5400, R_eq 14.16): none; #1 (t=5600, R_eq 12.54): none; #2 (t=5600, R_eq 11.56): none; #3 (t=5700, R_eq 12.03): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
