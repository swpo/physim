# Evidence pack: active-nematic-marangoni-two-kinds (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 449s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0630-c34-marangoni-two-kinds/world.py --out collective/contrib/20261026T0630-c34-marangoni-two-kinds/sel_s12 --seeds 1 2 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8371, 0.6103], min area 6 px

## Measurements
- components: final 28, mean 17.4, max 29; occupancy final 0.09
- tracks: 83; persistent (alive >= 50% of run): 8; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 27, 26], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.415/time; max body lengths 6.3
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 5, merges 9, merge/split ratio 0.257, nucleations 4
- channel total drift (end/start - 1): [-0.4928, -0.3945, 17.6867, 0.5693]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 113: holes 0, rim-vs-core 0.44, rim-vs-outside 0.51, heterogeneity 0.17; core [0.972, 0.983, 0.03, 0.538] rim [0.781, 0.841, 0.065, 0.903]
  - track 19 at frame 136: holes 0, rim-vs-core 0.51, rim-vs-outside 0.31, heterogeneity 0.15; core [0.943, 0.527, 0.478, 0.004] rim [0.744, 0.385, 0.927, 0.009]
  - track 26 at frame 145: holes 0, rim-vs-core 0.56, rim-vs-outside 0.32, heterogeneity 0.14; core [0.95, 0.702, 0.416, 0.007] rim [0.748, 0.436, 0.871, 0.016]
  - track 40 at frame 156: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.14; core [0.95, 0.678, 0.43, 0.001] rim [0.747, 0.425, 0.91, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 4.41 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.687)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 8.04 (aggregate of 115 individuals; 18/115 membrane-like individually; rim level 0.524)
  - radial surfactant A: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 3.16 (aggregate of 115 individuals; 46/115 membrane-like individually; rim level 0.52)
  - radial surfactant B: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 2.44 (aggregate of 115 individuals; 28/115 membrane-like individually; rim level 0.0939)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant B
- membrane-like channels per top track at mid-life: #4 (t=565, R_eq 4.69): ['surfactant B']; #19 (t=680, R_eq 4.85): ['order |Q|']; #26 (t=725, R_eq 3.99): none; #40 (t=780, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
