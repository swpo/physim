# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm4_q0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 315s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4_q0.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4q0/seed0 --seeds 0 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.006, 2.636], min area 6 px

## Measurements
- components: final 0, mean 10.1, max 25; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 3; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 24
- channel total drift (end/start - 1): [-0.9801, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 29: holes 0, rim-vs-core 0.45, rim-vs-outside 0.19, heterogeneity 0.08; core [0.77, 0.174, 0.989, 0.562] rim [0.322, 0.167, 0.945, 0.577]
  - track 17 at frame 29: holes 0, rim-vs-core 0.44, rim-vs-outside 0.21, heterogeneity 0.07; core [0.787, 0.18, 1.0, 0.549] rim [0.343, 0.173, 0.993, 0.558]
  - track 26 at frame 29: holes 0, rim-vs-core 0.44, rim-vs-outside 0.21, heterogeneity 0.07; core [0.785, 0.189, 1.0, 0.529] rim [0.344, 0.181, 1.0, 0.54]
  - track 2 at frame 22: holes 0, rim-vs-core 0.30, rim-vs-outside 0.36, heterogeneity 0.08; core [0.789, 0.291, 0.984, 0.317] rim [0.496, 0.283, 0.954, 0.333]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.598, rim/outside 16.8 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.585)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 1.08 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.248)
  - radial shell q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 1.15 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.923)
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.51, rim/outside 0.992 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.49)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=232, R_eq 3.24): none; #17 (t=232, R_eq 3.19): none; #26 (t=232, R_eq 3.19): none; #2 (t=176, R_eq 3.52): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
