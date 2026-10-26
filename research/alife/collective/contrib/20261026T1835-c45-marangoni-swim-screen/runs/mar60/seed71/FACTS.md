# Evidence pack: active-nematic-marangoni (seed 71)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 357s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/mar60/seed71 --seeds 71 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.8293, 0.526], min area 6 px

## Measurements
- components: final 28, mean 20.1, max 30; occupancy final 0.09
- tracks: 149; persistent (alive >= 50% of run): 7; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 26], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.341/time; max body lengths 13.9
- replication (lineage window K = 20 frames = time 100, default): splits 58, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 5, merges 28, merge/split ratio 0.483, nucleations 5
- channel total drift (end/start - 1): [-0.4969, -0.5324, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 119: holes 0, rim-vs-core 0.53, rim-vs-outside 0.32, heterogeneity 0.15; core [0.957, 0.618, 0.482, 0.0] rim [0.763, 0.375, 0.916, 0.0]
  - track 27 at frame 129: holes 0, rim-vs-core 0.48, rim-vs-outside 0.31, heterogeneity 0.15; core [0.945, 0.557, 0.498, 0.0] rim [0.745, 0.36, 0.882, 0.0]
  - track 31 at frame 123: holes 0, rim-vs-core 0.45, rim-vs-outside 0.30, heterogeneity 0.12; core [0.945, 0.51, 0.493, 0.0] rim [0.763, 0.329, 0.867, 0.0]
  - track 105 at frame 178: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.13; core [0.949, 0.846, 0.438, 0.0] rim [0.775, 0.524, 0.822, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.21 (aggregate of 133 individuals; 1/133 membrane-like individually; rim level 0.705)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 8.18 (aggregate of 133 individuals; 20/133 membrane-like individually; rim level 0.505)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 3.09 (aggregate of 133 individuals; 37/133 membrane-like individually; rim level 0.61)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 133 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=595, R_eq 4.11): none; #27 (t=645, R_eq 4.26): none; #31 (t=615, R_eq 4.41, ring): ['order |Q|']; #105 (t=890, R_eq 3.43): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
