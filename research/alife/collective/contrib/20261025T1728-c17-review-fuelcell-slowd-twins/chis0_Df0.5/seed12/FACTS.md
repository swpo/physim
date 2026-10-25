# Evidence pack: nematic-fuelcell (seed 12)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 389s; status ok
- command: `python -m labkit.run collective/contrib/c17-twins-wip/world.py --out collective/contrib/c17-twins-wip/chis0_Df0.5/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8608, 0.6304], min area 6 px

## Measurements
- components: final 20, mean 10.2, max 20; occupancy final 0.09
- tracks: 35; persistent (alive >= 50% of run): 6; longest 191 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 20, 19], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0602/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.1914, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 106: holes 0, rim-vs-core 0.25, rim-vs-outside 0.66, heterogeneity 0.09; core [0.953, 0.817, 0.981, 0.951] rim [0.813, 0.64, 0.942, 0.84]
  - track 6 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.66, heterogeneity 0.09; core [0.961, 0.825, 0.969, 0.93] rim [0.814, 0.649, 0.927, 0.818]
  - track 5 at frame 94: holes 0, rim-vs-core 0.38, rim-vs-outside 0.68, heterogeneity 0.11; core [0.997, 0.967, 0.964, 0.968] rim [0.821, 0.661, 0.928, 0.83]
  - track 15 at frame 156: holes 0, rim-vs-core 0.41, rim-vs-outside 0.45, heterogeneity 0.12; core [0.969, 0.954, 0.889, 0.936] rim [0.758, 0.668, 0.816, 0.752]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 3.56 (aggregate of 71 individuals; 6/71 membrane-like individually; rim level 0.572)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 5.29 (aggregate of 71 individuals; 6/71 membrane-like individually; rim level 0.479)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 1.48 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.826)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 2.24 (aggregate of 71 individuals; 3/71 membrane-like individually; rim level 0.709)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=530, R_eq 7.53, ring): none; #6 (t=505, R_eq 7.2): none; #5 (t=470, R_eq 6.31): none; #15 (t=780, R_eq 3.74): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
