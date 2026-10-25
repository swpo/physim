# Evidence pack: fch-cargo-micelles (seed 5)

- world: `../../20261025T0752-c03-fch-cargo-fission/world_chi0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0726-c03-fch-protocell/world.py; mutation: micelle-fission regime (eta1=4, eta2=5, amphiphile feed 5e-4) and chi=-3: the self-made solute partitions INTO amphiphile-rich bodies (cargo)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0752-c03-fch-cargo-fission/world_chi0.py --out collective/contrib/20261025T0827-c06-review-c03-cargo-fission/rerun_chi0 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.14 of robust range [0.111, 2.9835], min area 6 px

## Measurements
- components: final 52, mean 40.5, max 52; occupancy final 0.27
- tracks: 84; persistent (alive >= 50% of run): 48; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 5.06 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 55, 55], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 30, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.6579, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 50: holes 0, rim-vs-core 0.44, rim-vs-outside 0.12, heterogeneity 0.14; core [0.622, 0.496] rim [0.183, 0.476]
  - track 5 at frame 51: holes 0, rim-vs-core 0.44, rim-vs-outside 0.11, heterogeneity 0.15; core [0.603, 0.521] rim [0.167, 0.502]
  - track 7 at frame 51: holes 0, rim-vs-core 0.44, rim-vs-outside 0.11, heterogeneity 0.15; core [0.613, 0.53] rim [0.173, 0.511]
  - track 51 at frame 71: holes 0, rim-vs-core 0.45, rim-vs-outside 0.11, heterogeneity 0.15; core [0.629, 0.727] rim [0.183, 0.706]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 260 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 12.4 (aggregate of 260 individuals; 3/260 membrane-like individually; rim level 0.481)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 1.06 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.628)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=200, R_eq 4.69): none; #5 (t=204, R_eq 4.79): none; #7 (t=204, R_eq 4.75): none; #51 (t=284, R_eq 4.92): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
