# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi5mu10 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.592], min area 6 px

## Measurements
- components: final 76, mean 38.3, max 76; occupancy final 0.37
- tracks: 406; persistent (alive >= 50% of run): 2; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.47 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [76, 76, 76], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.04/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 1000, default): splits 161, persistent splits 67 (0 more failed only because the siblings re-merged within K), max generation 7, merges 35, merge/split ratio 0.217, nucleations 1
- channel total drift (end/start - 1): [-0.5572, -0.71, 0.4194, 0.2789]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 239 at frame 148: holes 0, rim-vs-core 0.76, rim-vs-outside 0.61, heterogeneity 0.21; core [0.195, 0.878, 0.791, 0.848] rim [0.374, 0.299, 0.413, 0.598]
  - track 247 at frame 148: holes 0, rim-vs-core 0.67, rim-vs-outside 0.59, heterogeneity 0.20; core [0.167, 0.818, 0.711, 0.834] rim [0.376, 0.312, 0.41, 0.597]
  - track 263 at frame 151: holes 0, rim-vs-core 0.56, rim-vs-outside 0.57, heterogeneity 0.17; core [0.119, 0.744, 0.666, 0.871] rim [0.268, 0.354, 0.414, 0.586]
  - track 394 at frame 187: holes 0, rim-vs-core 0.66, rim-vs-outside 0.58, heterogeneity 0.18; core [0.142, 0.786, 0.752, 0.886] rim [0.265, 0.347, 0.404, 0.558]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 258 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.22, rim/outside 0.913 (aggregate of 258 individuals; 0/258 membrane-like individually; rim level 0.424)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 10.3 (aggregate of 258 individuals; 0/258 membrane-like individually; rim level 0.688)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 9.39 (aggregate of 258 individuals; 158/258 membrane-like individually; rim level 0.774)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 8.7 (aggregate of 258 individuals; 1/258 membrane-like individually; rim level 0.908)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #239 (t=7400, R_eq 4.85): ['L link']; #247 (t=7400, R_eq 5.86): ['L link']; #263 (t=7550, R_eq 5.89): ['L link']; #394 (t=9350, R_eq 4.69): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 258 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
