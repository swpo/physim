# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 344s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/mar60/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.8299, 0.5264], min area 6 px

## Measurements
- components: final 31, mean 22.8, max 33; occupancy final 0.09
- tracks: 118; persistent (alive >= 50% of run): 12; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.59 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 31], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.442/time; max body lengths 12.4
- replication (lineage window K = 20 frames = time 100, default): splits 46, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 18, merge/split ratio 0.391, nucleations 8
- channel total drift (end/start - 1): [-0.4979, -0.5428, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 126: holes 0, rim-vs-core 0.57, rim-vs-outside 0.38, heterogeneity 0.17; core [0.962, 0.754, 0.462, 0.0] rim [0.764, 0.493, 0.934, 0.0]
  - track 37 at frame 133: holes 0, rim-vs-core 0.55, rim-vs-outside 0.31, heterogeneity 0.14; core [0.936, 0.649, 0.516, 0.0] rim [0.717, 0.356, 0.933, 0.0]
  - track 36 at frame 129: holes 0, rim-vs-core 0.54, rim-vs-outside 0.33, heterogeneity 0.14; core [0.944, 0.69, 0.472, 0.0] rim [0.745, 0.409, 0.894, 0.0]
  - track 75 at frame 163: holes 0, rim-vs-core 0.58, rim-vs-outside 0.37, heterogeneity 0.15; core [0.945, 0.828, 0.427, 0.0] rim [0.736, 0.458, 0.826, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 153 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.46 (aggregate of 153 individuals; 1/153 membrane-like individually; rim level 0.726)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 8.75 (aggregate of 153 individuals; 14/153 membrane-like individually; rim level 0.507)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.32 (aggregate of 153 individuals; 55/153 membrane-like individually; rim level 0.638)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 153 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #29 (t=630, R_eq 4.33): none; #37 (t=665, R_eq 3.78): ['surfactant s']; #36 (t=645, R_eq 3.83): none; #75 (t=815, R_eq 3.34): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 153 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
