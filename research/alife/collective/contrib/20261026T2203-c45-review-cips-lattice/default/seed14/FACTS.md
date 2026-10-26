# Evidence pack: cips-layered-divide (seed 14)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 151 frames x 1000 steps x dt 0.1 = time 15000; grid [128, 128]; wall 355s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out /tmp/claude-0/cl/default/seed14 --seeds 14 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0219, 0.974], min area 6 px

## Measurements
- components: final 7, mean 6.1, max 7; occupancy final 0.09
- tracks: 10; persistent (alive >= 50% of run): 7; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00132/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 3, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.0, -0.595, 0.6426, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 91: holes 0, rim-vs-core 0.60, rim-vs-outside 0.60, heterogeneity 0.17; core [0.982, 0.932, 0.06, 0.081] rim [0.755, 0.685, 0.248, 0.541]
  - track 4 at frame 91: holes 0, rim-vs-core 0.33, rim-vs-outside 0.79, heterogeneity 0.16; core [0.985, 0.933, 0.083, 0.076] rim [0.861, 0.803, 0.17, 0.336]
  - track 5 at frame 91: holes 0, rim-vs-core 0.55, rim-vs-outside 0.60, heterogeneity 0.16; core [0.979, 0.92, 0.065, 0.074] rim [0.771, 0.696, 0.237, 0.503]
  - track 6 at frame 92: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.16; core [0.988, 0.947, 0.058, 0.081] rim [0.777, 0.699, 0.247, 0.499]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 49.1 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.913)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 15.1 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.863)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 37.1, rim/outside 0.656 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.505)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.39, rim/outside 25.6 (aggregate of 38 individuals; 38/38 membrane-like individually; rim level 0.553)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #3 (t=9100, R_eq 8.25): ['s']; #4 (t=9100, R_eq 7.69): ['s']; #5 (t=9100, R_eq 8.5): ['s']; #6 (t=9200, R_eq 7.94): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
