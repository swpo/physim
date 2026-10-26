# Evidence pack: cips-turnover-divide (seed 9)

- world: `../../20261026T1025-c40-cips-turnover-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1352s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1025-c40-cips-turnover-divide-claim/world.py --out collective/contrib/20261026T1200-c41-review-cips-divide/rerun --seeds 9 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.021, 0.9758], min area 6 px

## Measurements
- components: final 18, mean 12.8, max 18; occupancy final 0.09
- tracks: 30; persistent (alive >= 50% of run): 12; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00317/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.5807, 0.6272]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 103: holes 0, rim-vs-core 0.36, rim-vs-outside 0.60, heterogeneity 0.12; core [0.98, 0.928, 0.052] rim [0.773, 0.697, 0.232]
  - track 8 at frame 121: holes 0, rim-vs-core 0.37, rim-vs-outside 0.62, heterogeneity 0.12; core [0.987, 0.948, 0.052] rim [0.783, 0.703, 0.24]
  - track 11 at frame 124: holes 0, rim-vs-core 0.40, rim-vs-outside 0.63, heterogeneity 0.13; core [0.986, 0.945, 0.055] rim [0.758, 0.687, 0.249]
  - track 26 at frame 175: holes 0, rim-vs-core 0.36, rim-vs-outside 0.64, heterogeneity 0.12; core [0.99, 0.958, 0.066] rim [0.792, 0.715, 0.247]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 42.5 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.905)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 13.8 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.857)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 28.4, rim/outside 0.656 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.501)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=10300, R_eq 8.21): none; #8 (t=12100, R_eq 7.84): none; #11 (t=12400, R_eq 7.96): none; #26 (t=17500, R_eq 7.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
