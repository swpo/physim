# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi4kd12 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5767], min area 6 px

## Measurements
- components: final 48, mean 38.9, max 56; occupancy final 0.25
- tracks: 280; persistent (alive >= 50% of run): 12; longest 162 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.44 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 48, 48], H1 [14, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0245/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 1000, default): splits 114, persistent splits 55 (0 more failed only because the siblings re-merged within K), max generation 6, merges 10, merge/split ratio 0.088, nucleations 0
- channel total drift (end/start - 1): [-0.4195, -0.8049, 0.0518, -0.1744]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 117 at frame 119: holes 0, rim-vs-core 0.34, rim-vs-outside 0.86, heterogeneity 0.15; core [0.065, 0.707, 0.588, 0.868] rim [0.259, 0.481, 0.575, 0.701]
  - track 124 at frame 124: holes 0, rim-vs-core 0.58, rim-vs-outside 0.53, heterogeneity 0.16; core [0.122, 0.724, 0.715, 0.889] rim [0.273, 0.372, 0.461, 0.543]
  - track 134 at frame 126: holes 0, rim-vs-core 0.38, rim-vs-outside 0.93, heterogeneity 0.17; core [0.082, 0.792, 0.649, 0.816] rim [0.272, 0.48, 0.605, 0.73]
  - track 208 at frame 155: holes 0, rim-vs-core 0.51, rim-vs-outside 0.61, heterogeneity 0.16; core [0.104, 0.736, 0.685, 0.873] rim [0.268, 0.396, 0.489, 0.595]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.43, rim/outside 0.895 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.457)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 11.7 (aggregate of 242 individuals; 1/242 membrane-like individually; rim level 0.715)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 9.87 (aggregate of 242 individuals; 159/242 membrane-like individually; rim level 0.791)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 9.46 (aggregate of 242 individuals; 25/242 membrane-like individually; rim level 0.9)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #117 (t=5950, R_eq 7.29): ['L link']; #124 (t=6200, R_eq 5.64): none; #134 (t=6300, R_eq 6.18): ['L link']; #208 (t=7750, R_eq 5.89): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
