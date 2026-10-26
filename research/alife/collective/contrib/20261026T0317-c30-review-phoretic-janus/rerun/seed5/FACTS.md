# Evidence pack: phoretic-colloids (seed 5)

- world: `../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/20261026T0317-c30-review-phoretic-janus/rerun --seeds 4 5 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7242], min area 6 px

## Measurements
- components: final 11, mean 18.5, max 32; occupancy final 0.07
- tracks: 157; persistent (alive >= 50% of run): 9; longest 291 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 14, 9], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.521/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 10, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 32, merge/split ratio 10.7, nucleations 119
- channel total drift (end/start - 1): [0.0, -0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 188: holes 0, rim-vs-core 0.17, rim-vs-outside 0.39, heterogeneity 0.15; core [0.754, 0.401, 0.423] rim [0.614, 0.309, 0.394]
  - track 13 at frame 182: holes 0, rim-vs-core 0.35, rim-vs-outside 0.28, heterogeneity 0.19; core [0.764, 0.501, 0.563] rim [0.433, 0.562, 0.458]
  - track 10 at frame 175: holes 0, rim-vs-core 0.12, rim-vs-outside 0.27, heterogeneity 0.12; core [0.594, 0.49, 0.296] rim [0.512, 0.408, 0.272]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 13.9 (aggregate of 91 individuals; 2/91 membrane-like individually; rim level 0.659)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 10.9 (aggregate of 91 individuals; 30/91 membrane-like individually; rim level 0.4)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 2.68 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.55)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=94, R_eq 3.34): ['B density']; #13 (t=91, R_eq 3.95): ['B density']; #10 (t=87.5, R_eq 1.87): none; #124 (t=154.5, R_eq 1.78): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
