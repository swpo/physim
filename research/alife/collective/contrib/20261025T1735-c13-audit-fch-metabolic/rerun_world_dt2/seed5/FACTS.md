# Evidence pack: fch-metabolic-micelles-dt2 (seed 5)

- world: `../../world_dt2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 800 steps x dt 0.01 = time 800; grid [128, 128]; wall 609s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1735-c13-audit-fch-metabolic/world_dt2.py --out collective/contrib/20261025T1735-c13-audit-fch-metabolic/rerun_world_dt2/seed5 --seeds 5 --spf 800 --frames 100 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0965, 2.9793], min area 6 px

## Measurements
- components: final 34, mean 24.2, max 34; occupancy final 0.18
- tracks: 78; persistent (alive >= 50% of run): 18; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.69 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 35, 35], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 31, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.161, nucleations 3
- channel total drift (end/start - 1): [0.2455, 2.3346, None, -0.5316]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 52: holes 0, rim-vs-core 0.79, rim-vs-outside 0.26, heterogeneity 0.27; core [0.633, 0.65, 0.307, 0.028] rim [0.169, 0.024, 0.398, 0.089]
  - track 20 at frame 52: holes 0, rim-vs-core 0.67, rim-vs-outside 0.26, heterogeneity 0.25; core [0.63, 0.549, 0.325, 0.036] rim [0.167, 0.07, 0.397, 0.094]
  - track 23 at frame 52: holes 0, rim-vs-core 0.73, rim-vs-outside 0.28, heterogeneity 0.26; core [0.635, 0.649, 0.301, 0.046] rim [0.176, 0.1, 0.403, 0.118]
  - track 41 at frame 69: holes 0, rim-vs-core 0.63, rim-vs-outside 0.30, heterogeneity 0.26; core [0.618, 0.567, 0.342, 0.082] rim [0.168, 0.135, 0.428, 0.155]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.527, rim/outside 5.61 (aggregate of 155 individuals; 2/155 membrane-like individually; rim level 0.495)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.477, rim/outside 6.19 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.313)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.6, rim/outside 3.77 (aggregate of 155 individuals; 151/155 membrane-like individually; rim level 0.732)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.22, rim/outside 0.89 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.231)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #19 (t=416, R_eq 5.17): ['shell q']; #20 (t=416, R_eq 5.17): ['shell q']; #23 (t=416, R_eq 5.08): ['shell q']; #41 (t=552, R_eq 5.01): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
