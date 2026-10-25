# Evidence pack: active-nematic-droplets-audit-source-split3 (seed 9)

- world: `../world_srcsplit3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 500s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2125-c21-review-c11-ring-source/world_srcsplit3.py --out collective/contrib/20261025T2125-c21-review-c11-ring-source/fresh9 --seeds 9 --no-movie`
- segmentation: matter > 0.53 of robust range [-0.8226, 0.7411], min area 6 px

## Measurements
- components: final 30, mean 19.5, max 30; occupancy final 0.07
- tracks: 95; persistent (alive >= 50% of run): 8; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 29], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.0708/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.211, nucleations 11
- channel total drift (end/start - 1): [-0.498, -0.3891, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 118: holes 0, rim-vs-core 0.54, rim-vs-outside 0.36, heterogeneity 0.15; core [0.923, 0.837, 0.465, 0.312, 0.421] rim [0.724, 0.568, 0.647, 0.552, 0.727]
  - track 27 at frame 128: holes 0, rim-vs-core 0.74, rim-vs-outside 0.42, heterogeneity 0.21; core [0.987, 0.877, 0.658, 0.182, 0.256] rim [0.756, 0.651, 1.0, 0.52, 0.721]
  - track 31 at frame 134: holes 0, rim-vs-core 0.66, rim-vs-outside 0.37, heterogeneity 0.17; core [0.947, 0.9, 0.415, 0.31, 0.444] rim [0.727, 0.591, 0.638, 0.596, 0.839]
  - track 63 at frame 175: holes 0, rim-vs-core 0.53, rim-vs-outside 0.35, heterogeneity 0.14; core [0.914, 0.859, 0.501, 0.302, 0.422] rim [0.724, 0.586, 0.687, 0.523, 0.714]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 4.92 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.755)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.44 (aggregate of 131 individuals; 1/131 membrane-like individually; rim level 0.62)
  - radial s rod-made (phi>0): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 2.81 (aggregate of 131 individuals; 69/131 membrane-like individually; rim level 0.624)
  - radial s interface-made (-0.5<phi<=0): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 1.95 (aggregate of 131 individuals; 97/131 membrane-like individually; rim level 0.489)  MEMBRANE-LIKE
  - radial s far-bath-made (phi<=-0.5): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 1.45 (aggregate of 131 individuals; 69/131 membrane-like individually; rim level 0.629)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s interface-made (-0.5<phi<=0)
- membrane-like channels per top track at mid-life: #19 (t=590, R_eq 2.99): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #27 (t=640, R_eq 5.29): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #31 (t=670, R_eq 2.99): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #63 (t=875, R_eq 3.52): ['s interface-made (-0.5<phi<=0)']

## Warnings
- radial: 3 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
