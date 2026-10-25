# Evidence pack: fch-gated-micelles (seed 3)

- world: `../world_shell_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c01-review-fch-gated/world_shell_lowD.py --out collective/contrib/20261025T0828-c01-review-fch-gated/shell_lowD --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1153, 2.9878], min area 6 px

## Measurements
- components: final 52, mean 38.8, max 52; occupancy final 0.26
- tracks: 88; persistent (alive >= 50% of run): 38; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 80, default): splits 32, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.031, nucleations 20
- channel total drift (end/start - 1): [0.6636, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.58, rim-vs-outside 0.13, heterogeneity 0.23; core [0.613, 0.333, 0.634] rim [0.165, 0.039, 0.419]
  - track 6 at frame 51: holes 0, rim-vs-core 0.18, rim-vs-outside 0.41, heterogeneity 0.23; core [0.544, 0.251, 0.612] rim [0.38, 0.219, 0.539]
  - track 7 at frame 51: holes 0, rim-vs-core 0.58, rim-vs-outside 0.12, heterogeneity 0.23; core [0.612, 0.337, 0.645] rim [0.159, 0.04, 0.429]
  - track 44 at frame 69: holes 0, rim-vs-core 0.47, rim-vs-outside 0.24, heterogeneity 0.21; core [0.659, 0.3, 0.739] rim [0.265, 0.117, 0.574]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 10.1 (aggregate of 247 individuals; 1/247 membrane-like individually; rim level 0.487)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.308, rim/outside 3.55 (aggregate of 247 individuals; 2/247 membrane-like individually; rim level 0.169)
  - radial shell q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.732, rim/outside 1.91 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.605)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=200, R_eq 4.95): none; #6 (t=204, R_eq 5.01): none; #7 (t=204, R_eq 4.98): none; #44 (t=276, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
