# Evidence pack: active-gel-ac-cells (seed 8)

- world: `../world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 601 frames x 100 steps x dt 0.01 = time 600; grid [128, 128]; wall 346s; status ok
- command: `python -m labkit.run /tmp/c20ac/world.py --out /tmp/c20ac/L040_s8 --seeds 8 --frames 600 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 0.7, max 37; occupancy final 0.00
- tracks: 95; persistent (alive >= 50% of run): 0; longest 223 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.817/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 20, default): splits 19, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 15, merge/split ratio 0.789, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -0.9194, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 94 at frame 151: holes 0, rim-vs-core 0.06, rim-vs-outside 1.05, heterogeneity 0.15; core [1.0, 0.152, 0.658, 0.07] rim [0.98, 0.185, 0.621, 0.093]
  - track 92 at frame 25: holes 0, rim-vs-core 0.66, rim-vs-outside 0.42, heterogeneity 0.23; core [0.963, 0.486, 0.672, 0.067] rim [0.701, 0.032, 0.315, 0.251]
  - track 93 at frame 25: holes 0, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.21; core [0.992, 0.359, 0.539, 0.053] rim [0.766, 0.028, 0.341, 0.233]
  - track 90 at frame 20: holes 0, rim-vs-core 0.73, rim-vs-outside 0.29, heterogeneity 0.22; core [0.888, 0.567, 0.764, 0.045] rim [0.622, 0.047, 0.353, 0.194]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [101, 202]):
  - radial cell phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 97.3 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.974)
  - radial generator a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.29, rim/outside 11.3 (aggregate of 2 individuals; 1/2 membrane-like individually; rim level 0.176)  MEMBRANE-LIKE
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 3.32 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.684)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.88, rim/outside 0.679 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): generator a
- membrane-like channels per top track at mid-life: #94 (t=151, R_eq 67.27): none; #92 (t=25, R_eq 10.17): none; #93 (t=25, R_eq 17.54): none; #90 (t=20, R_eq 6.68): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 1 of 2 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
