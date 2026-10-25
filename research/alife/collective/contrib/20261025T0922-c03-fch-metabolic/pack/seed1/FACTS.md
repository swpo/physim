# Evidence pack: fch-metabolic-micelles (seed 1)

- world: `../../wm4.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 469s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4fed/seed1 --seeds 1 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0804, 2.992], min area 6 px

## Measurements
- components: final 60, mean 44.1, max 60; occupancy final 0.30
- tracks: 103; persistent (alive >= 50% of run): 42; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 60, 60], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 42, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [0.8797, 3.7167, None, -0.7565]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 76: holes 0, rim-vs-core 0.77, rim-vs-outside 0.23, heterogeneity 0.24; core [0.624, 0.618, 0.233, 0.033] rim [0.177, 0.006, 0.327, 0.085]
  - track 14 at frame 76: holes 0, rim-vs-core 0.79, rim-vs-outside 0.23, heterogeneity 0.25; core [0.631, 0.644, 0.238, 0.033] rim [0.179, 0.003, 0.341, 0.09]
  - track 16 at frame 76: holes 0, rim-vs-core 0.76, rim-vs-outside 0.24, heterogeneity 0.25; core [0.634, 0.656, 0.218, 0.058] rim [0.184, 0.061, 0.335, 0.13]
  - track 61 at frame 105: holes 0, rim-vs-core 0.37, rim-vs-outside 0.37, heterogeneity 0.23; core [0.628, 0.36, 0.346, 0.036] rim [0.332, 0.149, 0.393, 0.056]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 282 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 7.68 (aggregate of 282 individuals; 0/282 membrane-like individually; rim level 0.488)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.301, rim/outside 8.43 (aggregate of 282 individuals; 0/282 membrane-like individually; rim level 0.201)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13, rim/outside 4.43 (aggregate of 282 individuals; 282/282 membrane-like individually; rim level 0.701)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 2.54, rim/outside 0.916 (aggregate of 282 individuals; 0/282 membrane-like individually; rim level 0.177)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #5 (t=608, R_eq 5.14): ['shell q']; #14 (t=608, R_eq 5.11): ['shell q']; #16 (t=608, R_eq 5.08): ['shell q']; #61 (t=840, R_eq 5.17): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
