# Evidence pack: membrane-kinds-chi0 (seed 3)

- world: `../world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 16s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0318-c32-review-membrane-kinds/world_chi0.py --out collective/contrib/20261026T0318-c32-review-membrane-kinds/pack_chi0 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5903], min area 6 px

## Measurements
- components: final 39, mean 29.5, max 42; occupancy final 0.35
- tracks: 130; persistent (alive >= 50% of run): 21; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.48 (1 = constant size)
- enclosures: components with a hole mean 2.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 26]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [38, 36, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00386/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 53, persistent splits 37 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.019, nucleations 0
- channel total drift (end/start - 1): [-0.5217, -0.7695, None, 0.2384, 0.0028]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 119: holes 0, rim-vs-core 0.45, rim-vs-outside 1.00, heterogeneity 0.15; core [0.089, 0.859, 0.0, 0.762, 0.595] rim [0.288, 0.478, 0.0, 0.707, 0.701]
  - track 55 at frame 121: holes 0, rim-vs-core 0.42, rim-vs-outside 1.03, heterogeneity 0.14; core [0.083, 0.854, 0.0, 0.749, 0.589] rim [0.271, 0.514, 0.0, 0.725, 0.739]
  - track 64 at frame 126: holes 0, rim-vs-core 0.44, rim-vs-outside 1.01, heterogeneity 0.14; core [0.09, 0.864, 0.0, 0.769, 0.599] rim [0.282, 0.492, 0.0, 0.719, 0.71]
  - track 124 at frame 190: holes 0, rim-vs-core 0.41, rim-vs-outside 1.10, heterogeneity 0.13; core [0.05, 0.005, 0.976, 0.788, 0.775] rim [0.223, 0.003, 0.612, 0.803, 0.695]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 189 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 12.4, rim/outside 0.9 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.482)
  - radial K1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 12.7 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.715)
  - radial K2: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 7.39 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.107)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 9.6 (aggregate of 189 individuals; 3/189 membrane-like individually; rim level 0.818)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.99, rim/outside 8.89 (aggregate of 189 individuals; 177/189 membrane-like individually; rim level 0.843)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #51 (t=5950, R_eq 7.53): ['membrane (wall)']; #55 (t=6050, R_eq 7.63): ['membrane (wall)']; #64 (t=6300, R_eq 7.18): ['membrane (wall)']; #124 (t=9500, R_eq 6.05): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 189 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
