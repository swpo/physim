# Evidence pack: active-nematic-droplets (seed 0)

- world: `../../world4.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 341s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world4.py --out /tmp/claude-0/c11ex/s_chi3/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8191, 0.6117], min area 6 px

## Measurements
- components: final 30, mean 18.2, max 30; occupancy final 0.06
- tracks: 80; persistent (alive >= 50% of run): 13; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.0797/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.152, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.4345, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 118: holes 0, rim-vs-core 0.52, rim-vs-outside 0.37, heterogeneity 0.17; core [0.947, 0.922, 0.438] rim [0.715, 0.604, 0.776]
  - track 23 at frame 128: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.14; core [0.914, 0.789, 0.482] rim [0.732, 0.539, 0.755]
  - track 24 at frame 128: holes 0, rim-vs-core 0.51, rim-vs-outside 0.33, heterogeneity 0.17; core [0.948, 0.798, 0.538] rim [0.74, 0.527, 0.912]
  - track 58 at frame 182: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.17; core [0.951, 0.888, 0.443] rim [0.732, 0.577, 0.806]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 4.92 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.774)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 8.39 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.662)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 2.12 (aggregate of 126 individuals; 97/126 membrane-like individually; rim level 0.656)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #15 (t=590, R_eq 3.24): ['surfactant s']; #23 (t=640, R_eq 3.48): none; #24 (t=640, R_eq 2.71): ['surfactant s']; #58 (t=910, R_eq 2.88): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
