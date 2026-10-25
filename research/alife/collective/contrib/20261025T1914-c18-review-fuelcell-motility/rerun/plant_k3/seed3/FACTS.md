# Evidence pack: nematic-fuelcell-planted (seed 3)

- world: `../world_plant.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 373s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev12/world_plant.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev12/plant_k3 --seeds 3 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.732, 0.7489], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 8; occupancy final 0.01
- tracks: 15; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.126, -0.8933, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.14; core [0.925, 0.88, 0.705, 0.69] rim [0.737, 0.561, 0.928, 0.538]
  - track 5 at frame 108: holes 0, rim-vs-core 0.45, rim-vs-outside 0.36, heterogeneity 0.13; core [0.927, 0.898, 0.699, 0.692] rim [0.742, 0.587, 0.924, 0.548]
  - track 8 at frame 109: holes 0, rim-vs-core 0.46, rim-vs-outside 0.35, heterogeneity 0.14; core [0.916, 0.862, 0.718, 0.693] rim [0.73, 0.548, 0.931, 0.523]
  - track 12 at frame 113: holes 0, rim-vs-core 0.47, rim-vs-outside 0.35, heterogeneity 0.14; core [0.926, 0.883, 0.702, 0.686] rim [0.734, 0.558, 0.925, 0.523]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 4.85 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.833)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 12.1 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.726)
  - radial shell s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 2.09 (aggregate of 30 individuals; 23/30 membrane-like individually; rim level 0.876)  MEMBRANE-LIKE
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 5.14 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.629)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell s
- membrane-like channels per top track at mid-life: #2 (t=505, R_eq 3.7): ['shell s']; #5 (t=540, R_eq 3.78): ['shell s']; #8 (t=545, R_eq 3.7): ['shell s']; #12 (t=565, R_eq 3.7): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
