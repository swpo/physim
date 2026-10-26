# Evidence pack: phoretic-colloids (seed 6)

- world: `../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 213s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0430-c29-review-phoretic-dthalf/world.py --out collective/contrib/20261026T0430-c29-review-phoretic-dthalf/rerun_dthalf --seeds 6 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8225], min area 6 px

## Measurements
- components: final 14, mean 15.0, max 24; occupancy final 0.05
- tracks: 295; persistent (alive >= 50% of run): 5; longest 696 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 15, 10], H1 [0, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.483/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 10, default): splits 16, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 29, merge/split ratio 1.81, nucleations 234
- channel total drift (end/start - 1): [0.5657, 0.11, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 45 at frame 450: holes 0, rim-vs-core 0.23, rim-vs-outside 0.25, heterogeneity 0.21; core [0.653, 0.507, 0.568] rim [0.524, 0.336, 0.475]
  - track 62 at frame 343: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.20; core [0.843, 0.313, 0.715] rim [0.621, 0.287, 0.576]
  - track 77 at frame 356: holes 0, rim-vs-core 0.17, rim-vs-outside 0.29, heterogeneity 0.17; core [0.69, 0.396, 0.418] rim [0.574, 0.291, 0.362]
  - track 217 at frame 719: holes 0, rim-vs-core 0.35, rim-vs-outside 0.30, heterogeneity 0.23; core [0.894, 0.224, 0.75] rim [0.581, 0.269, 0.595]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 14.9 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.676)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 12.7 (aggregate of 77 individuals; 33/77 membrane-like individually; rim level 0.348)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 2.71 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.58)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #45 (t=225, R_eq 3.52): none; #62 (t=171.5, R_eq 4.37): ['B density']; #77 (t=178, R_eq 2.65): none; #217 (t=359.5, R_eq 4.48): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
