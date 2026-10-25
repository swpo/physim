# Evidence pack: fch-cargo-micelles (seed 17)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0726-c03-fch-protocell/world.py; mutation: micelle-fission regime (eta1=4, eta2=5, amphiphile feed 5e-4) and chi=-3: the self-made solute partitions INTO amphiphile-rich bodies (cargo)
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 395s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0907-c12-review-cargo-fission/world.py --out collective/contrib/20261025T0907-c12-review-cargo-fission/rerun/seed17 --seeds 17 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1173, 2.9955], min area 6 px

## Measurements
- components: final 83, mean 52.3, max 83; occupancy final 0.41
- tracks: 149; persistent (alive >= 50% of run): 36; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 83, 83], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0174/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 80, default): splits 61, persistent splits 50 (0 more failed only because the siblings re-merged within K), max generation 5, merges 2, merge/split ratio 0.033, nucleations 22
- channel total drift (end/start - 1): [1.3299, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.10, heterogeneity 0.28; core [0.603, 0.203] rim [0.158, 0.001]
  - track 9 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.11, heterogeneity 0.28; core [0.62, 0.203] rim [0.173, 0.001]
  - track 11 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.11, heterogeneity 0.28; core [0.626, 0.207] rim [0.177, 0.001]
  - track 90 at frame 161: holes 0, rim-vs-core 0.48, rim-vs-outside 0.10, heterogeneity 0.25; core [0.615, 0.157] rim [0.165, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 355 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.511, rim/outside 6.11 (aggregate of 355 individuals; 4/355 membrane-like individually; rim level 0.478)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.036, rim/outside 1.72 (aggregate of 355 individuals; 4/355 membrane-like individually; rim level 0.014)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=404, R_eq 4.98): none; #9 (t=404, R_eq 5.01): none; #11 (t=404, R_eq 5.01): none; #90 (t=644, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
