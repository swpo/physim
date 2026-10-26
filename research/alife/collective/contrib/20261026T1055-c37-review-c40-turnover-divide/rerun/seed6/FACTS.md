# Evidence pack: cips-turnover-divide (seed 6)

- world: `../../../../20261026T1025-c40-cips-turnover-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [192, 192]; wall 798s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1025-c40-cips-turnover-divide-claim/world.py --out collective/contrib/wip-c37/c40/rerun/seed6 --seeds 6 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0227, 0.9739], min area 6 px

## Measurements
- components: final 12, mean 6.7, max 12; occupancy final 0.06
- tracks: 20; persistent (alive >= 50% of run): 7; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.0, -0.6435, 0.6944]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 55: holes 0, rim-vs-core 0.36, rim-vs-outside 0.61, heterogeneity 0.12; core [0.982, 0.947, 0.036] rim [0.777, 0.716, 0.213]
  - track 6 at frame 55: holes 0, rim-vs-core 0.37, rim-vs-outside 0.62, heterogeneity 0.12; core [0.985, 0.953, 0.034] rim [0.777, 0.713, 0.215]
  - track 9 at frame 56: holes 0, rim-vs-core 0.21, rim-vs-outside 0.77, heterogeneity 0.12; core [0.986, 0.95, 0.047] rim [0.858, 0.813, 0.147]
  - track 11 at frame 57: holes 0, rim-vs-core 0.38, rim-vs-outside 0.61, heterogeneity 0.12; core [0.983, 0.95, 0.035] rim [0.764, 0.705, 0.219]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 24.6 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.824)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 11.3 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.813)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 20.2, rim/outside 0.638 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.485)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=5500, R_eq 8.43): none; #6 (t=5500, R_eq 8.37): none; #9 (t=5600, R_eq 8.02): none; #11 (t=5700, R_eq 8.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
