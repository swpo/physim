# Evidence pack: active-nematic-marangoni (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 421s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/ablate_kappa0 --seeds 0 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8411, 0.5767], min area 6 px

## Measurements
- components: final 29, mean 22.0, max 31; occupancy final 0.10
- tracks: 89; persistent (alive >= 50% of run): 16; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 29, 29], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.385/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 12, merge/split ratio 0.353, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.4128, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 114: holes 0, rim-vs-core 0.69, rim-vs-outside 0.36, heterogeneity 0.20; core [0.971, 0.762, 0.33, 0.902] rim [0.779, 0.476, 0.922, 0.857]
  - track 14 at frame 113: holes 0, rim-vs-core 0.57, rim-vs-outside 0.32, heterogeneity 0.14; core [0.955, 0.675, 0.401, 0.849] rim [0.761, 0.436, 0.877, 0.806]
  - track 23 at frame 124: holes 0, rim-vs-core 0.64, rim-vs-outside 0.33, heterogeneity 0.18; core [0.957, 0.619, 0.412, 0.934] rim [0.729, 0.359, 0.949, 0.88]
  - track 35 at frame 139: holes 0, rim-vs-core 0.60, rim-vs-outside 0.35, heterogeneity 0.15; core [0.947, 0.837, 0.425, 0.92] rim [0.75, 0.52, 0.889, 0.881]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.57 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.706)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 8.93 (aggregate of 148 individuals; 10/148 membrane-like individually; rim level 0.546)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.2 (aggregate of 148 individuals; 60/148 membrane-like individually; rim level 0.582)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 1.27 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.778)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=570, R_eq 4.3): none; #14 (t=565, R_eq 3.99): none; #23 (t=620, R_eq 4.37): none; #35 (t=695, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 148 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
