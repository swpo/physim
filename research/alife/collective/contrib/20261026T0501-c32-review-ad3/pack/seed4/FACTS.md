# Evidence pack: ad3-membrane (seed 4)

- world: `../../world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 138s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0501-c32-review-ad3/world.py --out collective/contrib/20261026T0501-c32-review-ad3/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0494, 1.2328], min area 6 px

## Measurements
- components: final 16, mean 10.3, max 16; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 4; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.32 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00232/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1708, -0.6243, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 141: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.15; core [0.951, 0.037, 0.204] rim [0.759, 0.074, 0.558]
  - track 13 at frame 141: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.15; core [0.948, 0.039, 0.211] rim [0.662, 0.088, 0.731]
  - track 14 at frame 141: holes 0, rim-vs-core 0.63, rim-vs-outside 0.36, heterogeneity 0.16; core [0.939, 0.041, 0.23] rim [0.624, 0.091, 0.771]
  - track 18 at frame 153: holes 0, rim-vs-core 0.51, rim-vs-outside 0.55, heterogeneity 0.16; core [0.962, 0.018, 0.187] rim [0.727, 0.085, 0.64]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 35.5 (aggregate of 66 individuals; 2/66 membrane-like individually; rim level 0.868)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.11, rim/outside 0.673 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.154)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.55, rim/outside 11.3 (aggregate of 66 individuals; 59/66 membrane-like individually; rim level 0.685)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #10 (t=14100, R_eq 5.64): ['psi (amphiphile)']; #13 (t=14100, R_eq 5.67): ['psi (amphiphile)']; #14 (t=14100, R_eq 5.81): ['psi (amphiphile)']; #18 (t=15300, R_eq 7.25): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 66 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
