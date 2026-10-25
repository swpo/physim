# Evidence pack: active-gel-ac-cells (seed 4)

- world: `../../../20261025T1249-c09-ac-gel-cells-bistable/world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 101 frames x 300 steps x dt 0.01 = time 300; grid [128, 128]; wall 200s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1249-c09-ac-gel-cells-bistable/world.py --out collective/contrib/20261025T1440-c16-review-acgel/rerun_ath0.2/seed4 --seeds 4 --frames 100 --spf 300 --no-movie`
- segmentation: matter > -0.02 of robust range [0.5108, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.4, max 38; occupancy final 1.00
- tracks: 39; persistent (alive >= 50% of run): 1; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.01 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.9854, 2.6939, 2.6562, -0.8199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 0: holes 2, rim-vs-core 0.07, rim-vs-outside 0.19, heterogeneity 0.10; core [0.289, 0.015, 0.056, 1.0] rim [0.22, 0.015, 0.045, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial cell phi: flat profile (no radial structure; level 1; aggregate of 6 individuals)
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.0669)
  - radial regulator b: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.541)
  - radial substrate s: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.191)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=153, R_eq 72.22): none; #0 (t=0, R_eq 46.97, ring): none; #1 (t=0, R_eq 9.11, ring): none; #2 (t=0, R_eq 1.87): ['cell phi', 'regulator b']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
