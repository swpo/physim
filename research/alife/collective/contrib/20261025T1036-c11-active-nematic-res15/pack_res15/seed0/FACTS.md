# Evidence pack: active-nematic-droplets (seed 0)

- world: `../../world3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 753s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world3.py --out /tmp/claude-0/c11ex/c_res15/seed0 --seeds 0 --size 192 192 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8089, 0.5458], min area 6 px

## Measurements
- components: final 13, mean 5.2, max 14; occupancy final 0.04
- tracks: 31; persistent (alive >= 50% of run): 0; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 15, 12], H1 [1, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.14/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.143, nucleations 1
- channel total drift (end/start - 1): [-0.5018, -0.6404, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 153: holes 0, rim-vs-core 0.32, rim-vs-outside 0.49, heterogeneity 0.21; core [0.993, 0.952, 0.377] rim [0.83, 0.687, 0.465]
  - track 4 at frame 146: holes 0, rim-vs-core 0.33, rim-vs-outside 0.30, heterogeneity 0.16; core [0.959, 0.932, 0.417] rim [0.758, 0.67, 0.431]
  - track 11 at frame 150: holes 0, rim-vs-core 0.29, rim-vs-outside 0.25, heterogeneity 0.13; core [0.937, 0.781, 0.428] rim [0.752, 0.552, 0.443]
  - track 18 at frame 183: holes 0, rim-vs-core 0.32, rim-vs-outside 0.26, heterogeneity 0.15; core [0.951, 0.928, 0.425] rim [0.756, 0.675, 0.435]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.769, rim/outside 3.96 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.679)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 5.52 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.622)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=765, R_eq 6.28): none; #4 (t=730, R_eq 5.61): none; #11 (t=750, R_eq 5.59): none; #18 (t=915, R_eq 5.32): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
