# Evidence pack: marangoni-flames (seed 32)

- world: `../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c53-rev-mf/pack_m100 --seeds 32 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 3.8038], min area 6 px

## Measurements
- components: final 60, mean 58.2, max 65; occupancy final 0.03
- tracks: 172; persistent (alive >= 50% of run): 60; longest 601 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 17.89 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 60, 54], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 20, default): splits 59, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.068, nucleations 30
- channel total drift (end/start - 1): [-0.8364, -0.4287, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 303: holes 0, rim-vs-core 1.28, rim-vs-outside 0.23, heterogeneity 0.34; core [0.973, 0.359, 0.8, 1.0] rim [0.157, 0.232, 0.327, 0.149]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.319, rim/outside 29.5 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.312)
  - radial fuel Y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.487, rim/outside 0.946 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.284)
  - radial |u|: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 42.4, rim/outside 9.74 (aggregate of 35 individuals; 35/35 membrane-like individually; rim level 0.652)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.306, rim/outside 30.9 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.299)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u| (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #4 (t=303, R_eq 2.03): ['|u|']; #12 (t=303, R_eq 1.69): ['|u|']; #14 (t=303, R_eq 1.69): ['|u|']; #135 (t=313, R_eq 1.69): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
