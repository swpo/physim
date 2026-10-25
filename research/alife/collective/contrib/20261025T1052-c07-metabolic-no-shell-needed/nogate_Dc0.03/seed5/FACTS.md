# Evidence pack: fch-metabolic-micelles-lowDc (seed 5)

- world: `../../world_nogate_Dc0.03.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 437s; status ok
- command: `python -m labkit.run collective/contrib/_c07f2/world_nogate_Dc0.03.py --out collective/contrib/_c07f2/nogate_Dc0.03/seed5 --seeds 5 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1062, 2.9734], min area 6 px

## Measurements
- components: final 25, mean 24.7, max 25; occupancy final 0.13
- tracks: 30; persistent (alive >= 50% of run): 25; longest 101 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 14.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.0446, 1.6961, None, -0.4298]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 50: holes 0, rim-vs-core 0.59, rim-vs-outside 0.27, heterogeneity 0.21; core [0.625, 0.681, 0.292, 0.09] rim [0.17, 0.335, 0.38, 0.18]
  - track 3 at frame 50: holes 0, rim-vs-core 0.56, rim-vs-outside 0.25, heterogeneity 0.21; core [0.618, 0.602, 0.324, 0.072] rim [0.162, 0.299, 0.376, 0.149]
  - track 4 at frame 51: holes 0, rim-vs-core 0.31, rim-vs-outside 0.45, heterogeneity 0.21; core [0.607, 0.736, 0.287, 0.097] rim [0.369, 0.549, 0.306, 0.154]
  - track 5 at frame 51: holes 0, rim-vs-core 0.56, rim-vs-outside 0.27, heterogeneity 0.21; core [0.619, 0.599, 0.323, 0.075] rim [0.165, 0.294, 0.396, 0.151]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 22.6 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.494)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.559, rim/outside 5.71 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.507)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.2, rim/outside 6.52 (aggregate of 150 individuals; 150/150 membrane-like individually; rim level 0.741)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.23, rim/outside 0.845 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.263)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #1 (t=400, R_eq 5.01): ['shell q']; #3 (t=400, R_eq 5.05): ['shell q']; #4 (t=408, R_eq 5.01): ['shell q']; #5 (t=408, R_eq 5.05): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
