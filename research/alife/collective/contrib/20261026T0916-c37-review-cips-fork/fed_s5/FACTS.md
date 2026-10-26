# Evidence pack: cips-turnover (seed 5)

- world: `../../../20261026T0704-c35-cips-coop-fork-lsc5/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 91 frames x 1000 steps x dt 0.1 = time 9000; grid [192, 192]; wall 937s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5/world.py --out collective/contrib/wip-c37/cips/fed_s5 --seeds 5 --size 192 192 --spf 1000 --frames 90 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0076, 0.9832], min area 6 px

## Measurements
- components: final 11, mean 6.8, max 11; occupancy final 0.11
- tracks: 11; persistent (alive >= 50% of run): 11; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.24 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.0008, -0.5682, 0.6119]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 59: holes 0, rim-vs-core 0.17, rim-vs-outside 0.80, heterogeneity 0.10; core [0.952, 0.845, 0.026] rim [0.854, 0.753, 0.126]
  - track 1 at frame 61: holes 0, rim-vs-core 0.29, rim-vs-outside 0.73, heterogeneity 0.11; core [0.973, 0.888, 0.029] rim [0.811, 0.729, 0.208]
  - track 2 at frame 61: holes 0, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.11; core [0.98, 0.911, 0.034] rim [0.817, 0.74, 0.217]
  - track 3 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.73, heterogeneity 0.11; core [0.979, 0.908, 0.036] rim [0.818, 0.739, 0.21]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [30, 45, 60, 75, 90]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 53.3 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.889)
  - radial p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 18.9 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.863)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.6, rim/outside 0.669 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.525)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5900, R_eq 13.99): none; #1 (t=6100, R_eq 12.45): none; #2 (t=6100, R_eq 11.48): none; #3 (t=6200, R_eq 11.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
