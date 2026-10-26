# Evidence pack: active-nematic-marangoni (seed 9)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 595s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev9/m0_s9 --seeds 9 --frames 200 --no-movie`
- segmentation: matter > 0.53 of robust range [-0.8226, 0.7411], min area 6 px

## Measurements
- components: final 30, mean 19.5, max 30; occupancy final 0.07
- tracks: 95; persistent (alive >= 50% of run): 8; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 29], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.0708/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.211, nucleations 11
- channel total drift (end/start - 1): [-0.498, -0.3891, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 118: holes 0, rim-vs-core 0.65, rim-vs-outside 0.35, heterogeneity 0.20; core [0.923, 0.837, 0.296, 0.503] rim [0.724, 0.568, 0.594, 0.03]
  - track 27 at frame 128: holes 0, rim-vs-core 0.84, rim-vs-outside 0.42, heterogeneity 0.28; core [0.987, 0.877, 0.401, 0.506] rim [0.756, 0.651, 1.0, 0.016]
  - track 31 at frame 134: holes 0, rim-vs-core 0.66, rim-vs-outside 0.37, heterogeneity 0.21; core [0.947, 0.9, 0.244, 0.433] rim [0.727, 0.591, 0.585, 0.013]
  - track 63 at frame 175: holes 0, rim-vs-core 0.66, rim-vs-outside 0.33, heterogeneity 0.20; core [0.914, 0.859, 0.301, 0.514] rim [0.724, 0.586, 0.588, 0.021]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 4.92 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.755)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.44 (aggregate of 131 individuals; 1/131 membrane-like individually; rim level 0.62)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 3.07 (aggregate of 131 individuals; 100/131 membrane-like individually; rim level 0.515)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.293, rim/outside 1.86 (aggregate of 131 individuals; 18/131 membrane-like individually; rim level 0.157)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #19 (t=590, R_eq 2.99): ['surfactant s']; #27 (t=640, R_eq 5.29): ['surfactant s']; #31 (t=670, R_eq 2.99): ['surfactant s']; #63 (t=875, R_eq 3.52): ['surfactant s']

## Warnings
- radial: 3 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
