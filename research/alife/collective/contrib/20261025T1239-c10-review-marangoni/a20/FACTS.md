# Evidence pack: marangoni-droplets (seed 7)

- world: `../../20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 342s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T1239-c10-review-marangoni/a20 --seeds 7 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0383, 1.286], min area 6 px

## Measurements
- components: final 22, mean 19.5, max 22; occupancy final 0.12
- tracks: 58; persistent (alive >= 50% of run): 22; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00743/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 28, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1811, -0.664, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 108: holes 0, rim-vs-core 0.16, rim-vs-outside 0.44, heterogeneity 0.06; core [0.912, 0.036, 0.011] rim [0.754, 0.055, 0.011]
  - track 24 at frame 108: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.929, 0.031, 0.012] rim [0.641, 0.074, 0.009]
  - track 27 at frame 109: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.06; core [0.931, 0.027, 0.021] rim [0.645, 0.073, 0.013]
  - track 54 at frame 143: holes 0, rim-vs-core 0.19, rim-vs-outside 0.43, heterogeneity 0.06; core [0.924, 0.031, 0.014] rim [0.733, 0.059, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 125 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 59.6 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.906)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.46, rim/outside 0.706 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.126)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.689, rim/outside 2.52 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.0507)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=10800, R_eq 5.05): none; #24 (t=10800, R_eq 5.01): none; #27 (t=10900, R_eq 5.26): none; #54 (t=14300, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
