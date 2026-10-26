# Evidence pack: active-nematic-cargo (seed 22)

- world: `../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 575s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/c39-audit-wip/res15/seed22 --seeds 22 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8254, 0.6136], min area 6 px

## Measurements
- components: final 32, mean 19.4, max 32; occupancy final 0.07
- tracks: 78; persistent (alive >= 50% of run): 5; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 31], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.136/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 100, default): splits 30, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.233, nucleations 11
- channel total drift (end/start - 1): [-0.5109, -0.3922, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 83: holes 0, rim-vs-core 0.65, rim-vs-outside 0.26, heterogeneity 0.21; core [0.917, 0.852, 0.409, 0.458] rim [0.722, 0.584, 0.739, 0.014]
  - track 27 at frame 84: holes 0, rim-vs-core 0.68, rim-vs-outside 0.24, heterogeneity 0.22; core [0.913, 0.858, 0.433, 0.464] rim [0.709, 0.573, 0.803, 0.01]
  - track 17 at frame 68: holes 0, rim-vs-core 0.72, rim-vs-outside 0.25, heterogeneity 0.24; core [0.921, 0.914, 0.426, 0.442] rim [0.69, 0.603, 0.854, 0.005]
  - track 41 at frame 94: holes 0, rim-vs-core 0.62, rim-vs-outside 0.25, heterogeneity 0.21; core [0.906, 0.834, 0.426, 0.427] rim [0.706, 0.561, 0.746, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 4.59 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.752)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.735, rim/outside 7.85 (aggregate of 135 individuals; 1/135 membrane-like individually; rim level 0.6)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 3.04 (aggregate of 135 individuals; 97/135 membrane-like individually; rim level 0.568)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.254, rim/outside 1.96 (aggregate of 135 individuals; 14/135 membrane-like individually; rim level 0.156)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #25 (t=415, R_eq 5.05): ['surfactant s']; #27 (t=420, R_eq 5.01): ['surfactant s']; #17 (t=340, R_eq 5.44): ['surfactant s']; #41 (t=470, R_eq 5.29): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 135 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
