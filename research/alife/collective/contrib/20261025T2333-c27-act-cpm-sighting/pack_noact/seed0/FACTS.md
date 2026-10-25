# Evidence pack: act-cpm (seed 0)

- world: `../../world.py`, family `cellular-potts`
- parent: None; mutation: new class: Cellular Potts model with the Act (actin activity memory) term of Niculescu et al. 2015, cells planted as 3x3 seeds
- run: 201 frames x 10 steps x dt 1.0 = time 2000; grid [128, 128]; wall 2s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27m/world.py --out collective/contrib/wip-c27m/pack_noact --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 39.8, max 40; occupancy final 0.25
- tracks: 40; persistent (alive >= 50% of run): 40; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.02 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 40
- channel total drift (end/start - 1): [101.55, 1.421, 3.6688]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.02, rim-vs-outside 1.43, heterogeneity 0.02; core [1.0, 0.0, 0.0] rim [1.0, 0.02, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.02, rim-vs-outside 1.46, heterogeneity 0.02; core [1.0, 0.0, 0.0] rim [1.0, 0.019, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.00, rim-vs-outside 1.44, heterogeneity 0.00; core [1.0, 0.0, 0.0] rim [1.0, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.00, rim-vs-outside 1.43, heterogeneity 0.01; core [1.0, 0.0, 0.0] rim [1.0, 0.005, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial cell (sigma > 0): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 3.6 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.999)
  - radial activity act/max: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 19.2, rim/outside 6 (aggregate of 240 individuals; 240/240 membrane-like individually; rim level 0.182)  MEMBRANE-LIKE
  - radial cell boundary: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 54, rim/outside 7.21 (aggregate of 240 individuals; 240/240 membrane-like individually; rim level 0.53)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): activity act/max, cell boundary
- membrane-like channels per top track at mid-life: #0 (t=1010, R_eq 5.7): ['activity act/max', 'cell boundary']; #1 (t=1010, R_eq 5.73): ['activity act/max', 'cell boundary']; #2 (t=1010, R_eq 5.7): ['activity act/max', 'cell boundary']; #3 (t=1010, R_eq 5.64): ['activity act/max', 'cell boundary']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
