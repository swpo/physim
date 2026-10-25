# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm4.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 456s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4fed/seed0 --seeds 0 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0784, 2.9939], min area 6 px

## Measurements
- components: final 62, mean 45.8, max 62; occupancy final 0.31
- tracks: 103; persistent (alive >= 50% of run): 44; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 62, 62], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 37, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.8746, 3.7779, None, -0.7626]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 76: holes 0, rim-vs-core 0.80, rim-vs-outside 0.22, heterogeneity 0.25; core [0.625, 0.65, 0.231, 0.035] rim [0.176, 0.001, 0.315, 0.095]
  - track 17 at frame 76: holes 0, rim-vs-core 0.75, rim-vs-outside 0.23, heterogeneity 0.24; core [0.627, 0.599, 0.243, 0.028] rim [0.178, 0.003, 0.335, 0.076]
  - track 29 at frame 95: holes 0, rim-vs-core 0.66, rim-vs-outside 0.29, heterogeneity 0.23; core [0.63, 0.498, 0.274, 0.045] rim [0.185, 0.038, 0.425, 0.091]
  - track 87 at frame 121: holes 0, rim-vs-core 0.50, rim-vs-outside 0.32, heterogeneity 0.19; core [0.618, 0.191, 0.351, 0.117] rim [0.175, 0.005, 0.491, 0.143]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 296 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 8.6 (aggregate of 296 individuals; 0/296 membrane-like individually; rim level 0.488)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.311, rim/outside 8.92 (aggregate of 296 individuals; 0/296 membrane-like individually; rim level 0.202)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13, rim/outside 4.71 (aggregate of 296 individuals; 296/296 membrane-like individually; rim level 0.691)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 2.26, rim/outside 0.925 (aggregate of 296 individuals; 0/296 membrane-like individually; rim level 0.188)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #12 (t=608, R_eq 5.14): ['shell q']; #17 (t=608, R_eq 5.11): ['shell q']; #29 (t=760, R_eq 5.05): ['shell q']; #87 (t=968, R_eq 5.08): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
