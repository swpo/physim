# Evidence pack: active-nematic-marangoni (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 409s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/twin_zeta0 --seeds 0 --no-movie`
- segmentation: matter > 0.52 of robust range [-0.8623, 0.7914], min area 6 px

## Measurements
- components: final 15, mean 11.9, max 17; occupancy final 0.12
- tracks: 50; persistent (alive >= 50% of run): 7; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 36.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 15, 15], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.155/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.667, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.0426, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 111: holes 0, rim-vs-core 1.10, rim-vs-outside 0.61, heterogeneity 0.19; core [0.993, 0.931, 0.111, 1.0] rim [0.808, 0.593, 0.616, 0.104]
  - track 13 at frame 138: holes 0, rim-vs-core 0.74, rim-vs-outside 0.37, heterogeneity 0.23; core [0.945, 0.853, 0.332, 0.417] rim [0.744, 0.554, 0.831, 0.004]
  - track 18 at frame 150: holes 0, rim-vs-core 0.69, rim-vs-outside 0.39, heterogeneity 0.22; core [0.936, 0.849, 0.34, 0.401] rim [0.741, 0.584, 0.798, 0.002]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.668, rim/outside 3.6 (aggregate of 78 individuals; 2/78 membrane-like individually; rim level 0.542)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.666, rim/outside 5.25 (aggregate of 78 individuals; 2/78 membrane-like individually; rim level 0.436)
  - radial surfactant s: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 3 (aggregate of 78 individuals; 29/78 membrane-like individually; rim level 0.424)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.355, rim/outside 1.94 (aggregate of 78 individuals; 6/78 membrane-like individually; rim level 0.0691)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 7.69): none; #6 (t=555, R_eq 6.86): none; #13 (t=690, R_eq 4.03): ['surfactant s']; #18 (t=750, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
