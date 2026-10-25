# Evidence pack: nematic-fuelcell-rodsrc (seed 6)

- world: `../../world_rodsrc.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 345s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2039-c23-audit-fuelcell/world_rodsrc.py --out collective/contrib/20261025T2039-c23-audit-fuelcell/rodsrc/seed6 --seeds 6 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8832, 0.7014], min area 6 px

## Measurements
- components: final 12, mean 7.6, max 13; occupancy final 0.10
- tracks: 23; persistent (alive >= 50% of run): 7; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 48.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 13, 12], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0232/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.286, nucleations 7
- channel total drift (end/start - 1): [-0.4995, -0.0239, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 104: holes 0, rim-vs-core 0.40, rim-vs-outside 0.63, heterogeneity 0.13; core [0.948, 0.845, 0.419, 0.922] rim [0.798, 0.646, 0.723, 0.862]
  - track 0 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.67, heterogeneity 0.14; core [0.992, 0.967, 0.286, 0.966] rim [0.811, 0.678, 0.74, 0.918]
  - track 6 at frame 116: holes 0, rim-vs-core 0.56, rim-vs-outside 0.40, heterogeneity 0.15; core [0.945, 0.907, 0.455, 0.931] rim [0.702, 0.576, 0.817, 0.822]
  - track 11 at frame 173: holes 0, rim-vs-core 0.40, rim-vs-outside 0.66, heterogeneity 0.14; core [0.957, 0.822, 0.429, 0.984] rim [0.804, 0.646, 0.744, 0.926]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 2.8 (aggregate of 51 individuals; 10/51 membrane-like individually; rim level 0.492)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 3.85 (aggregate of 51 individuals; 10/51 membrane-like individually; rim level 0.41)
  - radial shell s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.6 (aggregate of 51 individuals; 21/51 membrane-like individually; rim level 0.492)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 1.48 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.794)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=520, R_eq 8.79, ring): ['phi (droplet)', 'order |Q|', 'shell s']; #0 (t=505, R_eq 7.27): none; #6 (t=580, R_eq 4.33): ['shell s']; #11 (t=865, R_eq 6.72, ring): ['phi (droplet)', 'order |Q|', 'shell s']

## Warnings
- radial: 19 of 51 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
