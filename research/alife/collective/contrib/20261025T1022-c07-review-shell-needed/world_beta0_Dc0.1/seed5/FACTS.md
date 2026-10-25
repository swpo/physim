# Evidence pack: fch-metabolic-micelles-lowDc (seed 5)

- world: `../../world_beta0_Dc0.1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 447s; status ok
- command: `python -m labkit.run collective/contrib/_c07rev18/world_beta0_Dc0.1.py --out collective/contrib/_c07rev18/world_beta0_Dc0.1/seed5 --seeds 5 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0067, 2.6631], min area 6 px

## Measurements
- components: final 0, mean 10.8, max 25; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 5; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.978, -0.999, None, -0.0001]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 29: holes 0, rim-vs-core 0.66, rim-vs-outside 0.64, heterogeneity 0.16; core [0.802, 0.325, 0.451, 0.428] rim [0.364, 0.284, 0.939, 0.448]
  - track 9 at frame 29: holes 0, rim-vs-core 0.55, rim-vs-outside 0.57, heterogeneity 0.16; core [0.768, 0.312, 0.513, 0.445] rim [0.32, 0.271, 0.83, 0.464]
  - track 11 at frame 29: holes 0, rim-vs-core 0.66, rim-vs-outside 0.64, heterogeneity 0.16; core [0.803, 0.334, 0.451, 0.435] rim [0.364, 0.291, 0.942, 0.453]
  - track 16 at frame 29: holes 0, rim-vs-core 0.67, rim-vs-outside 0.65, heterogeneity 0.16; core [0.804, 0.306, 0.44, 0.449] rim [0.363, 0.267, 0.946, 0.467]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.593, rim/outside 16.8 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.586)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.672, rim/outside 1.59 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.393)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 9.76, rim/outside 7.23 (aggregate of 55 individuals; 55/55 membrane-like individually; rim level 0.998)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.938 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=232, R_eq 3.19): ['shell q']; #9 (t=232, R_eq 3.34): ['shell q']; #11 (t=232, R_eq 3.19): ['shell q']; #16 (t=232, R_eq 3.19): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
