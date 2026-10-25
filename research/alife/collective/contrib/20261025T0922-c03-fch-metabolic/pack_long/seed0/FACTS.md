# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm4.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 936s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4long/seed0 --seeds 0 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0784, 2.9982], min area 6 px

## Measurements
- components: final 65, mean 54.8, max 65; occupancy final 0.33
- tracks: 109; persistent (alive >= 50% of run): 60; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 65, 65], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 320, default): splits 40, persistent splits 40 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.9856, 4.0136, None, -0.8002]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 76: holes 0, rim-vs-core 0.70, rim-vs-outside 0.26, heterogeneity 0.26; core [0.616, 0.525, 0.304, 0.045] rim [0.173, 0.001, 0.407, 0.094]
  - track 17 at frame 76: holes 0, rim-vs-core 0.59, rim-vs-outside 0.27, heterogeneity 0.22; core [0.615, 0.401, 0.314, 0.057] rim [0.174, 0.026, 0.422, 0.093]
  - track 29 at frame 86: holes 0, rim-vs-core 0.61, rim-vs-outside 0.30, heterogeneity 0.24; core [0.623, 0.391, 0.324, 0.03] rim [0.178, 0.002, 0.471, 0.063]
  - track 87 at frame 98: holes 0, rim-vs-core 0.60, rim-vs-outside 0.32, heterogeneity 0.24; core [0.624, 0.365, 0.344, 0.033] rim [0.177, 0.0, 0.491, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 354 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.519, rim/outside 8.76 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.492)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.166, rim/outside 7.41 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.118)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13.7, rim/outside 4.89 (aggregate of 354 individuals; 354/354 membrane-like individually; rim level 0.746)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 3.3, rim/outside 0.934 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.126)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #12 (t=1216, R_eq 5.11): ['shell q']; #17 (t=1216, R_eq 5.08): ['shell q']; #29 (t=1376, R_eq 5.14): ['shell q']; #87 (t=1568, R_eq 5.14): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
