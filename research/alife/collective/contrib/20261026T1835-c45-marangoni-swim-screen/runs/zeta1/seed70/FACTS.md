# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 348s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/zeta1/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.834, 0.5827], min area 6 px

## Measurements
- components: final 30, mean 22.2, max 31; occupancy final 0.09
- tracks: 85; persistent (alive >= 50% of run): 20; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.23/time; max body lengths 13.3
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 5, merges 8, merge/split ratio 0.229, nucleations 7
- channel total drift (end/start - 1): [-0.4979, -0.4575, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 124: holes 0, rim-vs-core 0.63, rim-vs-outside 0.37, heterogeneity 0.15; core [0.962, 0.851, 0.322, 0.0] rim [0.772, 0.486, 0.803, 0.0]
  - track 22 at frame 124: holes 0, rim-vs-core 0.56, rim-vs-outside 0.40, heterogeneity 0.14; core [0.931, 0.901, 0.426, 0.0] rim [0.746, 0.604, 0.857, 0.0]
  - track 28 at frame 128: holes 0, rim-vs-core 0.64, rim-vs-outside 0.38, heterogeneity 0.14; core [0.966, 0.87, 0.283, 0.0] rim [0.767, 0.479, 0.75, 0.0]
  - track 81 at frame 178: holes 0, rim-vs-core 0.53, rim-vs-outside 0.40, heterogeneity 0.14; core [0.939, 0.895, 0.347, 0.0] rim [0.734, 0.573, 0.721, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.64 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.72)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 9.09 (aggregate of 152 individuals; 12/152 membrane-like individually; rim level 0.551)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.19 (aggregate of 152 individuals; 68/152 membrane-like individually; rim level 0.581)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 152 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=620, R_eq 2.88): ['surfactant s']; #22 (t=620, R_eq 4.11): none; #28 (t=640, R_eq 2.76): ['surfactant s']; #81 (t=890, R_eq 3.57): ['surfactant s']

## Warnings
- radial: 3 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
