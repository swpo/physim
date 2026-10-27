# Evidence pack: cips-turnover-divide (seed 2)

- world: `../../../20261026T1505-c41-cips-parasite-finding/world_base.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [192, 192]; wall 519s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-parasite-finding/world_base.py --out collective/contrib/20261026T1626-c42-review-parasite/rerun/seed2 --seeds 2 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0217, 0.9757], min area 6 px

## Measurements
- components: final 14, mean 9.3, max 14; occupancy final 0.08
- tracks: 21; persistent (alive >= 50% of run): 7; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00414/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, -0.6142, 0.6631]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 44: holes 0, rim-vs-core 0.37, rim-vs-outside 0.61, heterogeneity 0.12; core [0.984, 0.947, 0.044] rim [0.772, 0.704, 0.227]
  - track 2 at frame 30: holes 0, rim-vs-core 0.35, rim-vs-outside 0.60, heterogeneity 0.12; core [0.981, 0.932, 0.033] rim [0.779, 0.702, 0.209]
  - track 6 at frame 32: holes 0, rim-vs-core 0.25, rim-vs-outside 0.68, heterogeneity 0.12; core [0.981, 0.934, 0.053] rim [0.825, 0.762, 0.156]
  - track 7 at frame 58: holes 0, rim-vs-core 0.37, rim-vs-outside 0.61, heterogeneity 0.12; core [0.982, 0.94, 0.035] rim [0.768, 0.696, 0.22]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 32.5 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.861)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 12.6 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.836)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 25.5, rim/outside 0.646 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.491)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=4400, R_eq 8.18): none; #2 (t=3000, R_eq 8.69): none; #6 (t=3200, R_eq 8.87): none; #7 (t=5800, R_eq 8.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
