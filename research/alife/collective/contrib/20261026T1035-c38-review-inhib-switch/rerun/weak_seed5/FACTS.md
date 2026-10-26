# Evidence pack: cips-turnover (seed 5)

- world: `../../../20261026T0959-c39-cips-inhib-switch-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 1001 frames x 100 steps x dt 0.1 = time 10000; grid [192, 192]; wall 1085s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0959-c39-cips-inhib-switch-negative/world.py --out collective/contrib/20261026T1035-c38-review-inhib-switch/rerun/weak_seed5 --seeds 5 --frames 1000 --size 192 192 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0077, 0.9822], min area 6 px

## Measurements
- components: final 10, mean 7.2, max 11; occupancy final 0.05
- tracks: 11; persistent (alive >= 50% of run): 11; longest 735 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 51.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.0008, -0.8072, 0.8686]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 639: holes 0, rim-vs-core 0.18, rim-vs-outside 0.81, heterogeneity 0.10; core [0.964, 0.873, 0.022] rim [0.859, 0.766, 0.124]
  - track 1 at frame 655: holes 0, rim-vs-core 0.32, rim-vs-outside 0.72, heterogeneity 0.12; core [0.979, 0.913, 0.03] rim [0.793, 0.731, 0.21]
  - track 2 at frame 655: holes 0, rim-vs-core 0.29, rim-vs-outside 0.75, heterogeneity 0.11; core [0.984, 0.93, 0.031] rim [0.824, 0.757, 0.208]
  - track 3 at frame 664: holes 0, rim-vs-core 0.30, rim-vs-outside 0.74, heterogeneity 0.11; core [0.984, 0.931, 0.035] rim [0.815, 0.751, 0.205]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [336, 504, 664, 832, 1000]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 18.9 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.898)
  - radial p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 13.7 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.73)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.53, rim/outside 0.757 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.619)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6390, R_eq 13.85): none; #1 (t=6550, R_eq 12.49): none; #2 (t=6550, R_eq 11.41): none; #3 (t=6640, R_eq 11.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
