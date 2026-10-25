# Evidence pack: nematic-fuelcell-planted (seed 12)

- world: `../../world_plant.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 400s; status ok
- command: `python -m labkit.run world_plant.py --out planted_k3/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.7279, 0.7454], min area 6 px

## Measurements
- components: final 4, mean 4.0, max 6; occupancy final 0.01
- tracks: 19; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00899/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.286, nucleations 0
- channel total drift (end/start - 1): [-0.1162, -0.917, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.40, heterogeneity 0.14; core [0.96, 0.953, 0.705, 0.773] rim [0.778, 0.658, 0.935, 0.612]
  - track 15 at frame 114: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.14; core [0.954, 0.913, 0.73, 0.778] rim [0.765, 0.587, 0.95, 0.601]
  - track 16 at frame 114: holes 0, rim-vs-core 0.47, rim-vs-outside 0.40, heterogeneity 0.14; core [0.958, 0.899, 0.729, 0.799] rim [0.777, 0.579, 0.951, 0.62]
  - track 18 at frame 119: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.14; core [0.947, 0.918, 0.731, 0.776] rim [0.757, 0.598, 0.95, 0.597]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 4.6 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.862)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 11.7 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.767)
  - radial shell s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 2.01 (aggregate of 24 individuals; 17/24 membrane-like individually; rim level 0.89)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 5.1 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.69)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=505, R_eq 3.78): ['shell s']; #15 (t=570, R_eq 3.57): ['shell s']; #16 (t=570, R_eq 3.43): ['shell s']; #18 (t=595, R_eq 3.74): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
