# Evidence pack: cips-turnover-divide (seed 1)

- world: `../../world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 909s; status ok
- command: `python -m labkit.run collective/contrib/c39-cips-iso-wip/world_iso.py --out collective/contrib/c39-cips-iso-wip/noise_iso1/seed1 --seeds 1 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0176, 0.9824], min area 6 px

## Measurements
- components: final 18, mean 12.8, max 18; occupancy final 0.09
- tracks: 28; persistent (alive >= 50% of run): 10; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00346/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [0.0, -0.5744, 0.6205]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 0.69, heterogeneity 0.12; core [0.989, 0.95, 0.054] rim [0.8, 0.704, 0.242]
  - track 7 at frame 72: holes 0, rim-vs-core 0.36, rim-vs-outside 0.70, heterogeneity 0.12; core [0.99, 0.952, 0.055] rim [0.803, 0.708, 0.242]
  - track 9 at frame 73: holes 0, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.12; core [0.988, 0.944, 0.048] rim [0.813, 0.711, 0.231]
  - track 19 at frame 93: holes 0, rim-vs-core 0.34, rim-vs-outside 0.69, heterogeneity 0.12; core [0.989, 0.947, 0.048] rim [0.814, 0.714, 0.229]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 49.6 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.938)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 15.2 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.883)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 31.5, rim/outside 0.66 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.505)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=6200, R_eq 7.92): none; #7 (t=7200, R_eq 7.88): none; #9 (t=7300, R_eq 8.06): none; #19 (t=9300, R_eq 8.04): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
