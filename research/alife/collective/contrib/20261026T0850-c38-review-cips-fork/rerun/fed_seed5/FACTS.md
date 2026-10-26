# Evidence pack: cips-turnover (seed 5)

- world: `../../../20261026T0704-c35-cips-coop-fork-lsc5/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 951 frames x 100 steps x dt 0.1 = time 9500; grid [192, 192]; wall 885s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5/world.py --out collective/contrib/20261026T0850-c38-review-cips-fork/rerun/fed_seed5 --seeds 5 --frames 950 --size 192 192 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0075, 0.9832], min area 6 px

## Measurements
- components: final 11, mean 7.1, max 11; occupancy final 0.11
- tracks: 11; persistent (alive >= 50% of run): 11; longest 685 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 51.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.0008, -0.5665, 0.61]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 615: holes 0, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.10; core [0.955, 0.848, 0.024] rim [0.853, 0.751, 0.127]
  - track 1 at frame 631: holes 0, rim-vs-core 0.28, rim-vs-outside 0.72, heterogeneity 0.11; core [0.974, 0.89, 0.029] rim [0.817, 0.734, 0.204]
  - track 2 at frame 631: holes 0, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.11; core [0.98, 0.91, 0.033] rim [0.819, 0.74, 0.215]
  - track 3 at frame 639: holes 0, rim-vs-core 0.30, rim-vs-outside 0.73, heterogeneity 0.11; core [0.979, 0.909, 0.037] rim [0.807, 0.732, 0.211]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [319, 479, 631, 790, 950]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 47.6 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.878)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 17.5 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.854)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.2, rim/outside 0.667 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.521)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6150, R_eq 13.95): none; #1 (t=6310, R_eq 12.36): none; #2 (t=6310, R_eq 11.45): none; #3 (t=6390, R_eq 11.98): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
