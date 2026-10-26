# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 397s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/gm2/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.8091, 0.5051], min area 6 px

## Measurements
- components: final 31, mean 21.8, max 31; occupancy final 0.08
- tracks: 85; persistent (alive >= 50% of run): 23; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 30], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.241/time; max body lengths 8.5
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 10, merge/split ratio 0.294, nucleations 7
- channel total drift (end/start - 1): [-0.4979, -0.5552, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 119: holes 0, rim-vs-core 0.61, rim-vs-outside 0.37, heterogeneity 0.14; core [0.976, 0.912, 0.398, 0.0] rim [0.758, 0.52, 0.812, 0.0]
  - track 16 at frame 119: holes 0, rim-vs-core 0.54, rim-vs-outside 0.40, heterogeneity 0.14; core [0.965, 0.907, 0.489, 0.0] rim [0.781, 0.632, 0.909, 0.0]
  - track 21 at frame 128: holes 0, rim-vs-core 0.44, rim-vs-outside 0.29, heterogeneity 0.14; core [0.929, 0.55, 0.586, 0.0] rim [0.756, 0.344, 0.94, 0.0]
  - track 42 at frame 141: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.10; core [0.94, 0.584, 0.537, 0.0] rim [0.763, 0.397, 0.867, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 4.45 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.758)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 9.05 (aggregate of 149 individuals; 3/149 membrane-like individually; rim level 0.603)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.33 (aggregate of 149 individuals; 76/149 membrane-like individually; rim level 0.678)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 149 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=595, R_eq 2.93): ['surfactant s']; #16 (t=595, R_eq 3.52): ['surfactant s']; #21 (t=640, R_eq 4.41): none; #42 (t=705, R_eq 3.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 149 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
