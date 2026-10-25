# Evidence pack: fl_shell2 (seed 7)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run world.py --out pack --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9418], min area 6 px

## Measurements
- components: final 12, mean 5.4, max 12; occupancy final 0.09
- tracks: 98; persistent (alive >= 50% of run): 0; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [6, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 11, 11], H1 [9, 7, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.716/time; max body lengths 15.5
- replication (lineage window K = 20 frames = time 40, default): splits 34, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 26, merge/split ratio 0.765, nucleations 5
- channel total drift (end/start - 1): [6.6901, 5.2392, -0.5228, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 323: holes 0, rim-vs-core 0.48, rim-vs-outside 0.18, heterogeneity 0.19; core [0.522, 0.405, 0.109, 0.0] rim [0.169, 0.073, 0.1, 0.0]
  - track 39 at frame 339: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.18; core [0.447, 0.365, 0.061, 0.0] rim [0.208, 0.075, 0.054, 0.0]
  - track 18 at frame 218: holes 0, rim-vs-core 0.36, rim-vs-outside 0.26, heterogeneity 0.21; core [0.411, 0.364, 0.251, 0.0] rim [0.22, 0.075, 0.341, 0.0]
  - track 54 at frame 353: holes 0, rim-vs-core 0.34, rim-vs-outside 0.27, heterogeneity 0.20; core [0.428, 0.369, 0.13, 0.0] rim [0.25, 0.081, 0.144, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.91, rim/outside 24.4 (aggregate of 40 individuals; 31/40 membrane-like individually; rim level 0.422)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 22.7 (aggregate of 40 individuals; 9/40 membrane-like individually; rim level 0.311)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.68, rim/outside 0.836 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.208)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.297 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.0712)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0
- membrane-like channels per top track at mid-life: #31 (t=646, R_eq 7.16): ['A0']; #39 (t=678, R_eq 6.05): ['A0']; #18 (t=436, R_eq 6.51): ['A0']; #54 (t=706, R_eq 6.51): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
