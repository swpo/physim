# Evidence pack: cips-turnover-divide (seed 4)

- world: `../../../20261026T1158-c39-cips-division-isotropy/world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1248s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1158-c39-cips-division-isotropy/world_iso.py --out collective/contrib/20261026T1517-c42-review-iso/rerun/seed4 --seeds 4 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0185, 0.9816], min area 6 px

## Measurements
- components: final 17, mean 8.2, max 17; occupancy final 0.08
- tracks: 31; persistent (alive >= 50% of run): 1; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.32 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00367/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.0, -0.5922, 0.6395]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 75: holes 0, rim-vs-core 0.35, rim-vs-outside 0.69, heterogeneity 0.12; core [0.988, 0.956, 0.041] rim [0.8, 0.718, 0.22]
  - track 11 at frame 92: holes 0, rim-vs-core 0.34, rim-vs-outside 0.69, heterogeneity 0.12; core [0.991, 0.962, 0.039] rim [0.817, 0.727, 0.22]
  - track 7 at frame 66: holes 0, rim-vs-core 0.36, rim-vs-outside 0.68, heterogeneity 0.12; core [0.986, 0.944, 0.034] rim [0.793, 0.706, 0.216]
  - track 19 at frame 107: holes 0, rim-vs-core 0.35, rim-vs-outside 0.69, heterogeneity 0.12; core [0.993, 0.965, 0.052] rim [0.812, 0.725, 0.233]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 42.9 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.917)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 13.9 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.875)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 28.7, rim/outside 0.65 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.491)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=7500, R_eq 8.35): none; #11 (t=9200, R_eq 7.98): none; #7 (t=6600, R_eq 8.56): none; #19 (t=10700, R_eq 7.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
