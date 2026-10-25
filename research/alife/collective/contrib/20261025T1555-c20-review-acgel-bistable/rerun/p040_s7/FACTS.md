# Evidence pack: active-gel-ac-cells (seed 7)

- world: `../world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 118s; status ok
- command: `python -m labkit.run /tmp/c20ac/world.py --out /tmp/c20ac/p040_s7 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.1, max 48; occupancy final 0.03
- tracks: 108; persistent (alive >= 50% of run): 1; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.17 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.976/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 20, default): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 1.23, nucleations 0
- channel total drift (end/start - 1): [-0.9279, -0.625, 1.8815, -0.2566]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 105 at frame 109: holes 0, rim-vs-core 0.19, rim-vs-outside 1.03, heterogeneity 0.17; core [1.0, 0.088, 0.609, 0.06] rim [0.928, 0.17, 0.457, 0.108]
  - track 102 at frame 24: holes 0, rim-vs-core 0.66, rim-vs-outside 0.30, heterogeneity 0.20; core [0.902, 0.351, 0.778, 0.052] rim [0.624, 0.02, 0.314, 0.224]
  - track 91 at frame 17: holes 0, rim-vs-core 0.69, rim-vs-outside 0.26, heterogeneity 0.21; core [0.887, 0.47, 0.591, 0.04] rim [0.608, 0.016, 0.175, 0.195]
  - track 103 at frame 22: holes 0, rim-vs-core 0.64, rim-vs-outside 0.44, heterogeneity 0.22; core [0.973, 0.327, 0.648, 0.059] rim [0.701, 0.02, 0.197, 0.24]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 7 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial cell phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.745, rim/outside 12.2 (aggregate of 7 individuals; 0/7 membrane-like individually; rim level 0.721)
  - radial generator a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 5.77 (aggregate of 7 individuals; 2/7 membrane-like individually; rim level 0.111)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 2.58 (aggregate of 7 individuals; 0/7 membrane-like individually; rim level 0.626)
  - radial substrate s: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 4.49, rim/outside 0.758 (aggregate of 7 individuals; 0/7 membrane-like individually; rim level 0.537)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #105 (t=109, R_eq 47.4): none; #102 (t=24, R_eq 7.48): none; #91 (t=17, R_eq 6.72): none; #103 (t=22, R_eq 10.76): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 3 of 7 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
