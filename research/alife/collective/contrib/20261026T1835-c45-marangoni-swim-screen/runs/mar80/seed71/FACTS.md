# Evidence pack: active-nematic-marangoni (seed 71)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 355s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/mar80/seed71 --seeds 71 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.816, 0.5026], min area 6 px

## Measurements
- components: final 27, mean 20.9, max 31; occupancy final 0.08
- tracks: 162; persistent (alive >= 50% of run): 9; longest 127 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 27, 27], H1 [0, 0, 0]
- motion: 64 long-lived tracks moved >= 1 body length; max speed 0.469/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 100, default): splits 60, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 5, merges 32, merge/split ratio 0.533, nucleations 11
- channel total drift (end/start - 1): [-0.4969, -0.6556, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 106: holes 0, rim-vs-core 0.25, rim-vs-outside 0.21, heterogeneity 0.09; core [0.871, 0.324, 0.636, 0.0] rim [0.748, 0.347, 0.853, 0.0]
  - track 64 at frame 138: holes 0, rim-vs-core 0.50, rim-vs-outside 0.38, heterogeneity 0.14; core [0.953, 0.895, 0.486, 0.0] rim [0.778, 0.591, 0.844, 0.0]
  - track 69 at frame 138: holes 0, rim-vs-core 0.50, rim-vs-outside 0.32, heterogeneity 0.13; core [0.97, 0.576, 0.453, 0.0] rim [0.776, 0.342, 0.853, 0.0]
  - track 71 at frame 139: holes 0, rim-vs-core 0.41, rim-vs-outside 0.26, heterogeneity 0.13; core [0.946, 0.469, 0.55, 0.0] rim [0.767, 0.292, 0.869, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 138 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 4.23 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.73)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 8.04 (aggregate of 138 individuals; 26/138 membrane-like individually; rim level 0.501)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 3.12 (aggregate of 138 individuals; 30/138 membrane-like individually; rim level 0.657)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 138 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=530, R_eq 4.11, ring): ['order |Q|']; #64 (t=690, R_eq 3.7): none; #69 (t=690, R_eq 3.87): none; #71 (t=695, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 138 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
