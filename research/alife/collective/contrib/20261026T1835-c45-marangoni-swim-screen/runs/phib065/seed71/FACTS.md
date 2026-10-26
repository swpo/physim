# Evidence pack: active-nematic-marangoni (seed 71)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 365s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/phib065/seed71 --seeds 71 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8031, 0.5265], min area 6 px

## Measurements
- components: final 13, mean 5.4, max 13; occupancy final 0.03
- tracks: 24; persistent (alive >= 50% of run): 2; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.34 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 12], H1 [1, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.327/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.6216, -0.7532, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 139: holes 0, rim-vs-core 0.60, rim-vs-outside 0.39, heterogeneity 0.15; core [0.989, 0.883, 0.518, 0.0] rim [0.804, 0.56, 0.988, 0.0]
  - track 6 at frame 129: holes 0, rim-vs-core 0.54, rim-vs-outside 0.43, heterogeneity 0.14; core [0.991, 0.957, 0.467, 0.0] rim [0.824, 0.679, 0.897, 0.0]
  - track 4 at frame 123: holes 0, rim-vs-core 0.54, rim-vs-outside 0.37, heterogeneity 0.16; core [0.982, 0.763, 0.548, 0.0] rim [0.779, 0.514, 0.987, 0.0]
  - track 18 at frame 190: holes 0, rim-vs-core 0.59, rim-vs-outside 0.45, heterogeneity 0.15; core [0.986, 0.966, 0.467, 0.0] rim [0.785, 0.7, 0.958, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 37 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 4.73 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.734)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 7.93 (aggregate of 37 individuals; 1/37 membrane-like individually; rim level 0.666)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.23 (aggregate of 37 individuals; 20/37 membrane-like individually; rim level 0.667)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 37 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=695, R_eq 4.15): none; #6 (t=645, R_eq 3.99): none; #4 (t=615, R_eq 4.48): none; #18 (t=950, R_eq 3.57): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
