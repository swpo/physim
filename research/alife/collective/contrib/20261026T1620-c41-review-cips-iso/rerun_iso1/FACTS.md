# Evidence pack: cips-turnover-divide (seed 15)

- world: `../../20261026T1158-c39-cips-division-isotropy/world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1136s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1158-c39-cips-division-isotropy/world_iso.py --out collective/contrib/20261026T1620-c41-review-cips-iso/rerun_iso1 --seeds 15 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0175, 0.9845], min area 6 px

## Measurements
- components: final 19, mean 15.6, max 19; occupancy final 0.09
- tracks: 28; persistent (alive >= 50% of run): 15; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00187/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 10
- channel total drift (end/start - 1): [0.0, -0.5652, 0.6106]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.68, heterogeneity 0.12; core [0.987, 0.941, 0.051] rim [0.808, 0.705, 0.236]
  - track 7 at frame 63: holes 0, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.12; core [0.986, 0.935, 0.048] rim [0.812, 0.708, 0.228]
  - track 10 at frame 74: holes 0, rim-vs-core 0.25, rim-vs-outside 0.79, heterogeneity 0.12; core [0.99, 0.954, 0.048] rim [0.867, 0.781, 0.184]
  - track 26 at frame 96: holes 0, rim-vs-core 0.36, rim-vs-outside 0.69, heterogeneity 0.12; core [0.991, 0.95, 0.07] rim [0.804, 0.704, 0.251]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 55.4 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.952)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 15.2 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.886)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 28.2, rim/outside 0.663 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.505)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 8): none; #7 (t=6300, R_eq 8.16): none; #10 (t=7400, R_eq 7.86): none; #26 (t=9600, R_eq 7.4): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
