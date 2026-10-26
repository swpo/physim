# Evidence pack: cips-layered-divide (seed 7)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 151 frames x 1000 steps x dt 0.1 = time 15000; grid [128, 128]; wall 409s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T2144-c47-review-cips-lattice/rerun_kF008/seed7 --seeds 7 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0533, 0.9399], min area 6 px

## Measurements
- components: final 14, mean 13.4, max 14; occupancy final 0.12
- tracks: 14; persistent (alive >= 50% of run): 14; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 14
- channel total drift (end/start - 1): [0.0, -0.3403, 1.4369, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 77: holes 0, rim-vs-core 0.63, rim-vs-outside 0.51, heterogeneity 0.17; core [0.959, 0.919, 0.065, 0.101] rim [0.722, 0.678, 0.244, 0.599]
  - track 1 at frame 77: holes 0, rim-vs-core 0.67, rim-vs-outside 0.50, heterogeneity 0.18; core [0.957, 0.917, 0.079, 0.103] rim [0.701, 0.663, 0.258, 0.641]
  - track 2 at frame 78: holes 0, rim-vs-core 0.61, rim-vs-outside 0.53, heterogeneity 0.18; core [0.965, 0.928, 0.099, 0.092] rim [0.729, 0.686, 0.255, 0.572]
  - track 3 at frame 78: holes 0, rim-vs-core 0.61, rim-vs-outside 0.51, heterogeneity 0.17; core [0.964, 0.925, 0.103, 0.092] rim [0.724, 0.679, 0.259, 0.578]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 37.1 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.924)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 11.7 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.858)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 18.4, rim/outside 0.669 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.482)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 11.5, rim/outside 38.8 (aggregate of 84 individuals; 84/84 membrane-like individually; rim level 0.899)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=7700, R_eq 7.14): ['s']; #1 (t=7700, R_eq 6.98): ['s']; #2 (t=7800, R_eq 6.36): ['s']; #3 (t=7800, R_eq 6.26): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
