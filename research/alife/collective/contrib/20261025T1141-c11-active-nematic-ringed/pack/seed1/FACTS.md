# Evidence pack: active-nematic-droplets (seed 1)

- world: `../../world4.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 343s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world4.py --out /tmp/claude-0/c11ex/s_chi3/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8137, 0.5791], min area 6 px

## Measurements
- components: final 21, mean 9.9, max 21; occupancy final 0.05
- tracks: 57; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 21], H1 [1, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.0831/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.12, nucleations 4
- channel total drift (end/start - 1): [-0.4928, -0.5739, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 155: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.17; core [0.973, 0.953, 0.433] rim [0.79, 0.724, 0.777]
  - track 8 at frame 87: holes 0, rim-vs-core 0.49, rim-vs-outside 0.36, heterogeneity 0.16; core [0.966, 0.944, 0.459] rim [0.764, 0.648, 0.8]
  - track 5 at frame 71: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.17; core [0.972, 0.911, 0.437] rim [0.781, 0.623, 0.783]
  - track 33 at frame 175: holes 0, rim-vs-core 0.55, rim-vs-outside 0.38, heterogeneity 0.18; core [0.968, 0.939, 0.487] rim [0.744, 0.62, 0.869]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 4.66 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.759)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 7.52 (aggregate of 69 individuals; 1/69 membrane-like individually; rim level 0.692)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 2.07 (aggregate of 69 individuals; 46/69 membrane-like individually; rim level 0.659)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=775, R_eq 3.39): ['surfactant s']; #8 (t=435, R_eq 3.14): ['surfactant s']; #5 (t=355, R_eq 2.88): ['surfactant s']; #33 (t=875, R_eq 2.99): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
