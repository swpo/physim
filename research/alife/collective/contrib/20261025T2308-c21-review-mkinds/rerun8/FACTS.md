# Evidence pack: membrane-kinds (seed 8)

- world: `../../../../threads/autopoiesis/worlds/membrane_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_kinds/world.py --out collective/contrib/20261025T2308-c21-review-mkinds/rerun8 --seeds 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6244], min area 6 px

## Measurements
- components: final 10, mean 14.0, max 28; occupancy final 0.11
- tracks: 182; persistent (alive >= 50% of run): 1; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.85 (1 = constant size)
- enclosures: components with a hole mean 7.93, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 10], H1 [5, 3, 1]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00997/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 76, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.105, nucleations 0
- channel total drift (end/start - 1): [-0.2251, -1.0, None, -0.5293, -0.6736]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 52: holes 1, rim-vs-core 0.17, rim-vs-outside 0.87, heterogeneity 0.16; core [0.137, 0.839, 0.0, 0.648, 0.621] rim [0.195, 0.692, 0.0, 0.592, 0.606]
  - track 44 at frame 49: holes 0, rim-vs-core 0.37, rim-vs-outside 0.75, heterogeneity 0.13; core [0.144, 0.782, 0.0, 0.577, 0.836] rim [0.285, 0.499, 0.0, 0.588, 0.65]
  - track 104 at frame 141: holes 0, rim-vs-core 0.31, rim-vs-outside 0.78, heterogeneity 0.15; core [0.061, 0.145, 0.625, 0.461, 0.697] rim [0.244, 0.104, 0.432, 0.596, 0.645]
  - track 142 at frame 165: holes 0, rim-vs-core 0.58, rim-vs-outside 0.50, heterogeneity 0.15; core [0.229, 0.0, 0.82, 0.908, 0.814] rim [0.33, 0.0, 0.479, 0.711, 0.407]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.77, rim/outside 0.781 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.48)
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 6.47 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.455)
  - radial K2: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 9.19 (aggregate of 83 individuals; 1/83 membrane-like individually; rim level 0.297)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 5.54 (aggregate of 83 individuals; 61/83 membrane-like individually; rim level 0.595)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 5.98 (aggregate of 83 individuals; 59/83 membrane-like individually; rim level 0.596)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #30 (t=2600, R_eq 10.28, ring): ['L link', 'membrane (wall)']; #44 (t=2450, R_eq 6.91): none; #104 (t=7050, R_eq 9.59): ['L link']; #142 (t=8250, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 37 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
