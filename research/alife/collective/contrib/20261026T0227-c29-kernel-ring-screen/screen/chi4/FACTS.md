# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi4 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5982], min area 6 px

## Measurements
- components: final 45, mean 34.8, max 49; occupancy final 0.33
- tracks: 389; persistent (alive >= 50% of run): 2; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.37 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 45, 45], H1 [17, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.0366/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 1000, default): splits 168, persistent splits 56 (0 more failed only because the siblings re-merged within K), max generation 6, merges 13, merge/split ratio 0.077, nucleations 1
- channel total drift (end/start - 1): [-0.5067, -0.7295, 0.3257, 0.0985]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 132 at frame 104: holes 0, rim-vs-core 0.35, rim-vs-outside 0.87, heterogeneity 0.16; core [0.096, 0.743, 0.577, 0.829] rim [0.257, 0.459, 0.555, 0.708]
  - track 153 at frame 108: holes 0, rim-vs-core 0.40, rim-vs-outside 0.66, heterogeneity 0.16; core [0.157, 0.707, 0.677, 0.875] rim [0.274, 0.449, 0.54, 0.629]
  - track 160 at frame 111: holes 0, rim-vs-core 0.45, rim-vs-outside 0.80, heterogeneity 0.19; core [0.195, 0.808, 0.772, 0.865] rim [0.289, 0.498, 0.533, 0.657]
  - track 358 at frame 190: holes 0, rim-vs-core 0.38, rim-vs-outside 0.90, heterogeneity 0.17; core [0.124, 0.784, 0.61, 0.815] rim [0.324, 0.477, 0.596, 0.729]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 228 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 4.59, rim/outside 0.924 (aggregate of 228 individuals; 0/228 membrane-like individually; rim level 0.458)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 6.04 (aggregate of 228 individuals; 1/228 membrane-like individually; rim level 0.692)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 5.29 (aggregate of 228 individuals; 131/228 membrane-like individually; rim level 0.751)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 5.8 (aggregate of 228 individuals; 26/228 membrane-like individually; rim level 0.873)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #132 (t=5200, R_eq 6.72): ['L link']; #153 (t=5400, R_eq 5.73): ['L link']; #160 (t=5550, R_eq 5.17): ['L link']; #358 (t=9500, R_eq 6.82): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
