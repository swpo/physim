# Evidence pack: nematic-fuelcell (seed 11)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 669s; status ok
- command: `python -m labkit.run /tmp/c20rev/world.py --out /tmp/c20rev/slowD_s11 --seeds 11 --no-movie`
- segmentation: matter > 0.51 of robust range [-0.8319, 0.7916], min area 6 px

## Measurements
- components: final 23, mean 17.8, max 24; occupancy final 0.07
- tracks: 52; persistent (alive >= 50% of run): 19; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 22, 22], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.0557/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.1, nucleations 9
- channel total drift (end/start - 1): [-0.5045, -0.3314, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 114: holes 0, rim-vs-core 0.48, rim-vs-outside 0.34, heterogeneity 0.16; core [0.929, 0.715, 0.958, 0.709] rim [0.681, 0.387, 0.866, 0.484]
  - track 10 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 0.33, heterogeneity 0.12; core [0.84, 0.718, 0.84, 0.589] rim [0.652, 0.471, 0.784, 0.302]
  - track 13 at frame 121: holes 0, rim-vs-core 0.40, rim-vs-outside 0.38, heterogeneity 0.16; core [0.913, 0.641, 0.959, 0.807] rim [0.661, 0.449, 0.866, 0.576]
  - track 34 at frame 136: holes 0, rim-vs-core 0.52, rim-vs-outside 0.37, heterogeneity 0.18; core [0.928, 0.84, 0.96, 0.779] rim [0.668, 0.491, 0.858, 0.506]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 6.56 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.737)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 10.7 (aggregate of 115 individuals; 3/115 membrane-like individually; rim level 0.566)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 1.54 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.872)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 3.48 (aggregate of 115 individuals; 9/115 membrane-like individually; rim level 0.518)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=570, R_eq 3.95): none; #10 (t=570, R_eq 3.39): none; #13 (t=605, R_eq 4.18): none; #34 (t=680, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
