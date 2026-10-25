# Evidence pack: active-nematic-droplets (seed 3)

- world: `../../20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 301s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out collective/contrib/20261025T1049-c01-review-nematic/zeta0 --seeds 3 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.8223, 0.9385], min area 6 px

## Measurements
- components: final 6, mean 5.6, max 6; occupancy final 0.05
- tracks: 6; persistent (alive >= 50% of run): 6; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [-0.5034, -0.3212, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.47, rim-vs-outside 0.57, heterogeneity 0.21; core [0.967, 0.936, 0.419] rim [0.685, 0.558, 0.438]
  - track 1 at frame 106: holes 0, rim-vs-core 0.27, rim-vs-outside 0.75, heterogeneity 0.17; core [0.949, 0.906, 0.42] rim [0.782, 0.694, 0.421]
  - track 2 at frame 108: holes 0, rim-vs-core 0.25, rim-vs-outside 0.77, heterogeneity 0.17; core [0.962, 0.929, 0.421] rim [0.811, 0.729, 0.421]
  - track 3 at frame 108: holes 0, rim-vs-core 0.46, rim-vs-outside 0.57, heterogeneity 0.25; core [0.966, 0.932, 0.429] rim [0.695, 0.567, 0.462]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 35.2 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.912)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 60 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.833)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 6.43): none; #1 (t=530, R_eq 6.7): none; #2 (t=540, R_eq 6.6): none; #3 (t=540, R_eq 6.13): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
