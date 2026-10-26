# Evidence pack: active-nematic-cargo (seed 15)

- world: `../../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 640s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/wip-c37/cargo/ctl_kappa0/seed15 --seeds 15 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8253, 0.619], min area 6 px

## Measurements
- components: final 29, mean 18.3, max 29; occupancy final 0.06
- tracks: 87; persistent (alive >= 50% of run): 11; longest 136 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 28], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.079/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.229, nucleations 9
- channel total drift (end/start - 1): [-0.5049, -0.413, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 133: holes 0, rim-vs-core 0.41, rim-vs-outside 0.30, heterogeneity 0.11; core [0.901, 0.752, 0.386, 0.931] rim [0.719, 0.51, 0.664, 0.886]
  - track 26 at frame 133: holes 0, rim-vs-core 0.46, rim-vs-outside 0.37, heterogeneity 0.13; core [0.928, 0.842, 0.384, 0.852] rim [0.739, 0.584, 0.713, 0.802]
  - track 33 at frame 139: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.14; core [0.938, 0.77, 0.395, 0.875] rim [0.714, 0.49, 0.812, 0.833]
  - track 60 at frame 175: holes 0, rim-vs-core 0.51, rim-vs-outside 0.33, heterogeneity 0.13; core [0.949, 0.895, 0.302, 0.879] rim [0.743, 0.6, 0.663, 0.835]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 127 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.73 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.762)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.02 (aggregate of 127 individuals; 1/127 membrane-like individually; rim level 0.639)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 2.98 (aggregate of 127 individuals; 102/127 membrane-like individually; rim level 0.591)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 1.29 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.822)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #25 (t=665, R_eq 3.14): ['surfactant s']; #26 (t=665, R_eq 3.57): ['surfactant s']; #33 (t=695, R_eq 2.76): ['surfactant s']; #60 (t=875, R_eq 2.99): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 127 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
