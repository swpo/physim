# Evidence pack: active-nematic-marangoni-two-kinds (seed 4)

- world: `../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 660s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/20261026T0915-c38-review-two-kinds/rerun/neutral_seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8412, 0.5767], min area 6 px

## Measurements
- components: final 31, mean 24.8, max 33; occupancy final 0.09
- tracks: 97; persistent (alive >= 50% of run): 18; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 31], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.265/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 14, merge/split ratio 0.389, nucleations 11
- channel total drift (end/start - 1): [-0.5085, -0.4311, 11.317, 7.2695]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 114: holes 0, rim-vs-core 0.48, rim-vs-outside 0.39, heterogeneity 0.14; core [0.953, 0.62, 0.406, 0.006] rim [0.792, 0.482, 0.841, 0.014]
  - track 20 at frame 116: holes 0, rim-vs-core 0.59, rim-vs-outside 0.34, heterogeneity 0.16; core [0.933, 0.795, 0.444, 0.032] rim [0.722, 0.473, 0.885, 0.073]
  - track 22 at frame 119: holes 0, rim-vs-core 0.46, rim-vs-outside 0.28, heterogeneity 0.13; core [0.915, 0.527, 0.018, 0.465] rim [0.737, 0.353, 0.04, 0.849]
  - track 79 at frame 165: holes 0, rim-vs-core 0.57, rim-vs-outside 0.38, heterogeneity 0.15; core [0.945, 0.897, 0.373, 0.024] rim [0.751, 0.567, 0.792, 0.062]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 164 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 4.52 (aggregate of 164 individuals; 1/164 membrane-like individually; rim level 0.703)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 8.87 (aggregate of 164 individuals; 9/164 membrane-like individually; rim level 0.53)
  - radial surfactant A: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 3.25 (aggregate of 164 individuals; 73/164 membrane-like individually; rim level 0.411)
  - radial surfactant B: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 2.93 (aggregate of 164 individuals; 60/164 membrane-like individually; rim level 0.232)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=570, R_eq 4.03): none; #20 (t=580, R_eq 3.83): ['surfactant A', 'surfactant B']; #22 (t=595, R_eq 4.65): none; #79 (t=825, R_eq 3.61): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 164 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
