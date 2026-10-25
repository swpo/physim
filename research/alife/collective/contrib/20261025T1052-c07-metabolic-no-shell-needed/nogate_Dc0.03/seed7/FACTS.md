# Evidence pack: fch-metabolic-micelles-lowDc (seed 7)

- world: `../../world_nogate_Dc0.03.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 459s; status ok
- command: `python -m labkit.run collective/contrib/_c07f2/world_nogate_Dc0.03.py --out collective/contrib/_c07f2/nogate_Dc0.03/seed7 --seeds 7 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1078, 2.9758], min area 6 px

## Measurements
- components: final 26, mean 24.2, max 26; occupancy final 0.13
- tracks: 31; persistent (alive >= 50% of run): 24; longest 101 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 15.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 160, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 22
- channel total drift (end/start - 1): [0.0499, 1.6048, None, -0.42]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 50: holes 0, rim-vs-core 0.61, rim-vs-outside 0.27, heterogeneity 0.21; core [0.635, 0.771, 0.246, 0.092] rim [0.177, 0.393, 0.358, 0.202]
  - track 3 at frame 50: holes 0, rim-vs-core 0.61, rim-vs-outside 0.27, heterogeneity 0.20; core [0.638, 0.721, 0.265, 0.08] rim [0.171, 0.353, 0.358, 0.181]
  - track 5 at frame 51: holes 0, rim-vs-core 0.36, rim-vs-outside 0.38, heterogeneity 0.21; core [0.619, 0.626, 0.342, 0.068] rim [0.332, 0.408, 0.344, 0.128]
  - track 6 at frame 51: holes 0, rim-vs-core 0.54, rim-vs-outside 0.35, heterogeneity 0.20; core [0.667, 0.583, 0.28, 0.049] rim [0.241, 0.314, 0.447, 0.123]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 22 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.492)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.562, rim/outside 5.57 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.491)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12, rim/outside 6.46 (aggregate of 148 individuals; 148/148 membrane-like individually; rim level 0.741)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.52, rim/outside 0.844 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.262)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #1 (t=400, R_eq 5.05): ['shell q']; #3 (t=400, R_eq 5.11): ['shell q']; #5 (t=408, R_eq 5.11): ['shell q']; #6 (t=408, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
