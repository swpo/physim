# Evidence pack: cips-turnover (seed 5)

- world: `../../../20261026T0704-c35-cips-coop-fork-lsc5/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 951 frames x 100 steps x dt 0.1 = time 9500; grid [192, 192]; wall 879s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5/world.py --out collective/contrib/20261026T0850-c38-review-cips-fork/rerun/fork_seed5 --seeds 5 --frames 950 --size 192 192 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0077, 0.9823], min area 6 px

## Measurements
- components: final 0, mean 5.4, max 11; occupancy final 0.00
- tracks: 11; persistent (alive >= 50% of run): 4; longest 541 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.0008, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 543: holes 0, rim-vs-core 0.14, rim-vs-outside 0.88, heterogeneity 0.09; core [0.951, 0.852, 0.232] rim [0.869, 0.777, 0.31]
  - track 1 at frame 559: holes 0, rim-vs-core 0.27, rim-vs-outside 0.73, heterogeneity 0.10; core [0.97, 0.89, 0.244] rim [0.812, 0.737, 0.396]
  - track 2 at frame 559: holes 0, rim-vs-core 0.28, rim-vs-outside 0.74, heterogeneity 0.10; core [0.981, 0.921, 0.253] rim [0.816, 0.748, 0.403]
  - track 3 at frame 567: holes 0, rim-vs-core 0.28, rim-vs-outside 0.73, heterogeneity 0.11; core [0.978, 0.909, 0.252] rim [0.807, 0.738, 0.401]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [319, 479, 631, 790]):
  - radial e: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 58.9 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.92)
  - radial p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 19.7 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.897)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.59, rim/outside 0.763 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.64)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5430, R_eq 14.14): none; #1 (t=5590, R_eq 12.55): none; #2 (t=5590, R_eq 11.56): none; #3 (t=5670, R_eq 12.07): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
