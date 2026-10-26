# Evidence pack: active-nematic-marangoni (seed 62)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 561s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/minority/scout/seed62 --seeds 62 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8393, 0.571], min area 6 px

## Measurements
- components: final 29, mean 22.0, max 32; occupancy final 0.10
- tracks: 115; persistent (alive >= 50% of run): 12; longest 159 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 29], H1 [0, 0, 0]
- motion: 62 long-lived tracks moved >= 1 body length; max speed 0.32/time; max body lengths 10.9
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 5, merges 21, merge/split ratio 0.488, nucleations 7
- channel total drift (end/start - 1): [-0.4953, -0.4344, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 121: holes 0, rim-vs-core 0.57, rim-vs-outside 0.41, heterogeneity 0.22; core [0.96, 0.789, 0.357, 0.448] rim [0.799, 0.543, 0.721, 0.117]
  - track 27 at frame 123: holes 0, rim-vs-core 0.68, rim-vs-outside 0.39, heterogeneity 0.24; core [0.945, 0.727, 0.428, 0.486] rim [0.772, 0.435, 0.853, 0.081]
  - track 28 at frame 123: holes 0, rim-vs-core 0.64, rim-vs-outside 0.32, heterogeneity 0.21; core [0.929, 0.671, 0.442, 0.388] rim [0.742, 0.445, 0.866, 0.012]
  - track 95 at frame 180: holes 0, rim-vs-core 0.75, rim-vs-outside 0.32, heterogeneity 0.23; core [0.956, 0.668, 0.391, 0.486] rim [0.756, 0.403, 0.876, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 145 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.5 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.696)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 8.24 (aggregate of 145 individuals; 15/145 membrane-like individually; rim level 0.51)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.23 (aggregate of 145 individuals; 63/145 membrane-like individually; rim level 0.576)
  - radial cargo c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 2 (aggregate of 145 individuals; 28/145 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=605, R_eq 3.83): ['surfactant s']; #27 (t=615, R_eq 4.11): ['surfactant s']; #28 (t=615, R_eq 4.55): none; #95 (t=900, R_eq 4.15): none

## Warnings
- radial: 8 of 145 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
