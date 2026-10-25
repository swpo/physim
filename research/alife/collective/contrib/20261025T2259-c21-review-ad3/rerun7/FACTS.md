# Evidence pack: ad3-membrane (seed 7)

- world: `../../../../threads/active-droplets/worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 194s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out collective/contrib/20261025T2259-c21-review-ad3/rerun7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0508, 1.2328], min area 6 px

## Measurements
- components: final 18, mean 10.2, max 18; occupancy final 0.12
- tracks: 34; persistent (alive >= 50% of run): 8; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.77 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00163/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1791, -0.6389, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 139: holes 0, rim-vs-core 0.62, rim-vs-outside 0.32, heterogeneity 0.16; core [0.942, 0.036, 0.228] rim [0.639, 0.087, 0.766]
  - track 13 at frame 139: holes 0, rim-vs-core 0.62, rim-vs-outside 0.32, heterogeneity 0.15; core [0.943, 0.036, 0.224] rim [0.644, 0.087, 0.762]
  - track 14 at frame 143: holes 0, rim-vs-core 0.49, rim-vs-outside 0.54, heterogeneity 0.15; core [0.966, 0.017, 0.176] rim [0.745, 0.076, 0.606]
  - track 30 at frame 176: holes 0, rim-vs-core 0.56, rim-vs-outside 0.31, heterogeneity 0.14; core [0.948, 0.04, 0.208] rim [0.674, 0.084, 0.697]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 38.4 (aggregate of 70 individuals; 2/70 membrane-like individually; rim level 0.879)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.56, rim/outside 0.675 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.15)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.82, rim/outside 11.8 (aggregate of 70 individuals; 64/70 membrane-like individually; rim level 0.717)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #11 (t=13900, R_eq 5.94): ['psi (amphiphile)']; #13 (t=13900, R_eq 5.92): ['psi (amphiphile)']; #14 (t=14300, R_eq 6.79): ['psi (amphiphile)']; #30 (t=17600, R_eq 5.41): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
