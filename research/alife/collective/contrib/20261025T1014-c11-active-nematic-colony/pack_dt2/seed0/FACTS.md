# Evidence pack: active-nematic-droplets (seed 0)

- world: `../../world3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 200 steps x dt 0.025 (--dt; world META dt 0.05) = time 1000; grid [128, 128]; wall 570s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world3.py --out /tmp/claude-0/c11ex/c_dt2/seed0 --seeds 0 --dt 0.025 --spf 200 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8232, 0.6019], min area 6 px

## Measurements
- components: final 30, mean 24.4, max 34; occupancy final 0.06
- tracks: 150; persistent (alive >= 50% of run): 7; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 30], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.159/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 100, default): splits 61, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 4, merges 19, merge/split ratio 0.311, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.4048, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 114: holes 0, rim-vs-core 0.33, rim-vs-outside 0.31, heterogeneity 0.14; core [0.922, 0.822, 0.41] rim [0.731, 0.554, 0.43]
  - track 35 at frame 124: holes 0, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.16; core [0.953, 0.909, 0.535] rim [0.749, 0.619, 0.523]
  - track 50 at frame 138: holes 0, rim-vs-core 0.27, rim-vs-outside 0.32, heterogeneity 0.11; core [0.9, 0.722, 0.475] rim [0.724, 0.515, 0.464]
  - track 91 at frame 161: holes 0, rim-vs-core 0.36, rim-vs-outside 0.35, heterogeneity 0.15; core [0.941, 0.898, 0.512] rim [0.733, 0.603, 0.513]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 159 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 4.79 (aggregate of 159 individuals; 0/159 membrane-like individually; rim level 0.767)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 8.16 (aggregate of 159 individuals; 1/159 membrane-like individually; rim level 0.655)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=570, R_eq 3.24): none; #35 (t=620, R_eq 3.19): none; #50 (t=690, R_eq 3.7): none; #91 (t=805, R_eq 3.04): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 159 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
