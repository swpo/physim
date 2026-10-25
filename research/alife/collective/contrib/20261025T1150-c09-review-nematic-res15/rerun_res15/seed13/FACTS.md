# Evidence pack: active-nematic-droplets (seed 13)

- world: `../../../20261025T1036-c11-active-nematic-res15/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 612s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1036-c11-active-nematic-res15/world.py --out collective/contrib/20261025T1150-c09-review-nematic-res15/rerun_res15/seed13 --seeds 13 --size 192 192 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.797, 0.5262], min area 6 px

## Measurements
- components: final 10, mean 4.8, max 12; occupancy final 0.03
- tracks: 25; persistent (alive >= 50% of run): 0; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 10], H1 [1, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0926/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.2, nucleations 1
- channel total drift (end/start - 1): [-0.4979, -0.7594, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 156: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.16; core [0.977, 0.974, 0.357] rim [0.797, 0.752, 0.36]
  - track 2 at frame 81: holes 0, rim-vs-core 0.21, rim-vs-outside 0.54, heterogeneity 0.17; core [0.997, 0.986, 0.464] rim [0.875, 0.819, 0.432]
  - track 1 at frame 81: holes 0, rim-vs-core 0.19, rim-vs-outside 0.53, heterogeneity 0.16; core [0.993, 0.967, 0.452] rim [0.872, 0.819, 0.433]
  - track 14 at frame 176: holes 0, rim-vs-core 0.31, rim-vs-outside 0.29, heterogeneity 0.16; core [0.981, 0.975, 0.296] rim [0.794, 0.726, 0.301]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 5.22 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.834)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 7.8 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.801)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=780, R_eq 4.51): none; #2 (t=405, R_eq 7.69): none; #1 (t=405, R_eq 7.63): none; #14 (t=880, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
