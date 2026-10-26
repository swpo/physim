# Evidence pack: phoretic-colloids (seed 4)

- world: `../../20261026T0356-c33-phoretic-divide-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 111s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0356-c33-phoretic-divide-claim/world.py --out collective/contrib/20261026T0431-c30-review-phoretic-divide/tpack --seeds 4 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.765], min area 6 px

## Measurements
- components: final 8, mean 11.6, max 20; occupancy final 0.05
- tracks: 257; persistent (alive >= 50% of run): 0; longest 398 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 15, 8], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.476/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 10, default): splits 11, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 31, merge/split ratio 2.82, nucleations 204
- channel total drift (end/start - 1): [0.5343, 0.015, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 101 at frame 417: holes 0, rim-vs-core 0.17, rim-vs-outside 0.22, heterogeneity 0.18; core [0.656, 0.396, 0.349] rim [0.493, 0.353, 0.316]
  - track 35 at frame 269: holes 0, rim-vs-core 0.19, rim-vs-outside 0.27, heterogeneity 0.05; core [0.831, 0.0, 0.411] rim [0.651, 0.0, 0.356]
  - track 71 at frame 303: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.12; core [0.844, 0.19, 0.545] rim [0.609, 0.061, 0.444]
  - track 212 at frame 706: holes 0, rim-vs-core 0.31, rim-vs-outside 0.26, heterogeneity 0.23; core [0.69, 0.531, 0.645] rim [0.502, 0.322, 0.505]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 14.6 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.689)
  - radial B density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 9.31 (aggregate of 68 individuals; 20/68 membrane-like individually; rim level 0.313)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 2.74 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.578)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #101 (t=208.5, R_eq 2.33): none; #35 (t=134.5, R_eq 2.71): none; #71 (t=151.5, R_eq 3.78): none; #212 (t=353, R_eq 4.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
