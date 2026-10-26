# Evidence pack: cips-predator-prey (seed 5)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [128, 128]; wall 272s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1815-c43-review-cips-predator/world.py --out collective/contrib/20261026T1815-c43-review-cips-predator/rerun_preyonly/seed5 --seeds 5 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0262, 0.9678], min area 6 px

## Measurements
- components: final 7, mean 4.5, max 7; occupancy final 0.04
- tracks: 10; persistent (alive >= 50% of run): 4; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00191/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.0, -0.689, 0.7431, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 42: holes 0, rim-vs-core 0.40, rim-vs-outside 0.46, heterogeneity 0.07; core [0.971, 0.945, 0.036, 0.0, 0.0] rim [0.713, 0.69, 0.213, 0.0, 0.0]
  - track 0 at frame 37: holes 0, rim-vs-core 0.28, rim-vs-outside 0.73, heterogeneity 0.07; core [0.985, 0.959, 0.009, 0.0, 0.0] rim [0.811, 0.769, 0.129, 0.0, 0.0]
  - track 2 at frame 32: holes 0, rim-vs-core 0.31, rim-vs-outside 0.73, heterogeneity 0.07; core [0.985, 0.954, 0.002, 0.0, 0.0] rim [0.801, 0.747, 0.13, 0.0, 0.0]
  - track 4 at frame 66: holes 0, rim-vs-core 0.21, rim-vs-outside 0.62, heterogeneity 0.07; core [0.973, 0.941, 0.032, 0.0, 0.0] rim [0.84, 0.809, 0.124, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial e prey: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 18.5 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.779)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 10 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.791)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.8, rim/outside 0.62 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.46)
  - radial q predator: flat profile (no radial structure; level 0; aggregate of 30 individuals)
  - radial r: flat profile (no radial structure; level 0; aggregate of 30 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=4200, R_eq 5.35): none; #0 (t=3700, R_eq 6.28): none; #2 (t=3200, R_eq 6.41): none; #4 (t=6600, R_eq 5.47): none
- species `prey` (channels ['e prey'], own threshold): components final 7, mean 4.5, max 7; tracks 10, persistent 4; splits 3, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 2
- species `predator` (channels ['q predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
