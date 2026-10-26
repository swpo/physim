# Evidence pack: phoretic-colloids (seed 10)

- world: `../../../../20261026T0551-c33-phoretic-swimdivide-packs/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 385s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0551-c33-phoretic-swimdivide-packs/world.py --out collective/contrib/wip-c37/phor2/rerun/seed10 --seeds 10 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7657], min area 6 px

## Measurements
- components: final 13, mean 12.7, max 24; occupancy final 0.06
- tracks: 576; persistent (alive >= 50% of run): 0; longest 535 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 14, 11], H1 [0, 0, 0]
- motion: 88 long-lived tracks moved >= 1 body length; max speed 0.566/time; max body lengths 8.1
- replication (lineage window K = 20 frames = time 10, default): splits 49, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 10, merges 65, merge/split ratio 1.33, nucleations 414
- channel total drift (end/start - 1): [0.6029, 0.145, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 233 at frame 699: holes 0, rim-vs-core 0.15, rim-vs-outside 0.46, heterogeneity 0.22; core [0.777, 0.302, 0.734] rim [0.673, 0.213, 0.664]
  - track 22 at frame 296: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.18; core [0.685, 0.397, 0.618] rim [0.497, 0.336, 0.498]
  - track 88 at frame 323: holes 0, rim-vs-core 0.12, rim-vs-outside 0.20, heterogeneity 0.03; core [0.728, 0.0, 0.351] rim [0.613, 0.0, 0.317]
  - track 560 at frame 1560: holes 0, rim-vs-core 0.31, rim-vs-outside 0.23, heterogeneity 0.24; core [0.708, 0.403, 0.535] rim [0.418, 0.441, 0.442]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 18 (aggregate of 71 individuals; 2/71 membrane-like individually; rim level 0.627)
  - radial B density: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 14.7 (aggregate of 71 individuals; 26/71 membrane-like individually; rim level 0.34)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 3.01 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.594)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #233 (t=349.5, R_eq 5.01): none; #22 (t=148, R_eq 4.37): none; #88 (t=161.5, R_eq 2.11): none; #560 (t=780, R_eq 3.57): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
