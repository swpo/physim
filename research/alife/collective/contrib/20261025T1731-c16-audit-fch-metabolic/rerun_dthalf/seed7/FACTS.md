# Evidence pack: fch-metabolic-micelles (seed 7)

- world: `../../../20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 1266s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out collective/contrib/20261025T1731-c16-audit-fch-metabolic/rerun_dthalf/seed7 --seeds 7 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.14 of robust range [0.08, 2.9961], min area 6 px

## Measurements
- components: final 65, mean 54.3, max 65; occupancy final 0.33
- tracks: 110; persistent (alive >= 50% of run): 57; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 65, 65], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 320, default): splits 40, persistent splits 39 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.025, nucleations 22
- channel total drift (end/start - 1): [1.0058, 3.9509, None, -0.7984]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 76: holes 0, rim-vs-core 0.64, rim-vs-outside 0.28, heterogeneity 0.24; core [0.622, 0.438, 0.3, 0.054] rim [0.176, 0.004, 0.431, 0.097]
  - track 25 at frame 76: holes 0, rim-vs-core 0.70, rim-vs-outside 0.34, heterogeneity 0.24; core [0.651, 0.489, 0.269, 0.034] rim [0.202, 0.003, 0.492, 0.072]
  - track 27 at frame 86: holes 0, rim-vs-core 0.60, rim-vs-outside 0.35, heterogeneity 0.24; core [0.656, 0.483, 0.284, 0.034] rim [0.262, 0.072, 0.468, 0.065]
  - track 104 at frame 120: holes 0, rim-vs-core 0.59, rim-vs-outside 0.32, heterogeneity 0.24; core [0.618, 0.366, 0.368, 0.039] rim [0.174, 0.001, 0.5, 0.073]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 349 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 8.14 (aggregate of 349 individuals; 0/349 membrane-like individually; rim level 0.49)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.182, rim/outside 7.87 (aggregate of 349 individuals; 0/349 membrane-like individually; rim level 0.129)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13.7, rim/outside 4.66 (aggregate of 349 individuals; 349/349 membrane-like individually; rim level 0.753)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 3.49, rim/outside 0.933 (aggregate of 349 individuals; 0/349 membrane-like individually; rim level 0.123)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #22 (t=1216, R_eq 5.11): ['shell q']; #25 (t=1216, R_eq 5.11): ['shell q']; #27 (t=1376, R_eq 5.2): ['shell q']; #104 (t=1920, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
