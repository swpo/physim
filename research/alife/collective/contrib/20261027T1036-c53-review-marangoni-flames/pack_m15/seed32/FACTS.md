# Evidence pack: marangoni-flames (seed 32)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c53-rev-mf/pack_m15 --seeds 32 33 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.8017], min area 6 px

## Measurements
- components: final 17, mean 12.2, max 48; occupancy final 0.02
- tracks: 121; persistent (alive >= 50% of run): 11; longest 589 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.27 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0269/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 20, default): splits 38, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.132, nucleations 12
- channel total drift (end/start - 1): [-0.9253, -0.1962, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 74 at frame 308: holes 0, rim-vs-core 0.56, rim-vs-outside 0.71, heterogeneity 0.16; core [0.959, 0.044, 0.558, 0.992] rim [0.65, 0.134, 0.961, 0.787]
  - track 84 at frame 308: holes 0, rim-vs-core 0.57, rim-vs-outside 0.69, heterogeneity 0.16; core [0.937, 0.039, 0.542, 0.979] rim [0.632, 0.14, 0.962, 0.77]
  - track 104 at frame 323: holes 0, rim-vs-core 0.54, rim-vs-outside 0.69, heterogeneity 0.14; core [0.968, 0.029, 0.479, 0.982] rim [0.709, 0.119, 0.93, 0.855]
  - track 109 at frame 514: holes 0, rim-vs-core 0.57, rim-vs-outside 0.72, heterogeneity 0.15; core [0.974, 0.059, 0.604, 0.999] rim [0.627, 0.142, 0.979, 0.769]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 31.2 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.822)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.93, rim/outside 0.648 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.26)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.46, rim/outside 3.29 (aggregate of 77 individuals; 77/77 membrane-like individually; rim level 0.946)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 72.8 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.924)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #74 (t=308, R_eq 2.65): ['|u|']; #84 (t=308, R_eq 2.88): ['|u|']; #104 (t=323, R_eq 2.65): ['|u|']; #109 (t=514, R_eq 2.46): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
