# Evidence pack: cips-layered-divide (seed 13)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1426s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T1945-c47-review-cips-moat/rerun/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.50 of robust range [0.021, 0.9769], min area 6 px

## Measurements
- components: final 19, mean 14.9, max 19; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 19; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.51 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00358/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.5718, 0.6178, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 116: holes 0, rim-vs-core 0.59, rim-vs-outside 0.61, heterogeneity 0.17; core [0.979, 0.921, 0.054, 0.08] rim [0.757, 0.682, 0.24, 0.53]
  - track 10 at frame 119: holes 0, rim-vs-core 0.53, rim-vs-outside 0.63, heterogeneity 0.16; core [0.987, 0.942, 0.051, 0.079] rim [0.791, 0.703, 0.235, 0.466]
  - track 13 at frame 119: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.17; core [0.988, 0.944, 0.062, 0.077] rim [0.776, 0.694, 0.249, 0.496]
  - track 18 at frame 139: holes 0, rim-vs-core 0.36, rim-vs-outside 0.77, heterogeneity 0.17; core [0.985, 0.934, 0.064, 0.079] rim [0.849, 0.782, 0.176, 0.354]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 44.7 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.917)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 13.6 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.859)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 28.5, rim/outside 0.661 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.503)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.43, rim/outside 28.1 (aggregate of 96 individuals; 92/96 membrane-like individually; rim level 0.679)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #8 (t=11600, R_eq 8.16): ['s']; #10 (t=11900, R_eq 7.69): ['s']; #13 (t=11900, R_eq 7.46): ['s']; #18 (t=13900, R_eq 7.65): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
