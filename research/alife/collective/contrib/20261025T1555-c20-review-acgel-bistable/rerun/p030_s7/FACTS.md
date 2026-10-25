# Evidence pack: active-gel-ac-cells (seed 7)

- world: `../world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 119s; status ok
- command: `python -m labkit.run /tmp/c20ac/world.py --out /tmp/c20ac/p030_s7 --seeds 7 --no-movie`
- segmentation: matter > 0.20 of robust range [0.3747, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.3, max 48; occupancy final 1.00
- tracks: 53; persistent (alive >= 50% of run): 1; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.40 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 20, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 1.5, nucleations 0
- channel total drift (end/start - 1): [1.0071, 3.0091, 2.7614, -0.8339]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 0: holes 0, rim-vs-core 0.13, rim-vs-outside 0.24, heterogeneity 0.11; core [0.25, 0.014, 0.022, 1.0] rim [0.38, 0.011, 0.027, 1.0]
  - track 38 at frame 0: holes 0, rim-vs-core 0.27, rim-vs-outside 0.20, heterogeneity 0.11; core [0.58, 0.011, 0.021, 1.0] rim [0.31, 0.017, 0.067, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial cell phi: flat profile (no radial structure; level 1; aggregate of 6 individuals)
  - radial generator a: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 2.09, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.14)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.532)
  - radial substrate s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.176)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=101, R_eq 72.22): none; #8 (t=0, R_eq 2.82): ['cell phi', 'regulator b']; #38 (t=0, R_eq 4.03, ring): ['cell phi']; #0 (t=0, R_eq 43.85, ring): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
