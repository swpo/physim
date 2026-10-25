# Evidence pack: crawler (seed 3)

- world: `../../../../contrib/20261025T0641-c04-crawler-positive-control/world.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [256, 256]; wall 150s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0641-c04-crawler-positive-control/world.py --out collective/work_c05/rev_cs/rerun_R12/seed3 --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.53 of robust range [-0.0, 0.9491], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.03
- tracks: 1; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 1.59/time; max body lengths 17.7
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0498, -0.3888, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.35, rim-vs-outside 0.48, heterogeneity 0.11; core [0.932, 0.41, 0.0, 0.0] rim [0.731, 0.691, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 73.7 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.915)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.95, rim/outside 26.9 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.585)  MEMBRANE-LIKE
  - radial V/V0 (body content): flat profile (no radial structure; level 0; aggregate of 6 individuals)
  - radial n (nutrient): flat profile (no radial structure; level 0; aggregate of 6 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #0 (t=250, R_eq 25.43): ['|P| (actin polarization)']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
