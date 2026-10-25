# Evidence pack: active-nematic-droplets-audit-source-split3 (seed 0)

- world: `../world_srcsplit3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 663s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2125-c21-review-c11-ring-source/world_srcsplit3.py --out collective/contrib/20261025T2125-c21-review-c11-ring-source/res15 --seeds 0 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.7963, 0.5039], min area 6 px

## Measurements
- components: final 7, mean 2.1, max 7; occupancy final 0.02
- tracks: 13; persistent (alive >= 50% of run): 2; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0854/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 6, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5014, -0.8168, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 75: holes 0, rim-vs-core 0.47, rim-vs-outside 0.58, heterogeneity 0.14; core [1.0, 0.983, 0.7, 0.315, 0.49] rim [0.922, 0.886, 0.932, 0.53, 0.819]
  - track 1 at frame 72: holes 0, rim-vs-core 0.50, rim-vs-outside 0.57, heterogeneity 0.15; core [1.0, 0.977, 0.664, 0.308, 0.49] rim [0.919, 0.875, 0.922, 0.531, 0.829]
  - track 0 at frame 30: holes 0, rim-vs-core 1.04, rim-vs-outside 0.61, heterogeneity 0.24; core [1.0, 0.995, 0.367, 0.266, 0.322] rim [0.925, 0.589, 0.773, 0.863, 0.939]
  - track 4 at frame 112: holes 0, rim-vs-core 0.56, rim-vs-outside 0.36, heterogeneity 0.15; core [0.997, 0.996, 0.626, 0.357, 0.56] rim [0.846, 0.839, 0.888, 0.602, 0.923]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.708, rim/outside 3.4 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.665)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 4.98 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.667)
  - radial s rod-made (phi>0): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 3.11 (aggregate of 15 individuals; 1/15 membrane-like individually; rim level 0.717)
  - radial s interface-made (-0.5<phi<=0): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.78 (aggregate of 15 individuals; 5/15 membrane-like individually; rim level 0.416)
  - radial s far-bath-made (phi<=-0.5): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 1.21 (aggregate of 15 individuals; 1/15 membrane-like individually; rim level 0.633)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=375, R_eq 8.16): none; #1 (t=360, R_eq 7.84): none; #0 (t=150, R_eq 6.02): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #4 (t=560, R_eq 4.62): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
