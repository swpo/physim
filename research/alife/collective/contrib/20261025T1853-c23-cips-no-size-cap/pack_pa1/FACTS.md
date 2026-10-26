# Evidence pack: cips-fuel (seed 1)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 401 frames x 100 steps x dt 0.1 = time 4000; grid [256, 256]; wall 325s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1853-c23-cips-no-size-cap/world.py --out collective/contrib/20261025T1853-c23-cips-no-size-cap/pa1 --seeds 1 --frames 400 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0008, 0.9662], min area 6 px

## Measurements
- components: final 75, mean 85.1, max 162; occupancy final 0.14
- tracks: 295; persistent (alive >= 50% of run): 71; longest 336 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [79, 76, 74], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0305/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 106, merge/split ratio 106, nucleations 187
- channel total drift (end/start - 1): [0.0, -0.538, 0.4479]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 235: holes 0, rim-vs-core 0.22, rim-vs-outside 0.27, heterogeneity 0.06; core [0.864, 0.803, 0.024] rim [0.673, 0.714, 0.088]
  - track 6 at frame 235: holes 0, rim-vs-core 0.20, rim-vs-outside 0.25, heterogeneity 0.06; core [0.838, 0.833, 0.03] rim [0.664, 0.755, 0.089]
  - track 12 at frame 235: holes 0, rim-vs-core 0.21, rim-vs-outside 0.27, heterogeneity 0.06; core [0.875, 0.821, 0.022] rim [0.692, 0.733, 0.081]
  - track 13 at frame 235: holes 0, rim-vs-core 0.27, rim-vs-outside 0.30, heterogeneity 0.08; core [0.916, 0.875, 0.014] rim [0.689, 0.753, 0.085]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 493 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 13.8 (aggregate of 493 individuals; 0/493 membrane-like individually; rim level 0.797)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 3.06 (aggregate of 493 individuals; 0/493 membrane-like individually; rim level 0.839)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.4, rim/outside 0.512 (aggregate of 493 individuals; 0/493 membrane-like individually; rim level 0.417)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=2350, R_eq 3.91): none; #6 (t=2350, R_eq 3.99): none; #12 (t=2350, R_eq 3.99): none; #13 (t=2350, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
