# Evidence pack: marangoni-flames (seed 5)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 41s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/20261027T1500-c58-review-marangoni-flames/pack_m0 --seeds 4 5 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7287], min area 6 px

## Measurements
- components: final 8, mean 4.6, max 42; occupancy final 0.01
- tracks: 113; persistent (alive >= 50% of run): 0; longest 222 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0365/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 20, default): splits 33, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.091, nucleations 6
- channel total drift (end/start - 1): [-0.9682, -0.0887, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 161: holes 0, rim-vs-core 0.12, rim-vs-outside 0.54, heterogeneity 0.04; core [0.779, 0.079, 0.0, 0.917] rim [0.723, 0.165, 0.0, 0.978]
  - track 100 at frame 161: holes 0, rim-vs-core 0.12, rim-vs-outside 0.49, heterogeneity 0.04; core [0.786, 0.076, 0.0, 0.921] rim [0.747, 0.157, 0.0, 0.994]
  - track 101 at frame 358: holes 0, rim-vs-core 0.10, rim-vs-outside 0.65, heterogeneity 0.06; core [0.884, 0.09, 0.0, 0.986] rim [0.8, 0.142, 0.0, 0.964]
  - track 105 at frame 519: holes 0, rim-vs-core 0.23, rim-vs-outside 0.69, heterogeneity 0.05; core [0.97, 0.098, 0.0, 1.0] rim [0.756, 0.173, 0.0, 0.98]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 20.1 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.869)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.55, rim/outside 0.663 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.277)
  - radial |u|: flat profile (no radial structure; level 0; aggregate of 28 individuals)
  - radial burn r: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 67 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.986)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=161, R_eq 3.19): none; #100 (t=161, R_eq 3.09): none; #101 (t=358, R_eq 2.71): none; #105 (t=519, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
