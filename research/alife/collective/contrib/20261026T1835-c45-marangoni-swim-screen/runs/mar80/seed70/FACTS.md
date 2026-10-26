# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 361s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/mar80/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.8187, 0.5025], min area 6 px

## Measurements
- components: final 31, mean 22.0, max 31; occupancy final 0.08
- tracks: 151; persistent (alive >= 50% of run): 6; longest 151 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 0.515/time; max body lengths 23.5
- replication (lineage window K = 20 frames = time 100, default): splits 57, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 5, merges 27, merge/split ratio 0.474, nucleations 11
- channel total drift (end/start - 1): [-0.4979, -0.6249, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 126: holes 0, rim-vs-core 0.47, rim-vs-outside 0.29, heterogeneity 0.14; core [0.944, 0.599, 0.55, 0.0] rim [0.771, 0.363, 0.918, 0.0]
  - track 26 at frame 126: holes 0, rim-vs-core 0.60, rim-vs-outside 0.39, heterogeneity 0.15; core [0.977, 0.874, 0.506, 0.0] rim [0.797, 0.489, 0.925, 0.0]
  - track 34 at frame 128: holes 0, rim-vs-core 0.44, rim-vs-outside 0.28, heterogeneity 0.11; core [0.934, 0.418, 0.583, 0.0] rim [0.741, 0.248, 0.937, 0.0]
  - track 139 at frame 183: holes 0, rim-vs-core 0.47, rim-vs-outside 0.29, heterogeneity 0.13; core [0.95, 0.43, 0.555, 0.0] rim [0.756, 0.259, 0.946, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 4.31 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.738)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 8.14 (aggregate of 146 individuals; 20/146 membrane-like individually; rim level 0.489)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 3.27 (aggregate of 146 individuals; 45/146 membrane-like individually; rim level 0.665)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 146 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=630, R_eq 3.57): none; #26 (t=630, R_eq 3.19): ['surfactant s']; #34 (t=640, R_eq 4.03): ['order |Q|']; #139 (t=915, R_eq 4.18): ['order |Q|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
