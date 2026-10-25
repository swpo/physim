# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 309s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm_lowD.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m_lowD/seed0 --seeds 0 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1083, 2.9915], min area 6 px

## Measurements
- components: final 47, mean 40.5, max 47; occupancy final 0.24
- tracks: 73; persistent (alive >= 50% of run): 40; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 47, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 22, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.5691, 3.0307, None, -0.6432]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 51: holes 0, rim-vs-core 0.56, rim-vs-outside 0.31, heterogeneity 0.20; core [0.653, 0.562, 0.228, 0.03] rim [0.222, 0.238, 0.373, 0.076]
  - track 10 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.22, heterogeneity 0.21; core [0.608, 0.59, 0.259, 0.033] rim [0.155, 0.201, 0.311, 0.091]
  - track 11 at frame 51: holes 0, rim-vs-core 0.58, rim-vs-outside 0.24, heterogeneity 0.21; core [0.616, 0.535, 0.26, 0.033] rim [0.162, 0.188, 0.342, 0.086]
  - track 63 at frame 77: holes 0, rim-vs-core 0.53, rim-vs-outside 0.26, heterogeneity 0.21; core [0.611, 0.368, 0.366, 0.093] rim [0.156, 0.105, 0.421, 0.145]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 252 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.529, rim/outside 10.3 (aggregate of 252 individuals; 9/252 membrane-like individually; rim level 0.485)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.421, rim/outside 5.56 (aggregate of 252 individuals; 6/252 membrane-like individually; rim level 0.317)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.6, rim/outside 4.87 (aggregate of 252 individuals; 242/252 membrane-like individually; rim level 0.682)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.06, rim/outside 0.891 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.181)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #6 (t=408, R_eq 5.17): ['shell q']; #10 (t=408, R_eq 5.26): ['shell q']; #11 (t=408, R_eq 5.2): ['shell q']; #63 (t=616, R_eq 5.2): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
