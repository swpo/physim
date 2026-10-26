# Evidence pack: active-nematic-marangoni-two-kinds (seed 20)

- world: `../../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 692s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/Aswims/s20 --seeds 20 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8382, 0.6717], min area 6 px

## Measurements
- components: final 30, mean 22.5, max 33; occupancy final 0.09
- tracks: 103; persistent (alive >= 50% of run): 14; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.90 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 30], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.218/time; max body lengths 7.4
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.293, nucleations 9
- channel total drift (end/start - 1): [-0.494, -0.2835, 10.707, 7.1829]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 128: holes 0, rim-vs-core 0.52, rim-vs-outside 0.37, heterogeneity 0.13; core [0.93, 0.892, 0.008, 0.332] rim [0.736, 0.609, 0.023, 0.716]
  - track 33 at frame 134: holes 0, rim-vs-core 0.51, rim-vs-outside 0.31, heterogeneity 0.13; core [0.902, 0.733, 0.438, 0.019] rim [0.721, 0.481, 0.845, 0.042]
  - track 34 at frame 134: holes 0, rim-vs-core 0.49, rim-vs-outside 0.38, heterogeneity 0.15; core [0.913, 0.779, 0.496, 0.023] rim [0.744, 0.533, 0.886, 0.052]
  - track 67 at frame 161: holes 0, rim-vs-core 0.57, rim-vs-outside 0.31, heterogeneity 0.15; core [0.938, 0.562, 0.401, 0.009] rim [0.747, 0.38, 0.905, 0.026]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.75 (aggregate of 150 individuals; 1/150 membrane-like individually; rim level 0.719)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 8.38 (aggregate of 150 individuals; 9/150 membrane-like individually; rim level 0.561)
  - radial surfactant A: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.06 (aggregate of 150 individuals; 83/150 membrane-like individually; rim level 0.335)
  - radial surfactant B: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 2.85 (aggregate of 150 individuals; 88/150 membrane-like individually; rim level 0.272)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant B
- membrane-like channels per top track at mid-life: #27 (t=640, R_eq 3.57): ['surfactant B']; #33 (t=670, R_eq 4.07): none; #34 (t=670, R_eq 4.85): none; #67 (t=805, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 150 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
