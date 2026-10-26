# Evidence pack: cips-layered-divide (seed 6)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1297s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T1415-c42-review-cips-layered/rerun/seed6 --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0215, 0.975], min area 6 px

## Measurements
- components: final 17, mean 11.7, max 17; occupancy final 0.09
- tracks: 30; persistent (alive >= 50% of run): 7; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.69 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00308/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.0, -0.5846, 0.6313, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.56, rim-vs-outside 0.62, heterogeneity 0.16; core [0.983, 0.939, 0.049, 0.08] rim [0.776, 0.702, 0.232, 0.499]
  - track 6 at frame 116: holes 0, rim-vs-core 0.52, rim-vs-outside 0.63, heterogeneity 0.16; core [0.988, 0.951, 0.047, 0.081] rim [0.794, 0.712, 0.229, 0.458]
  - track 9 at frame 116: holes 0, rim-vs-core 0.34, rim-vs-outside 0.78, heterogeneity 0.16; core [0.984, 0.939, 0.058, 0.081] rim [0.859, 0.802, 0.159, 0.342]
  - track 20 at frame 158: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.988, 0.95, 0.049, 0.08] rim [0.783, 0.706, 0.235, 0.482]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 34.9 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.873)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 12.6 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.837)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.5, rim/outside 0.651 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.496)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.85, rim/outside 20.1 (aggregate of 77 individuals; 69/77 membrane-like individually; rim level 0.56)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #5 (t=11400, R_eq 8.08): ['s']; #6 (t=11600, R_eq 7.76): ['s']; #9 (t=11600, R_eq 7.86): ['s']; #20 (t=15800, R_eq 7.76): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
