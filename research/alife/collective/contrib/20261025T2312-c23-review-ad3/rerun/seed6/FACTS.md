# Evidence pack: ad3-membrane (seed 6)

- world: `../../../../../../threads/active-droplets/worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 147s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out collective/contrib/20261025T2312-c23-review-ad3/rerun/seed6 --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0499, 1.2333], min area 6 px

## Measurements
- components: final 18, mean 11.4, max 18; occupancy final 0.12
- tracks: 34; persistent (alive >= 50% of run): 6; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.34 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00192/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1788, -0.6381, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 129: holes 0, rim-vs-core 0.62, rim-vs-outside 0.35, heterogeneity 0.16; core [0.94, 0.038, 0.228] rim [0.629, 0.087, 0.767]
  - track 13 at frame 129: holes 0, rim-vs-core 0.61, rim-vs-outside 0.34, heterogeneity 0.15; core [0.941, 0.038, 0.223] rim [0.637, 0.086, 0.752]
  - track 16 at frame 131: holes 0, rim-vs-core 0.62, rim-vs-outside 0.34, heterogeneity 0.15; core [0.94, 0.034, 0.232] rim [0.642, 0.086, 0.772]
  - track 26 at frame 166: holes 0, rim-vs-core 0.61, rim-vs-outside 0.33, heterogeneity 0.15; core [0.949, 0.033, 0.214] rim [0.668, 0.084, 0.748]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 40.7 (aggregate of 76 individuals; 2/76 membrane-like individually; rim level 0.886)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.01, rim/outside 0.67 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.146)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.1, rim/outside 12.4 (aggregate of 76 individuals; 72/76 membrane-like individually; rim level 0.756)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #11 (t=12900, R_eq 5.75): ['psi (amphiphile)']; #13 (t=12900, R_eq 5.73): ['psi (amphiphile)']; #16 (t=13100, R_eq 6): ['psi (amphiphile)']; #26 (t=16600, R_eq 5.89): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
