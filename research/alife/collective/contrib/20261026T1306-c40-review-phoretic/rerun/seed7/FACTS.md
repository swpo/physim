# Evidence pack: phoretic-colloids (seed 7)

- world: `../../../20261026T0529-c33-phoretic-swimdivide-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 91s; status ok
- command: `python -m labkit.run ../20261026T0529-c33-phoretic-swimdivide-claim/world.py --out rerun/seed7 --seeds 7 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5144], min area 6 px

## Measurements
- components: final 17, mean 19.9, max 28; occupancy final 0.05
- tracks: 363; persistent (alive >= 50% of run): 7; longest 618 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 20, 12], H1 [0, 0, 0]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 0.53/time; max body lengths 7.6
- replication (lineage window K = 20 frames = time 10, default): splits 25, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 4, merges 42, merge/split ratio 1.68, nucleations 273
- channel total drift (end/start - 1): [0.5414, 0.045, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 123 at frame 471: holes 0, rim-vs-core 0.11, rim-vs-outside 0.24, heterogeneity 0.03; core [0.747, 0.0, 0.339] rim [0.639, 0.0, 0.311]
  - track 55 at frame 376: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.14; core [0.624, 0.534, 0.424] rim [0.503, 0.309, 0.369]
  - track 150 at frame 477: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.18; core [0.806, 0.282, 0.667] rim [0.531, 0.196, 0.533]
  - track 347 at frame 780: holes 0, rim-vs-core 0.35, rim-vs-outside 0.26, heterogeneity 0.24; core [0.798, 0.252, 0.724] rim [0.473, 0.289, 0.586]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 19.5 (aggregate of 91 individuals; 1/91 membrane-like individually; rim level 0.686)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.719, rim/outside 11.6 (aggregate of 91 individuals; 31/91 membrane-like individually; rim level 0.281)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 2.81 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.582)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #123 (t=235.5, R_eq 1.95): none; #55 (t=188, R_eq 2.52): none; #150 (t=238.5, R_eq 4.18): none; #347 (t=390, R_eq 4.3): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
