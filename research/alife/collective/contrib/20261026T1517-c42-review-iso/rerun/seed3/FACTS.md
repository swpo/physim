# Evidence pack: cips-turnover-divide (seed 3)

- world: `../../../20261026T1158-c39-cips-division-isotropy/world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1249s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1158-c39-cips-division-isotropy/world_iso.py --out collective/contrib/20261026T1517-c42-review-iso/rerun/seed3 --seeds 3 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0176, 0.982], min area 6 px

## Measurements
- components: final 17, mean 12.0, max 17; occupancy final 0.09
- tracks: 28; persistent (alive >= 50% of run): 7; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00459/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.5833, 0.63]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 72: holes 0, rim-vs-core 0.33, rim-vs-outside 0.69, heterogeneity 0.12; core [0.986, 0.943, 0.042] rim [0.819, 0.72, 0.219]
  - track 9 at frame 75: holes 0, rim-vs-core 0.35, rim-vs-outside 0.69, heterogeneity 0.12; core [0.991, 0.957, 0.06] rim [0.809, 0.716, 0.244]
  - track 12 at frame 76: holes 0, rim-vs-core 0.35, rim-vs-outside 0.69, heterogeneity 0.12; core [0.99, 0.956, 0.056] rim [0.812, 0.716, 0.239]
  - track 16 at frame 92: holes 0, rim-vs-core 0.35, rim-vs-outside 0.68, heterogeneity 0.12; core [0.988, 0.947, 0.05] rim [0.81, 0.711, 0.234]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 48 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.938)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 15.4 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.883)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 31, rim/outside 0.658 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.503)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=7200, R_eq 8.46): none; #9 (t=7500, R_eq 7.72): none; #12 (t=7600, R_eq 7.82): none; #16 (t=9200, R_eq 8.04): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
