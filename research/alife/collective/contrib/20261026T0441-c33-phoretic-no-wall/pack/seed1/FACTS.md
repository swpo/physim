# Evidence pack: phoretic-colloids (seed 1)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 113s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-nuc/world.py --out collective/contrib/wip-c33-nuc/pack --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.1902], min area 6 px

## Measurements
- components: final 10, mean 11.8, max 19; occupancy final 0.04
- tracks: 195; persistent (alive >= 50% of run): 1; longest 427 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 8], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.521/time; max body lengths 8.5
- replication (lineage window K = 20 frames = time 10, default): splits 14, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 20, merge/split ratio 1.43, nucleations 147
- channel total drift (end/start - 1): [0.6, -0.425, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 122 at frame 592: holes 0, rim-vs-core 0.19, rim-vs-outside 0.26, heterogeneity 0.08; core [0.871, 0.021, 0.492] rim [0.695, 0.039, 0.429]
  - track 143 at frame 618: holes 0, rim-vs-core 0.19, rim-vs-outside 0.28, heterogeneity 0.12; core [0.801, 0.296, 0.529] rim [0.701, 0.146, 0.465]
  - track 137 at frame 592: holes 0, rim-vs-core 0.10, rim-vs-outside 0.24, heterogeneity 0.04; core [0.835, 0.0, 0.45] rim [0.742, 0.0, 0.407]
  - track 158 at frame 659: holes 0, rim-vs-core 0.13, rim-vs-outside 0.36, heterogeneity 0.07; core [0.924, 0.001, 0.602] rim [0.812, 0.021, 0.544]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 11.1 (aggregate of 62 individuals; 3/62 membrane-like individually; rim level 0.736)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 10.1 (aggregate of 62 individuals; 30/62 membrane-like individually; rim level 0.27)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 2.14 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.615)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #122 (t=296, R_eq 3.09): ['B density']; #143 (t=309, R_eq 3.14): none; #137 (t=296, R_eq 2.59): none; #158 (t=329.5, R_eq 3.52): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
