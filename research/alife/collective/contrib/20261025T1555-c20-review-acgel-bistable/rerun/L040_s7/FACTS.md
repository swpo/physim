# Evidence pack: active-gel-ac-cells (seed 7)

- world: `../world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 601 frames x 100 steps x dt 0.01 = time 600; grid [128, 128]; wall 354s; status ok
- command: `python -m labkit.run /tmp/c20ac/world.py --out /tmp/c20ac/L040_s7 --seeds 7 --frames 600 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 0.7, max 48; occupancy final 0.00
- tracks: 108; persistent (alive >= 50% of run): 0; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.976/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 20, default): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 1.23, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -0.9464, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 105 at frame 111: holes 0, rim-vs-core 0.20, rim-vs-outside 1.05, heterogeneity 0.18; core [1.0, 0.137, 0.706, 0.057] rim [0.931, 0.247, 0.56, 0.103]
  - track 102 at frame 25: holes 0, rim-vs-core 0.78, rim-vs-outside 0.31, heterogeneity 0.22; core [0.894, 0.594, 0.881, 0.041] rim [0.604, 0.038, 0.455, 0.21]
  - track 91 at frame 20: holes 0, rim-vs-core 0.72, rim-vs-outside 0.17, heterogeneity 0.22; core [0.835, 0.592, 0.775, 0.047] rim [0.576, 0.053, 0.391, 0.177]
  - track 107 at frame 197: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.16; core [0.982, 0.145, 0.844, 0.193] rim [0.748, 0.057, 0.715, 0.294]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [101, 202]):
  - radial cell phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.743, rim/outside 32.6 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.73)
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.337, rim/outside 4.12 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.0724)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2.02 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.713)
  - radial substrate s: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 6.94, rim/outside 0.711 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #105 (t=111, R_eq 48.92): none; #102 (t=25, R_eq 7.18): none; #91 (t=20, R_eq 5.64): none; #107 (t=197, R_eq 14.96): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 1 of 2 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
