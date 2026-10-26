# Evidence pack: cips-turnover-divide (seed 4)

- world: `../../../20261026T1025-c40-cips-turnover-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1074s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1025-c40-cips-turnover-divide-claim/world.py --out collective/contrib/c39-rev-cipsdiv-wip/rerun/seed4 --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0217, 0.9751], min area 6 px

## Measurements
- components: final 17, mean 10.8, max 17; occupancy final 0.09
- tracks: 31; persistent (alive >= 50% of run): 6; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00307/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.0, -0.5881, 0.6351]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 118: holes 0, rim-vs-core 0.37, rim-vs-outside 0.63, heterogeneity 0.13; core [0.989, 0.954, 0.058] rim [0.779, 0.707, 0.243]
  - track 11 at frame 134: holes 0, rim-vs-core 0.29, rim-vs-outside 0.69, heterogeneity 0.12; core [0.986, 0.95, 0.037] rim [0.832, 0.758, 0.189]
  - track 14 at frame 138: holes 0, rim-vs-core 0.34, rim-vs-outside 0.59, heterogeneity 0.12; core [0.975, 0.915, 0.056] rim [0.766, 0.698, 0.222]
  - track 29 at frame 182: holes 0, rim-vs-core 0.37, rim-vs-outside 0.63, heterogeneity 0.12; core [0.989, 0.952, 0.057] rim [0.782, 0.706, 0.24]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 41.5 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.902)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 13.4 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.857)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 31.5, rim/outside 0.653 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.495)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=11800, R_eq 7.53): none; #11 (t=13400, R_eq 8): none; #14 (t=13800, R_eq 8.76): none; #29 (t=18200, R_eq 7.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
