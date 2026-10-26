# Evidence pack: active-nematic-cargo (seed 21)

- world: `../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 393s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/c39-audit-wip/rerun/seed21 --seeds 21 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.827, 0.633], min area 6 px

## Measurements
- components: final 30, mean 21.0, max 31; occupancy final 0.07
- tracks: 111; persistent (alive >= 50% of run): 8; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 28], H1 [0, 0, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.102/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 14, merge/split ratio 0.326, nucleations 11
- channel total drift (end/start - 1): [-0.5032, -0.4019, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 119: holes 0, rim-vs-core 0.52, rim-vs-outside 0.47, heterogeneity 0.20; core [0.946, 0.893, 0.284, 0.516] rim [0.807, 0.705, 0.555, 0.134]
  - track 12 at frame 101: holes 0, rim-vs-core 0.63, rim-vs-outside 0.32, heterogeneity 0.20; core [0.93, 0.876, 0.314, 0.421] rim [0.728, 0.586, 0.64, 0.014]
  - track 25 at frame 129: holes 0, rim-vs-core 0.56, rim-vs-outside 0.31, heterogeneity 0.18; core [0.901, 0.68, 0.463, 0.391] rim [0.731, 0.494, 0.796, 0.017]
  - track 95 at frame 187: holes 0, rim-vs-core 0.62, rim-vs-outside 0.37, heterogeneity 0.21; core [0.935, 0.888, 0.318, 0.435] rim [0.738, 0.612, 0.629, 0.025]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 141 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.66 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.745)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 7.94 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.635)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.63, rim/outside 2.91 (aggregate of 141 individuals; 106/141 membrane-like individually; rim level 0.562)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.238, rim/outside 1.63 (aggregate of 141 individuals; 16/141 membrane-like individually; rim level 0.13)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #19 (t=595, R_eq 3.19): ['surfactant s']; #12 (t=505, R_eq 3.19): ['surfactant s']; #25 (t=645, R_eq 4.26): ['cargo c']; #95 (t=935, R_eq 3.29): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 141 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
