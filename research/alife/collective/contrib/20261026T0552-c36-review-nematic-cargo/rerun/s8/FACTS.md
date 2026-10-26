# Evidence pack: active-nematic-cargo (seed 8)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 578s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev7/s8 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8255, 0.6215], min area 6 px

## Measurements
- components: final 35, mean 23.6, max 35; occupancy final 0.07
- tracks: 99; persistent (alive >= 50% of run): 9; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.58 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 34], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.0784/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.146, nucleations 11
- channel total drift (end/start - 1): [-0.5023, -0.3617, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 113: holes 0, rim-vs-core 0.72, rim-vs-outside 0.38, heterogeneity 0.22; core [0.946, 0.91, 0.304, 0.559] rim [0.75, 0.641, 0.654, 0.02]
  - track 13 at frame 114: holes 0, rim-vs-core 0.71, rim-vs-outside 0.35, heterogeneity 0.21; core [0.934, 0.879, 0.362, 0.539] rim [0.738, 0.604, 0.72, 0.021]
  - track 15 at frame 114: holes 0, rim-vs-core 0.67, rim-vs-outside 0.42, heterogeneity 0.23; core [0.945, 0.919, 0.36, 0.55] rim [0.77, 0.674, 0.731, 0.083]
  - track 55 at frame 150: holes 0, rim-vs-core 0.70, rim-vs-outside 0.38, heterogeneity 0.20; core [0.945, 0.874, 0.311, 0.513] rim [0.744, 0.591, 0.66, 0.018]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 161 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 4.75 (aggregate of 161 individuals; 0/161 membrane-like individually; rim level 0.757)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 8.19 (aggregate of 161 individuals; 0/161 membrane-like individually; rim level 0.629)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 3 (aggregate of 161 individuals; 129/161 membrane-like individually; rim level 0.578)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.238, rim/outside 1.56 (aggregate of 161 individuals; 11/161 membrane-like individually; rim level 0.129)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #11 (t=565, R_eq 3.19): ['surfactant s']; #13 (t=570, R_eq 3.39): ['surfactant s']; #15 (t=570, R_eq 3.61): ['surfactant s']; #55 (t=750, R_eq 3.09): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 161 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
