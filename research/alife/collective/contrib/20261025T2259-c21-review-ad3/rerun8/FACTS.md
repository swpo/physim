# Evidence pack: ad3-membrane (seed 8)

- world: `../../../../threads/active-droplets/worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 194s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out collective/contrib/20261025T2259-c21-review-ad3/rerun8 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0509, 1.2307], min area 6 px

## Measurements
- components: final 16, mean 9.6, max 16; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 8; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.47 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0028/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1738, -0.6306, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 133: holes 0, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.15; core [0.979, 0.02, 0.167] rim [0.755, 0.078, 0.586]
  - track 8 at frame 133: holes 0, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.15; core [0.979, 0.02, 0.167] rim [0.754, 0.078, 0.59]
  - track 14 at frame 141: holes 0, rim-vs-core 0.49, rim-vs-outside 0.56, heterogeneity 0.15; core [0.967, 0.017, 0.181] rim [0.747, 0.081, 0.613]
  - track 22 at frame 158: holes 0, rim-vs-core 0.64, rim-vs-outside 0.37, heterogeneity 0.16; core [0.94, 0.043, 0.228] rim [0.619, 0.091, 0.776]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 35.5 (aggregate of 66 individuals; 2/66 membrane-like individually; rim level 0.892)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.19, rim/outside 0.675 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.156)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.96, rim/outside 12 (aggregate of 66 individuals; 64/66 membrane-like individually; rim level 0.733)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #7 (t=13300, R_eq 6.46): ['psi (amphiphile)']; #8 (t=13300, R_eq 6.43): ['psi (amphiphile)']; #14 (t=14100, R_eq 7.11): ['psi (amphiphile)']; #22 (t=15800, R_eq 5.7): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 66 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
