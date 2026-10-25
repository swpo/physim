# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm_F0.004.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 928s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm_F0.004.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/mF0.004/seed0 --seeds 0 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0777, 2.8624], min area 6 px

## Measurements
- components: final 25, mean 24.9, max 25; occupancy final 0.09
- tracks: 29; persistent (alive >= 50% of run): 25; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 11.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 320, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 24
- channel total drift (end/start - 1): [-0.2894, 0.7913, None, -0.7147]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 76: holes 0, rim-vs-core 0.29, rim-vs-outside 0.47, heterogeneity 0.27; core [0.587, 0.448, 0.502, 0.034] rim [0.389, 0.243, 0.429, 0.052]
  - track 5 at frame 76: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.27; core [0.634, 0.477, 0.47, 0.027] rim [0.347, 0.204, 0.435, 0.055]
  - track 6 at frame 76: holes 0, rim-vs-core 0.61, rim-vs-outside 0.40, heterogeneity 0.26; core [0.674, 0.517, 0.404, 0.024] rim [0.272, 0.079, 0.521, 0.054]
  - track 7 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.33, heterogeneity 0.27; core [0.644, 0.512, 0.436, 0.027] rim [0.186, 0.0, 0.492, 0.068]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.481, rim/outside 24.6 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.466)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.147, rim/outside 12.6 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.118)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 14.7, rim/outside 8.07 (aggregate of 150 individuals; 150/150 membrane-like individually; rim level 0.923)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.09, rim/outside 0.787 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.0952)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=1216, R_eq 4.41): ['shell q']; #5 (t=1216, R_eq 4.41): ['shell q']; #6 (t=1216, R_eq 4.41): ['shell q']; #7 (t=1216, R_eq 4.41): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
