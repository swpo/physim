# Evidence pack: cips-layered-divide (seed 7)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 151 frames x 1000 steps x dt 0.1 = time 15000; grid [128, 128]; wall 412s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T2144-c47-review-cips-lattice/rerun_kF012/seed7 --seeds 7 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0343, 0.9629], min area 6 px

## Measurements
- components: final 15, mean 14.7, max 15; occupancy final 0.14
- tracks: 15; persistent (alive >= 50% of run): 15; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00164/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 15
- channel total drift (end/start - 1): [0.0, -0.3723, 1.0225, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 77: holes 0, rim-vs-core 0.62, rim-vs-outside 0.55, heterogeneity 0.17; core [0.971, 0.92, 0.066, 0.08] rim [0.734, 0.668, 0.254, 0.557]
  - track 1 at frame 77: holes 0, rim-vs-core 0.65, rim-vs-outside 0.55, heterogeneity 0.18; core [0.966, 0.91, 0.062, 0.085] rim [0.718, 0.657, 0.255, 0.596]
  - track 2 at frame 77: holes 0, rim-vs-core 0.61, rim-vs-outside 0.56, heterogeneity 0.17; core [0.973, 0.925, 0.073, 0.076] rim [0.738, 0.672, 0.256, 0.545]
  - track 3 at frame 77: holes 0, rim-vs-core 0.63, rim-vs-outside 0.56, heterogeneity 0.18; core [0.973, 0.924, 0.08, 0.077] rim [0.728, 0.666, 0.263, 0.563]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 55.9 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.951)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 13.5 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.869)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 30.8, rim/outside 0.678 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.501)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 10.8, rim/outside 44.8 (aggregate of 90 individuals; 90/90 membrane-like individually; rim level 0.848)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=7700, R_eq 7.25): ['s']; #1 (t=7700, R_eq 7.57): ['s']; #2 (t=7700, R_eq 7): ['s']; #3 (t=7700, R_eq 6.91): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
