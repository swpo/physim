# Evidence pack: marangoni-droplets (seed 7)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 275s; status ok
- command: `python -m labkit.run collective/contrib/c17-marangoni-wip/world.py --out collective/contrib/c17-marangoni-wip/rerun_a20/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0211, 1.2357], min area 6 px

## Measurements
- components: final 36, mean 28.3, max 47; occupancy final 0.12
- tracks: 224; persistent (alive >= 50% of run): 36; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 36], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.00559/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 2000, default): splits 86, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 29, merge/split ratio 0.337, nucleations 18
- channel total drift (end/start - 1): [0.2022, -0.6826, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 136 at frame 128: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.927, 0.012, 0.069] rim [0.643, 0.041, 0.058]
  - track 147 at frame 128: holes 0, rim-vs-core 0.27, rim-vs-outside 0.31, heterogeneity 0.07; core [0.925, 0.012, 0.109] rim [0.659, 0.042, 0.085]
  - track 149 at frame 128: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.07; core [0.918, 0.014, 0.098] rim [0.62, 0.045, 0.078]
  - track 175 at frame 129: holes 0, rim-vs-core 0.19, rim-vs-outside 0.41, heterogeneity 0.07; core [0.917, 0.013, 0.091] rim [0.731, 0.033, 0.083]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 187 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 37.5 (aggregate of 187 individuals; 0/187 membrane-like individually; rim level 0.855)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.17, rim/outside 0.71 (aggregate of 187 individuals; 0/187 membrane-like individually; rim level 0.0827)
  - radial |v| (flow speed): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 3.78 (aggregate of 187 individuals; 1/187 membrane-like individually; rim level 0.0963)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #136 (t=12800, R_eq 4.07): none; #147 (t=12800, R_eq 4.11): none; #149 (t=12800, R_eq 4.18): none; #175 (t=12900, R_eq 4.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
