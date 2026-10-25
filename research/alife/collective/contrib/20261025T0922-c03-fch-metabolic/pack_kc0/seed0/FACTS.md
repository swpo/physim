# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm4_kc0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 455s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4_kc0.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4kc0/seed0 --seeds 0 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.20 of robust range [0.0008, 2.5032], min area 6 px

## Measurements
- components: final 0, mean 6.6, max 25; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 24
- channel total drift (end/start - 1): [-0.9974, -1.0, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 29: holes 0, rim-vs-core 0.55, rim-vs-outside 0.56, heterogeneity 0.15; core [0.873, 0.104, 0.629, 0.638] rim [0.395, 0.104, 0.895, 0.643]
  - track 17 at frame 29: holes 0, rim-vs-core 0.59, rim-vs-outside 0.62, heterogeneity 0.15; core [0.881, 0.104, 0.619, 0.589] rim [0.403, 0.104, 0.963, 0.643]
  - track 26 at frame 29: holes 0, rim-vs-core 0.56, rim-vs-outside 0.60, heterogeneity 0.15; core [0.876, 0.104, 0.644, 0.571] rim [0.404, 0.104, 0.953, 0.589]
  - track 2 at frame 21: holes 0, rim-vs-core 0.33, rim-vs-outside 0.56, heterogeneity 0.16; core [0.855, 0.197, 0.576, 0.352] rim [0.563, 0.197, 0.728, 0.354]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [25, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 17.7 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.706)
  - radial catalyst c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.13)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 6.25, rim/outside 5.15 (aggregate of 28 individuals; 28/28 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.986 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.568)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=232, R_eq 3.19): ['shell q']; #17 (t=232, R_eq 3.19): ['shell q']; #26 (t=232, R_eq 3.19): ['shell q']; #2 (t=168, R_eq 3.57): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
