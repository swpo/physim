# Evidence pack: marangoni-droplets (seed 4)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 393s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1356-c12-review-marangoni/world.py --out collective/contrib/20261025T1356-c12-review-marangoni/a20/seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0385, 1.2903], min area 6 px

## Measurements
- components: final 22, mean 19.3, max 22; occupancy final 0.12
- tracks: 68; persistent (alive >= 50% of run): 18; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00571/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 2000, default): splits 33, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1805, -0.6629, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 104: holes 0, rim-vs-core 0.26, rim-vs-outside 0.32, heterogeneity 0.06; core [0.934, 0.04, 0.011] rim [0.672, 0.075, 0.01]
  - track 12 at frame 104: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.06; core [0.922, 0.041, 0.012] rim [0.637, 0.077, 0.01]
  - track 17 at frame 106: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.07; core [0.924, 0.027, 0.035] rim [0.613, 0.076, 0.024]
  - track 57 at frame 114: holes 0, rim-vs-core 0.30, rim-vs-outside 0.32, heterogeneity 0.07; core [0.929, 0.029, 0.025] rim [0.628, 0.075, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 124 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 58.6 (aggregate of 124 individuals; 0/124 membrane-like individually; rim level 0.906)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.2, rim/outside 0.708 (aggregate of 124 individuals; 0/124 membrane-like individually; rim level 0.127)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.63, rim/outside 2.67 (aggregate of 124 individuals; 0/124 membrane-like individually; rim level 0.0669)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=10400, R_eq 4.41): none; #12 (t=10400, R_eq 4.51): none; #17 (t=10600, R_eq 5.5): none; #57 (t=11400, R_eq 5.23): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
