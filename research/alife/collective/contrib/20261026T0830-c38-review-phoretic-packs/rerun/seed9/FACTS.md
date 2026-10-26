# Evidence pack: phoretic-colloids (seed 9)

- world: `../../../20261026T0551-c33-phoretic-swimdivide-packs/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 367s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0551-c33-phoretic-swimdivide-packs/world.py --out collective/contrib/20261026T0830-c38-review-phoretic-packs/rerun/seed9 --seeds 9 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7527], min area 6 px

## Measurements
- components: final 12, mean 13.1, max 21; occupancy final 0.05
- tracks: 536; persistent (alive >= 50% of run): 0; longest 573 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 17, 12], H1 [0, 0, 0]
- motion: 110 long-lived tracks moved >= 1 body length; max speed 0.564/time; max body lengths 10.4
- replication (lineage window K = 20 frames = time 10, default): splits 52, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 10, merges 64, merge/split ratio 1.23, nucleations 368
- channel total drift (end/start - 1): [0.5357, 0.175, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 336: holes 0, rim-vs-core 0.33, rim-vs-outside 0.26, heterogeneity 0.16; core [0.813, 0.145, 0.544] rim [0.513, 0.214, 0.435]
  - track 93 at frame 430: holes 0, rim-vs-core 0.28, rim-vs-outside 0.28, heterogeneity 0.08; core [0.877, 0.006, 0.443] rim [0.603, 0.029, 0.372]
  - track 292 at frame 914: holes 0, rim-vs-core 0.17, rim-vs-outside 0.25, heterogeneity 0.17; core [0.589, 0.49, 0.359] rim [0.469, 0.382, 0.313]
  - track 486 at frame 1506: holes 0, rim-vs-core 0.28, rim-vs-outside 0.26, heterogeneity 0.24; core [0.688, 0.373, 0.683] rim [0.49, 0.254, 0.521]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 14.6 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.606)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 16.6 (aggregate of 67 individuals; 26/67 membrane-like individually; rim level 0.362)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.07 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.568)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=168, R_eq 3.87): ['B density']; #93 (t=215, R_eq 3.09): ['B density']; #292 (t=457, R_eq 2.59): none; #486 (t=753, R_eq 5.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
