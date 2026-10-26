# Evidence pack: cips-predator-prey (seed 3)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 61 frames x 1000 steps x dt 0.1 = time 6000; grid [128, 128]; wall 218s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/preyonly_seed3 --seeds 3 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0269, 0.9676], min area 6 px

## Measurements
- components: final 7, mean 4.3, max 7; occupancy final 0.04
- tracks: 10; persistent (alive >= 50% of run): 4; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.46 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 2000, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [-0.0, -0.6878, 0.7417, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 33: holes 0, rim-vs-core 0.21, rim-vs-outside 0.80, heterogeneity 0.07; core [0.986, 0.957, 0.003, 0.0, 0.0] rim [0.864, 0.821, 0.099, 0.0, 0.0]
  - track 2 at frame 31: holes 0, rim-vs-core 0.29, rim-vs-outside 0.74, heterogeneity 0.07; core [0.988, 0.962, 0.005, 0.0, 0.0] rim [0.812, 0.768, 0.124, 0.0, 0.0]
  - track 3 at frame 26: holes 0, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.07; core [0.989, 0.969, 0.009, 0.0, 0.0] rim [0.809, 0.775, 0.14, 0.0, 0.0]
  - track 4 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.46, heterogeneity 0.07; core [0.977, 0.95, 0.031, 0.0, 0.0] rim [0.727, 0.694, 0.208, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial e prey: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 15 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.768)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 8.99 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.783)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.6, rim/outside 0.628 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.471)
  - radial q predator: flat profile (no radial structure; level 0; aggregate of 30 individuals)
  - radial r: flat profile (no radial structure; level 0; aggregate of 30 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3300, R_eq 6.31): none; #2 (t=3100, R_eq 6.48): none; #3 (t=2600, R_eq 6.21): none; #4 (t=5000, R_eq 5.5): none
- species `prey` (channels ['e prey'], own threshold): components final 7, mean 4.3, max 7; tracks 10, persistent 4; splits 3, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['q predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
