# Evidence pack: phoretic-colloids (seed 6)

- world: `../../../20261026T0551-c33-phoretic-swimdivide-packs/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 194s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0551-c33-phoretic-swimdivide-packs/world.py --out collective/contrib/c39-rev-phor2-wip/rerun/seed6 --seeds 6 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6743], min area 6 px

## Measurements
- components: final 11, mean 14.7, max 29; occupancy final 0.06
- tracks: 442; persistent (alive >= 50% of run): 0; longest 631 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 7], H1 [0, 0, 0]
- motion: 101 long-lived tracks moved >= 1 body length; max speed 0.559/time; max body lengths 10.2
- replication (lineage window K = 20 frames = time 10, default): splits 55, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 11, merges 72, merge/split ratio 1.31, nucleations 261
- channel total drift (end/start - 1): [0.5471, 0.17, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 209 at frame 941: holes 0, rim-vs-core 0.11, rim-vs-outside 0.23, heterogeneity 0.09; core [0.707, 0.144, 0.334] rim [0.608, 0.115, 0.304]
  - track 71 at frame 430: holes 0, rim-vs-core 0.26, rim-vs-outside 0.26, heterogeneity 0.13; core [0.704, 0.347, 0.534] rim [0.617, 0.114, 0.449]
  - track 32 at frame 363: holes 0, rim-vs-core 0.29, rim-vs-outside 0.37, heterogeneity 0.10; core [0.906, 0.006, 0.501] rim [0.639, 0.057, 0.414]
  - track 417 at frame 1573: holes 0, rim-vs-core 0.30, rim-vs-outside 0.24, heterogeneity 0.29; core [0.656, 0.387, 0.772] rim [0.411, 0.376, 0.599]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 15.5 (aggregate of 78 individuals; 3/78 membrane-like individually; rim level 0.625)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 16.3 (aggregate of 78 individuals; 29/78 membrane-like individually; rim level 0.342)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 2.83 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.578)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #209 (t=470.5, R_eq 2.03): ['B density']; #71 (t=215, R_eq 3.52): none; #32 (t=181.5, R_eq 3.43): ['B density']; #417 (t=786.5, R_eq 5.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
