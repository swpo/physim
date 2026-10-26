# Evidence pack: membrane-kinds (seed 3)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 16s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0318-c32-review-membrane-kinds/world.py --out collective/contrib/20261026T0318-c32-review-membrane-kinds/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6071], min area 6 px

## Measurements
- components: final 8, mean 11.6, max 20; occupancy final 0.14
- tracks: 163; persistent (alive >= 50% of run): 1; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.05 (1 = constant size)
- enclosures: components with a hole mean 7.62, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 4, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [7, 7, 4]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00932/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 67, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.09, nucleations 0
- channel total drift (end/start - 1): [-0.2209, -0.9977, None, -0.5465, -0.6373]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 56 at frame 86: holes 1, rim-vs-core 0.22, rim-vs-outside 0.81, heterogeneity 0.15; core [0.106, 0.659, 0.0, 0.521, 0.83] rim [0.169, 0.641, 0.0, 0.545, 0.623]
  - track 106 at frame 141: holes 1, rim-vs-core 0.15, rim-vs-outside 0.82, heterogeneity 0.15; core [0.115, 0.765, 0.0, 0.566, 0.671] rim [0.188, 0.644, 0.0, 0.568, 0.621]
  - track 105 at frame 133: holes 1, rim-vs-core 0.15, rim-vs-outside 0.80, heterogeneity 0.15; core [0.118, 0.773, 0.0, 0.581, 0.645] rim [0.178, 0.638, 0.0, 0.555, 0.62]
  - track 124 at frame 158: holes 1, rim-vs-core 0.16, rim-vs-outside 0.82, heterogeneity 0.17; core [0.124, 0.769, 0.0, 0.622, 0.693] rim [0.194, 0.673, 0.0, 0.579, 0.587]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 12, rim/outside 0.725 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.453)
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 5.4 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.532)
  - radial K2: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.28 (aggregate of 64 individuals; 3/64 membrane-like individually; rim level 0.222)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 4.81 (aggregate of 64 individuals; 53/64 membrane-like individually; rim level 0.547)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.71, rim/outside 4.38 (aggregate of 64 individuals; 55/64 membrane-like individually; rim level 0.528)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #56 (t=4300, R_eq 14.12, ring): ['L link', 'membrane (wall)']; #106 (t=7050, R_eq 10.56, ring): ['L link', 'membrane (wall)']; #105 (t=6650, R_eq 12.77, ring): ['L link', 'membrane (wall)']; #124 (t=7900, R_eq 12.06, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 48 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
