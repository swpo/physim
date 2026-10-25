# Evidence pack: fch-gated-micelles-dt2 (seed 5)

- world: `../../world_dt2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 400 steps x dt 0.01 = time 400; grid [128, 128]; wall 298s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1724-c13-audit-fch-gated-micelles/world_dt2.py --out collective/contrib/20261025T1724-c13-audit-fch-gated-micelles/rerun_world_dt2/seed5 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1226, 2.988], min area 6 px

## Measurements
- components: final 54, mean 36.7, max 54; occupancy final 0.27
- tracks: 138; persistent (alive >= 50% of run): 30; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.25 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0296/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 80, default): splits 57, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 13, merge/split ratio 0.228, nucleations 3
- channel total drift (end/start - 1): [0.6579, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 55: holes 0, rim-vs-core 0.59, rim-vs-outside 0.22, heterogeneity 0.27; core [0.598, 0.513, 0.265] rim [0.15, 0.126, 0.298]
  - track 43 at frame 55: holes 0, rim-vs-core 0.67, rim-vs-outside 0.28, heterogeneity 0.29; core [0.622, 0.568, 0.291] rim [0.167, 0.087, 0.411]
  - track 46 at frame 55: holes 0, rim-vs-core 0.65, rim-vs-outside 0.25, heterogeneity 0.27; core [0.628, 0.522, 0.246] rim [0.172, 0.074, 0.369]
  - track 97 at frame 76: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.30; core [0.615, 0.454, 0.387] rim [0.158, 0.073, 0.491]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 248 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.511, rim/outside 4.76 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.483)
  - radial cargo c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.636, rim/outside 3.38 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.361)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.3, rim/outside 3.59 (aggregate of 248 individuals; 246/248 membrane-like individually; rim level 0.686)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #42 (t=220, R_eq 5.08): ['shell q']; #43 (t=220, R_eq 5.17): ['shell q']; #46 (t=220, R_eq 5.11): ['shell q']; #97 (t=304, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
