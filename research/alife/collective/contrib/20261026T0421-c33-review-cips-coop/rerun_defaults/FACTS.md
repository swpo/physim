# Evidence pack: cips-turnover (seed 4)

- world: `../../20261026T0301-c35-cips-coop-rods-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 241 frames x 500 steps x dt 0.1 = time 12000; grid [256, 256]; wall 1379s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0301-c35-cips-coop-rods-negative/world.py --out collective/contrib/wip-c33-cips/rerun --seeds 4 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0001, 0.9998], min area 6 px

## Measurements
- components: final 123, mean 157.5, max 306; occupancy final 0.14
- tracks: 485; persistent (alive >= 50% of run): 133; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [123, 123, 123], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00116/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 173, merge/split ratio n/a, nucleations 312
- channel total drift (end/start - 1): [0.0, -0.2776, 0.1913]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 123: holes 0, rim-vs-core 0.26, rim-vs-outside 0.50, heterogeneity 0.08; core [0.983, 0.847, 0.241] rim [0.807, 0.684, 0.354]
  - track 13 at frame 123: holes 0, rim-vs-core 0.27, rim-vs-outside 0.50, heterogeneity 0.09; core [0.973, 0.812, 0.316] rim [0.768, 0.66, 0.416]
  - track 19 at frame 123: holes 0, rim-vs-core 0.24, rim-vs-outside 0.49, heterogeneity 0.08; core [0.984, 0.846, 0.288] rim [0.829, 0.696, 0.389]
  - track 23 at frame 123: holes 0, rim-vs-core 0.27, rim-vs-outside 0.50, heterogeneity 0.09; core [0.975, 0.811, 0.288] rim [0.774, 0.659, 0.388]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 899 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 66.6 (aggregate of 899 individuals; 0/899 membrane-like individually; rim level 0.961)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 4.9 (aggregate of 899 individuals; 0/899 membrane-like individually; rim level 0.827)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.73, rim/outside 0.7 (aggregate of 899 individuals; 0/899 membrane-like individually; rim level 0.495)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=6150, R_eq 3.48): none; #13 (t=6150, R_eq 3.14): none; #19 (t=6150, R_eq 3.19): none; #23 (t=6150, R_eq 3.19): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
