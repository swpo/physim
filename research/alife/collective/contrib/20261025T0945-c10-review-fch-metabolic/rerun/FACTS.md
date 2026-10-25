# Evidence pack: fch-metabolic-micelles (seed 23)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 621s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0945-c10-review-fch-metabolic/world_ctl.py --out collective/contrib/20261025T0945-c10-review-fch-metabolic/rerun --seeds 23 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0805, 2.992], min area 6 px

## Measurements
- components: final 60, mean 43.5, max 60; occupancy final 0.30
- tracks: 103; persistent (alive >= 50% of run): 38; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.94 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 60, 60], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 40, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 19
- channel total drift (end/start - 1): [0.8688, 3.7117, None, -0.7505]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 76: holes 0, rim-vs-core 0.76, rim-vs-outside 0.31, heterogeneity 0.25; core [0.68, 0.708, 0.184, 0.043] rim [0.259, 0.106, 0.371, 0.093]
  - track 12 at frame 68: holes 0, rim-vs-core 0.66, rim-vs-outside 0.20, heterogeneity 0.22; core [0.615, 0.561, 0.216, 0.08] rim [0.169, 0.086, 0.266, 0.142]
  - track 32 at frame 95: holes 0, rim-vs-core 0.63, rim-vs-outside 0.37, heterogeneity 0.24; core [0.679, 0.55, 0.239, 0.029] rim [0.282, 0.122, 0.463, 0.059]
  - track 93 at frame 129: holes 0, rim-vs-core 0.48, rim-vs-outside 0.29, heterogeneity 0.20; core [0.613, 0.176, 0.396, 0.106] rim [0.167, 0.005, 0.477, 0.13]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 277 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.518, rim/outside 7.47 (aggregate of 277 individuals; 0/277 membrane-like individually; rim level 0.491)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.306, rim/outside 7.89 (aggregate of 277 individuals; 0/277 membrane-like individually; rim level 0.204)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.8, rim/outside 4.34 (aggregate of 277 individuals; 277/277 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 2.6, rim/outside 0.915 (aggregate of 277 individuals; 0/277 membrane-like individually; rim level 0.178)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #22 (t=608, R_eq 5.14): ['shell q']; #12 (t=544, R_eq 5.08): ['shell q']; #32 (t=760, R_eq 5.05): ['shell q']; #93 (t=1032, R_eq 5.14): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
