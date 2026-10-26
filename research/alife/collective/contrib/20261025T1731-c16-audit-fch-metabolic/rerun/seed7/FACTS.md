# Evidence pack: fch-metabolic-micelles (seed 7)

- world: `../../../20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 638s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out collective/contrib/20261025T1731-c16-audit-fch-metabolic/rerun/seed7 --seeds 7 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.08, 2.9934], min area 6 px

## Measurements
- components: final 61, mean 44.6, max 61; occupancy final 0.31
- tracks: 102; persistent (alive >= 50% of run): 45; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 61, 61], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 36, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.028, nucleations 22
- channel total drift (end/start - 1): [0.8967, 3.7434, None, -0.7649]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 76: holes 0, rim-vs-core 0.77, rim-vs-outside 0.22, heterogeneity 0.25; core [0.618, 0.629, 0.238, 0.031] rim [0.175, 0.004, 0.317, 0.084]
  - track 25 at frame 76: holes 0, rim-vs-core 0.65, rim-vs-outside 0.32, heterogeneity 0.24; core [0.664, 0.612, 0.216, 0.042] rim [0.25, 0.134, 0.359, 0.083]
  - track 27 at frame 95: holes 0, rim-vs-core 0.65, rim-vs-outside 0.32, heterogeneity 0.24; core [0.659, 0.502, 0.257, 0.034] rim [0.224, 0.056, 0.445, 0.072]
  - track 86 at frame 121: holes 0, rim-vs-core 0.60, rim-vs-outside 0.30, heterogeneity 0.23; core [0.624, 0.383, 0.344, 0.077] rim [0.174, 0.008, 0.462, 0.124]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 288 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 8.23 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.487)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.31, rim/outside 8.95 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.201)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13, rim/outside 4.58 (aggregate of 288 individuals; 288/288 membrane-like individually; rim level 0.696)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 2.33, rim/outside 0.922 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.183)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #22 (t=608, R_eq 5.01): ['shell q']; #25 (t=608, R_eq 4.98): ['shell q']; #27 (t=760, R_eq 5.14): ['shell q']; #86 (t=968, R_eq 5.14): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
