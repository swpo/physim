# Evidence pack: fch-allee-micelles (seed 7)

- world: `../../../20261025T1050-c03-allee-no-turnover/world_wb1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 76 frames x 800 steps x dt 0.02 = time 1200; grid [128, 128]; wall 468s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1050-c03-allee-no-turnover/world_wb1.py --out collective/contrib/20261025T1240-c09-review-allee/wb1/seed7 --seeds 7 --frames 75 --spf 800 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1182, 2.9612], min area 6 px

## Measurements
- components: final 42, mean 40.5, max 42; occupancy final 0.20
- tracks: 63; persistent (alive >= 50% of run): 42; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 320, default): splits 18, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 22
- channel total drift (end/start - 1): [0.3108, -0.6194, None, -0.7706]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 38: holes 0, rim-vs-core 0.35, rim-vs-outside 0.42, heterogeneity 0.27; core [0.586, 0.504, 0.351, 0.047] rim [0.34, 0.259, 0.337, 0.088]
  - track 6 at frame 38: holes 0, rim-vs-core 0.68, rim-vs-outside 0.34, heterogeneity 0.24; core [0.646, 0.488, 0.286, 0.033] rim [0.216, 0.006, 0.481, 0.081]
  - track 7 at frame 38: holes 0, rim-vs-core 0.31, rim-vs-outside 0.42, heterogeneity 0.25; core [0.572, 0.449, 0.383, 0.048] rim [0.362, 0.228, 0.337, 0.075]
  - track 45 at frame 41: holes 0, rim-vs-core 0.65, rim-vs-outside 0.29, heterogeneity 0.24; core [0.612, 0.456, 0.331, 0.047] rim [0.163, 0.005, 0.437, 0.099]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 252 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.497, rim/outside 19.1 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.471)
  - radial catalyst c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.237, rim/outside 10 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.171)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13.9, rim/outside 6.31 (aggregate of 252 individuals; 252/252 membrane-like individually; rim level 0.765)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 5.97, rim/outside 0.865 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.142)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #5 (t=608, R_eq 4.98): ['shell q']; #6 (t=608, R_eq 4.92): ['shell q']; #7 (t=608, R_eq 4.98): ['shell q']; #45 (t=656, R_eq 4.95): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
