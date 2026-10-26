# Evidence pack: active-nematic-marangoni (seed 17)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 625s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0830-c38-audit-marangoni/rerun/mar0_seed17 --seeds 17 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8234, 0.6252], min area 6 px

## Measurements
- components: final 29, mean 23.2, max 33; occupancy final 0.06
- tracks: 112; persistent (alive >= 50% of run): 10; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 28], H1 [1, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.0955/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 15, merge/split ratio 0.349, nucleations 11
- channel total drift (end/start - 1): [-0.5019, -0.4313, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 108: holes 0, rim-vs-core 0.72, rim-vs-outside 0.37, heterogeneity 0.22; core [0.943, 0.887, 0.32, 0.464] rim [0.72, 0.575, 0.723, 0.01]
  - track 20 at frame 116: holes 0, rim-vs-core 0.50, rim-vs-outside 0.39, heterogeneity 0.19; core [0.921, 0.849, 0.362, 0.39] rim [0.762, 0.599, 0.616, 0.082]
  - track 11 at frame 97: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.17; core [0.933, 0.838, 0.272, 0.355] rim [0.749, 0.579, 0.558, 0.017]
  - track 67 at frame 156: holes 0, rim-vs-core 0.62, rim-vs-outside 0.33, heterogeneity 0.20; core [0.938, 0.86, 0.289, 0.394] rim [0.722, 0.557, 0.611, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 154 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.79 (aggregate of 154 individuals; 0/154 membrane-like individually; rim level 0.756)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 8.12 (aggregate of 154 individuals; 1/154 membrane-like individually; rim level 0.638)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 2.96 (aggregate of 154 individuals; 128/154 membrane-like individually; rim level 0.565)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.227, rim/outside 1.61 (aggregate of 154 individuals; 12/154 membrane-like individually; rim level 0.127)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #5 (t=540, R_eq 3.04): ['surfactant s']; #20 (t=580, R_eq 3.43): ['surfactant s']; #11 (t=485, R_eq 2.93): ['surfactant s']; #67 (t=780, R_eq 2.93): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 154 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
