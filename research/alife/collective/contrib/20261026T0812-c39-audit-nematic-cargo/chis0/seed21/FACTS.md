# Evidence pack: active-nematic-cargo (seed 21)

- world: `../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 388s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/c39-audit-wip/chis0/seed21 --seeds 21 --no-movie`
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
  - track 19 at frame 119: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.09; core [0.946, 0.893, 0.841, 0.101] rim [0.807, 0.705, 0.756, 0.123]
  - track 12 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.36, heterogeneity 0.10; core [0.93, 0.876, 0.797, 0.11] rim [0.728, 0.586, 0.678, 0.139]
  - track 25 at frame 129: holes 0, rim-vs-core 0.28, rim-vs-outside 0.34, heterogeneity 0.08; core [0.901, 0.68, 0.952, 0.1] rim [0.731, 0.494, 0.832, 0.122]
  - track 95 at frame 187: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.10; core [0.935, 0.888, 0.808, 0.099] rim [0.738, 0.612, 0.688, 0.124]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 141 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.66 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.745)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 7.94 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.635)
  - radial surfactant s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 2.15 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.775)
  - radial cargo c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.38, rim/outside 0.679 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.256)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=595, R_eq 3.19): none; #12 (t=505, R_eq 3.19): none; #25 (t=645, R_eq 4.26): none; #95 (t=935, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 141 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
