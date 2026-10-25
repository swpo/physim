# Evidence pack: cips-fuel (seed 4)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 314s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1926-c19-review-cips/fork/seed4 --seeds 4 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0001, 0.9974], min area 6 px

## Measurements
- components: final 0, mean 111.3, max 307; occupancy final 0.00
- tracks: 404; persistent (alive >= 50% of run): 0; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 7, 2], H1 [13, 6, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 84, merge/split ratio 84, nucleations 318
- channel total drift (end/start - 1): [0.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 88: holes 0, rim-vs-core 0.26, rim-vs-outside 0.51, heterogeneity 0.09; core [0.984, 0.937, 0.644] rim [0.795, 0.774, 0.7]
  - track 1 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.08; core [0.981, 0.931, 0.658] rim [0.778, 0.761, 0.717]
  - track 3 at frame 88: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.08; core [0.982, 0.932, 0.653] rim [0.787, 0.764, 0.712]
  - track 5 at frame 88: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.08; core [0.983, 0.944, 0.634] rim [0.792, 0.776, 0.695]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 725 components >= 12 px at frames [50, 101, 151]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 35 (aggregate of 725 individuals; 0/725 membrane-like individually; rim level 0.915)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 2.87 (aggregate of 725 individuals; 0/725 membrane-like individually; rim level 0.708)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.892 (aggregate of 725 individuals; 0/725 membrane-like individually; rim level 0.626)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=880, R_eq 3.34): none; #1 (t=880, R_eq 3.29): none; #3 (t=880, R_eq 3.29): none; #5 (t=880, R_eq 3.48): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
