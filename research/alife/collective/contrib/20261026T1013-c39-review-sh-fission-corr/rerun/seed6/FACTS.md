# Evidence pack: sh-spots-inhibitor (seed 6)

- world: `../../world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor (drift bifurcation, kap*tau=3) and a consumed regrowing resource that sets the local growth rate; new class
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 39s; status ok
- command: `python -m labkit.run collective/contrib/c39-rev-shcorr-wip/world.py --out collective/contrib/c39-rev-shcorr-wip/rerun/seed6 --seeds 6 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.3914, 1.5957], min area 6 px

## Measurements
- components: final 60, mean 55.7, max 125; occupancy final 0.12
- tracks: 198; persistent (alive >= 50% of run): 49; longest 201 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 4.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [70, 61, 60], H1 [20, 0, 0]
- motion: 80 long-lived tracks moved >= 1 body length; max speed 0.273/time; max body lengths 45.7
- replication (lineage window K = 20 frames = time 100, default): splits 29, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.069, nucleations 68
- channel total drift (end/start - 1): [30.5571, None, -0.3386]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.16, rim-vs-outside 0.44, heterogeneity 0.16; core [0.817, 0.718, 0.168] rim [0.694, 0.624, 0.194]
  - track 7 at frame 101: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.15; core [0.871, 0.718, 0.038] rim [0.608, 0.538, 0.081]
  - track 10 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.23, heterogeneity 0.16; core [0.86, 0.714, 0.085] rim [0.572, 0.523, 0.14]
  - track 15 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.26, heterogeneity 0.15; core [0.842, 0.741, 0.161] rim [0.558, 0.521, 0.225]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 322 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (SH field): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 9.23 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.743)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.16 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.634)
  - radial R (resource): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.57, rim/outside 0.841 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.187)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=505, R_eq 3.29): none; #7 (t=505, R_eq 3.04): none; #10 (t=505, R_eq 3.19): none; #15 (t=505, R_eq 3.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
