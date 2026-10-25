# Evidence pack: marangoni-droplets (seed 2)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 280s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1410-c13-review-marangoni/world.py --out collective/contrib/20261025T1410-c13-review-marangoni/rerun_a20/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0385, 1.2844], min area 6 px

## Measurements
- components: final 20, mean 18.0, max 20; occupancy final 0.12
- tracks: 50; persistent (alive >= 50% of run): 20; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00115/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 2000, default): splits 20, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1771, -0.6582, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 103: holes 0, rim-vs-core 0.31, rim-vs-outside 0.31, heterogeneity 0.07; core [0.924, 0.029, 0.07] rim [0.615, 0.081, 0.055]
  - track 8 at frame 103: holes 0, rim-vs-core 0.29, rim-vs-outside 0.30, heterogeneity 0.08; core [0.903, 0.036, 0.164] rim [0.616, 0.083, 0.12]
  - track 24 at frame 111: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.07; core [0.928, 0.028, 0.029] rim [0.614, 0.081, 0.021]
  - track 42 at frame 124: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.07; core [0.927, 0.029, 0.031] rim [0.612, 0.081, 0.02]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 57.3 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.91)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.3, rim/outside 0.701 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.133)
  - radial |v| (flow speed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 2.86 (aggregate of 116 individuals; 1/116 membrane-like individually; rim level 0.0689)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=10300, R_eq 5.73): none; #8 (t=10300, R_eq 5.89): none; #24 (t=11100, R_eq 5.75): none; #42 (t=12400, R_eq 5.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
