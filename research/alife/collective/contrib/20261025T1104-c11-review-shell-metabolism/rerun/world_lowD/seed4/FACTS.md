# Evidence pack: fch-metabolic-micelles (seed 4)

- world: `../world_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 321s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11rev15/world_lowD.py --out /tmp/claude-0/c11rev15/world_lowD --seeds 4 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0937, 2.9862], min area 6 px

## Measurements
- components: final 50, mean 42.3, max 50; occupancy final 0.25
- tracks: 89; persistent (alive >= 50% of run): 44; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 50, 50], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 32, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.031, nucleations 16
- channel total drift (end/start - 1): [0.6175, 3.2136, None, -0.6727]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.62, rim-vs-outside 0.28, heterogeneity 0.21; core [0.634, 0.522, 0.227, 0.029] rim [0.188, 0.128, 0.38, 0.08]
  - track 7 at frame 51: holes 0, rim-vs-core 0.61, rim-vs-outside 0.22, heterogeneity 0.21; core [0.621, 0.531, 0.254, 0.038] rim [0.168, 0.124, 0.316, 0.095]
  - track 14 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.22, heterogeneity 0.21; core [0.613, 0.534, 0.246, 0.043] rim [0.169, 0.135, 0.312, 0.103]
  - track 83 at frame 86: holes 0, rim-vs-core 0.46, rim-vs-outside 0.30, heterogeneity 0.17; core [0.614, 0.066, 0.408, 0.195] rim [0.162, 0.022, 0.481, 0.203]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 260 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.523, rim/outside 8.11 (aggregate of 260 individuals; 1/260 membrane-like individually; rim level 0.485)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.308, rim/outside 5.39 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.226)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12, rim/outside 4.46 (aggregate of 260 individuals; 254/260 membrane-like individually; rim level 0.682)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.88, rim/outside 0.908 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.191)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=400, R_eq 4.92): ['shell q']; #7 (t=408, R_eq 5.05): ['shell q']; #14 (t=408, R_eq 5.05): ['shell q']; #83 (t=688, R_eq 5.08): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
