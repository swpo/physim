# Evidence pack: active-nematic-marangoni (seed 72)

- world: `../../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 385s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/c49rev5/runs/mar60/seed72 --seeds 72 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.8271, 0.5264], min area 6 px

## Measurements
- components: final 29, mean 21.0, max 35; occupancy final 0.09
- tracks: 126; persistent (alive >= 50% of run): 3; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 29], H1 [0, 0, 0]
- motion: 67 long-lived tracks moved >= 1 body length; max speed 0.293/time; max body lengths 7.8
- replication (lineage window K = 20 frames = time 100, default): splits 51, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 4, merges 19, merge/split ratio 0.373, nucleations 5
- channel total drift (end/start - 1): [-0.5073, -0.564, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 124: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.15; core [0.946, 0.796, 0.487, 0.0] rim [0.752, 0.432, 0.92, 0.0]
  - track 21 at frame 104: holes 0, rim-vs-core 0.52, rim-vs-outside 0.33, heterogeneity 0.13; core [0.965, 0.649, 0.435, 0.0] rim [0.776, 0.394, 0.851, 0.0]
  - track 47 at frame 148: holes 0, rim-vs-core 0.55, rim-vs-outside 0.31, heterogeneity 0.14; core [0.97, 0.57, 0.423, 0.0] rim [0.774, 0.342, 0.882, 0.0]
  - track 71 at frame 161: holes 0, rim-vs-core 0.45, rim-vs-outside 0.43, heterogeneity 0.14; core [0.94, 0.901, 0.474, 0.0] rim [0.782, 0.603, 0.766, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 140 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 4.46 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.725)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 8.83 (aggregate of 140 individuals; 14/140 membrane-like individually; rim level 0.521)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.38 (aggregate of 140 individuals; 52/140 membrane-like individually; rim level 0.655)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 140 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=620, R_eq 3.19): ['surfactant s']; #21 (t=520, R_eq 3.87): none; #47 (t=740, R_eq 4.15): ['order |Q|']; #71 (t=805, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 140 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
