# Evidence pack: cips-layered-divide (seed 13)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [128, 128]; wall 468s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py --out /tmp/claude-0/cs/lo25/seed13 --seeds 13 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0251, 0.9704], min area 6 px

## Measurements
- components: final 5, mean 4.2, max 5; occupancy final 0.04
- tracks: 8; persistent (alive >= 50% of run): 5; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00164/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 3, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.0, -0.7987, 0.2147, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 119: holes 0, rim-vs-core 0.38, rim-vs-outside 0.41, heterogeneity 0.10; core [0.917, 0.594, 0.0, 0.059] rim [0.693, 0.441, 0.043, 0.326]
  - track 4 at frame 123: holes 0, rim-vs-core 0.37, rim-vs-outside 0.78, heterogeneity 0.16; core [0.992, 0.969, 0.079, 0.103] rim [0.859, 0.804, 0.22, 0.368]
  - track 5 at frame 123: holes 0, rim-vs-core 0.59, rim-vs-outside 0.63, heterogeneity 0.17; core [0.99, 0.961, 0.093, 0.099] rim [0.774, 0.712, 0.286, 0.555]
  - track 6 at frame 136: holes 0, rim-vs-core 0.39, rim-vs-outside 0.41, heterogeneity 0.10; core [0.918, 0.596, 0.0, 0.059] rim [0.689, 0.439, 0.048, 0.331]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 20.3 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.871)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 11.8 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.737)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.6, rim/outside 0.646 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.406)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.02, rim/outside 19.5 (aggregate of 26 individuals; 25/26 membrane-like individually; rim level 0.541)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #3 (t=11900, R_eq 6.65): ['s']; #4 (t=12300, R_eq 8.41): ['s']; #5 (t=12300, R_eq 8.44): ['s']; #6 (t=13600, R_eq 6.46): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
