# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm4_b0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 314s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4_b0.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4b0/seed0 --seeds 0 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0059, 2.6342], min area 6 px

## Measurements
- components: final 0, mean 10.0, max 25; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 3; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 24
- channel total drift (end/start - 1): [-0.9803, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 29: holes 0, rim-vs-core 0.50, rim-vs-outside 0.55, heterogeneity 0.15; core [0.769, 0.154, 0.583, 0.577] rim [0.32, 0.152, 0.805, 0.596]
  - track 17 at frame 29: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.14; core [0.785, 0.156, 0.523, 0.566] rim [0.342, 0.154, 0.887, 0.574]
  - track 26 at frame 29: holes 0, rim-vs-core 0.56, rim-vs-outside 0.61, heterogeneity 0.14; core [0.783, 0.158, 0.55, 0.553] rim [0.342, 0.156, 0.895, 0.562]
  - track 2 at frame 21: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.16; core [0.781, 0.279, 0.529, 0.3] rim [0.485, 0.277, 0.637, 0.312]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.598, rim/outside 16.7 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.585)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 1.03 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.226)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 7.88, rim/outside 6.89 (aggregate of 53 individuals; 53/53 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.994 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.502)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=232, R_eq 3.24): ['shell q']; #17 (t=232, R_eq 3.19): ['shell q']; #26 (t=232, R_eq 3.19): ['shell q']; #2 (t=168, R_eq 3.61): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
