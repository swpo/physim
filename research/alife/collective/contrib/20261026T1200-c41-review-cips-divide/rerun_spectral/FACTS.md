# Evidence pack: cips-turnover-divide (seed 9)

- world: `../world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1169s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1200-c41-review-cips-divide/world_iso.py --out collective/contrib/20261026T1200-c41-review-cips-divide/rerun_spectral --seeds 9 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0183, 0.9812], min area 6 px

## Measurements
- components: final 17, mean 11.3, max 17; occupancy final 0.09
- tracks: 27; persistent (alive >= 50% of run): 8; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.26 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00357/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, -0.584, 0.6308]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 62: holes 0, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.12; core [0.989, 0.95, 0.047] rim [0.819, 0.72, 0.23]
  - track 7 at frame 76: holes 0, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.12; core [0.987, 0.944, 0.044] rim [0.812, 0.713, 0.229]
  - track 9 at frame 76: holes 0, rim-vs-core 0.36, rim-vs-outside 0.69, heterogeneity 0.12; core [0.989, 0.951, 0.054] rim [0.804, 0.711, 0.239]
  - track 17 at frame 90: holes 0, rim-vs-core 0.35, rim-vs-outside 0.70, heterogeneity 0.12; core [0.992, 0.959, 0.06] rim [0.812, 0.719, 0.244]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 51.3 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.956)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 15.9 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.896)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 31.2, rim/outside 0.659 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.504)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6200, R_eq 8.2): none; #7 (t=7600, R_eq 8.39): none; #9 (t=7600, R_eq 8.08): none; #17 (t=9000, R_eq 7.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
