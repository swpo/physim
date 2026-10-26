# Evidence pack: active-nematic-marangoni-two-kinds (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 456s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/20261026T0655-c34-two-kinds-swap/swap --seeds 0 1 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8331, 0.6513], min area 6 px

## Measurements
- components: final 32, mean 16.6, max 33; occupancy final 0.09
- tracks: 100; persistent (alive >= 50% of run): 4; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 31], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.302/time; max body lengths 8.3
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 6, merges 12, merge/split ratio 0.286, nucleations 4
- channel total drift (end/start - 1): [-0.4928, -0.3451, 4.5763, 14.2635]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 126: holes 0, rim-vs-core 0.61, rim-vs-outside 0.33, heterogeneity 0.15; core [0.961, 0.717, 0.024, 0.394] rim [0.759, 0.451, 0.068, 0.899]
  - track 14 at frame 138: holes 0, rim-vs-core 0.67, rim-vs-outside 0.42, heterogeneity 0.17; core [0.983, 0.964, 0.34, 0.03] rim [0.766, 0.749, 0.934, 0.103]
  - track 5 at frame 96: holes 0, rim-vs-core 0.54, rim-vs-outside 0.41, heterogeneity 0.16; core [0.966, 0.825, 0.333, 0.013] rim [0.809, 0.582, 0.783, 0.031]
  - track 45 at frame 145: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.13; core [0.913, 0.711, 0.022, 0.477] rim [0.747, 0.505, 0.05, 0.873]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 4.61 (aggregate of 116 individuals; 1/116 membrane-like individually; rim level 0.706)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 8.38 (aggregate of 116 individuals; 6/116 membrane-like individually; rim level 0.559)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 2.92 (aggregate of 116 individuals; 56/116 membrane-like individually; rim level 0.195)
  - radial surfactant B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.16 (aggregate of 116 individuals; 62/116 membrane-like individually; rim level 0.46)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=630, R_eq 3.99): ['surfactant A']; #14 (t=690, R_eq 4.11): ['surfactant A', 'surfactant B']; #5 (t=480, R_eq 4.18): ['surfactant A', 'surfactant B']; #45 (t=725, R_eq 4.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 116 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
