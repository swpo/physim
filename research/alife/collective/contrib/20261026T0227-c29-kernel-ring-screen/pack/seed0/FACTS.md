# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 321s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5856], min area 6 px

## Measurements
- components: final 298, mean 220.6, max 298; occupancy final 0.38
- tracks: 1200; persistent (alive >= 50% of run): 218; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.35 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [300, 299, 298], H1 [0, 0, 0]
- motion: 101 long-lived tracks moved >= 1 body length; max speed 0.033/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 1000, default): splits 477, persistent splits 224 (1 more failed only because the siblings re-merged within K), max generation 5, merges 72, merge/split ratio 0.151, nucleations 2
- channel total drift (end/start - 1): [-0.5593, -0.7042, 0.4298, 0.3526]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 430 at frame 113: holes 0, rim-vs-core 0.59, rim-vs-outside 0.57, heterogeneity 0.17; core [0.106, 0.77, 0.731, 0.887] rim [0.247, 0.392, 0.441, 0.579]
  - track 463 at frame 114: holes 0, rim-vs-core 0.56, rim-vs-outside 0.46, heterogeneity 0.15; core [0.106, 0.689, 0.693, 0.907] rim [0.238, 0.403, 0.447, 0.521]
  - track 468 at frame 114: holes 0, rim-vs-core 0.60, rim-vs-outside 0.57, heterogeneity 0.17; core [0.108, 0.763, 0.721, 0.886] rim [0.248, 0.375, 0.43, 0.563]
  - track 992 at frame 143: holes 0, rim-vs-core 0.63, rim-vs-outside 0.57, heterogeneity 0.18; core [0.108, 0.777, 0.739, 0.886] rim [0.244, 0.371, 0.42, 0.557]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1434 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 8.52, rim/outside 0.942 (aggregate of 1434 individuals; 0/1434 membrane-like individually; rim level 0.378)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 11 (aggregate of 1434 individuals; 1/1434 membrane-like individually; rim level 0.723)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 10.1 (aggregate of 1434 individuals; 1148/1434 membrane-like individually; rim level 0.824)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 8.31 (aggregate of 1434 individuals; 4/1434 membrane-like individually; rim level 0.934)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #430 (t=5650, R_eq 5.11): ['L link']; #463 (t=5700, R_eq 5.41): ['L link']; #468 (t=5700, R_eq 5.35): none; #992 (t=7150, R_eq 5.01): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1434 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
