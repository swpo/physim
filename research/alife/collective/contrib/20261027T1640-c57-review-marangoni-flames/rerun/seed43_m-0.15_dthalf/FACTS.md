# Evidence pack: marangoni-flames (seed 43)

- world: `../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 50 steps x dt 0.04 = time 1200; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c57-w15/m15_dthalf --seeds 43 --frames 600 --spf 50 --no-movie`
- segmentation: matter > 0.37 of robust range [0.0, 0.6811], min area 6 px

## Measurements
- components: final 23, mean 17.4, max 44; occupancy final 0.03
- tracks: 129; persistent (alive >= 50% of run): 16; longest 589 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.86 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0131/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 40, default): splits 37, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.135, nucleations 17
- channel total drift (end/start - 1): [-0.8652, -0.2608, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 308: holes 0, rim-vs-core 0.55, rim-vs-outside 0.68, heterogeneity 0.14; core [0.973, 0.026, 0.534, 1.0] rim [0.679, 0.107, 0.943, 0.803]
  - track 93 at frame 313: holes 0, rim-vs-core 0.56, rim-vs-outside 0.67, heterogeneity 0.15; core [0.953, 0.018, 0.514, 0.959] rim [0.659, 0.11, 0.942, 0.78]
  - track 102 at frame 318: holes 0, rim-vs-core 0.57, rim-vs-outside 0.67, heterogeneity 0.15; core [0.939, 0.021, 0.524, 0.954] rim [0.636, 0.115, 0.953, 0.757]
  - track 115 at frame 484: holes 0, rim-vs-core 0.53, rim-vs-outside 0.68, heterogeneity 0.15; core [0.97, 0.028, 0.55, 0.995] rim [0.678, 0.107, 0.932, 0.79]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 32.1 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.814)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.3, rim/outside 0.632 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.237)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.33, rim/outside 3.31 (aggregate of 109 individuals; 109/109 membrane-like individually; rim level 0.949)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 81.6 (aggregate of 109 individuals; 1/109 membrane-like individually; rim level 0.914)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #60 (t=616, R_eq 2.39): ['|u|']; #93 (t=626, R_eq 2.71): ['|u|']; #102 (t=636, R_eq 2.76): ['|u|']; #115 (t=968, R_eq 2.46): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
