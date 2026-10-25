# Evidence pack: active-nematic-droplets (seed 11)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 513s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1245-c12-review-nematic-ringed/world.py --out collective/contrib/20261025T1245-c12-review-nematic-ringed/rerun/seed11 --seeds 11 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8239, 0.6788], min area 6 px

## Measurements
- components: final 30, mean 20.8, max 31; occupancy final 0.06
- tracks: 103; persistent (alive >= 50% of run): 9; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 29, 28], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.0768/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 13, merge/split ratio 0.325, nucleations 9
- channel total drift (end/start - 1): [-0.5045, -0.4059, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 113: holes 0, rim-vs-core 0.48, rim-vs-outside 0.33, heterogeneity 0.16; core [0.94, 0.874, 0.456] rim [0.744, 0.589, 0.794]
  - track 21 at frame 118: holes 0, rim-vs-core 0.64, rim-vs-outside 0.40, heterogeneity 0.22; core [0.988, 0.944, 0.41] rim [0.753, 0.67, 0.941]
  - track 10 at frame 94: holes 0, rim-vs-core 0.51, rim-vs-outside 0.34, heterogeneity 0.17; core [0.935, 0.907, 0.443] rim [0.712, 0.591, 0.767]
  - track 75 at frame 166: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.13; core [0.904, 0.786, 0.453] rim [0.72, 0.547, 0.707]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 140 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 4.61 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.749)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.762, rim/outside 7.57 (aggregate of 140 individuals; 3/140 membrane-like individually; rim level 0.598)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 2.17 (aggregate of 140 individuals; 104/140 membrane-like individually; rim level 0.658)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #9 (t=565, R_eq 3.61): ['surfactant s']; #21 (t=590, R_eq 4.82): ['surfactant s']; #10 (t=470, R_eq 3.24): ['surfactant s']; #75 (t=830, R_eq 3.29): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 140 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
