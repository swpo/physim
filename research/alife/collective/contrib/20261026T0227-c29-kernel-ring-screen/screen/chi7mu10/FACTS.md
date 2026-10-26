# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi7mu10 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5961], min area 6 px

## Measurements
- components: final 74, mean 58.5, max 74; occupancy final 0.39
- tracks: 269; persistent (alive >= 50% of run): 63; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.20 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [74, 74, 74], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0302/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 1000, default): splits 97, persistent splits 44 (0 more failed only because the siblings re-merged within K), max generation 3, merges 22, merge/split ratio 0.227, nucleations 1
- channel total drift (end/start - 1): [-0.5729, -0.6945, 0.4458, 0.3636]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 90 at frame 109: holes 0, rim-vs-core 0.56, rim-vs-outside 0.57, heterogeneity 0.16; core [0.124, 0.754, 0.678, 0.903] rim [0.258, 0.412, 0.388, 0.587]
  - track 155 at frame 118: holes 0, rim-vs-core 0.42, rim-vs-outside 0.72, heterogeneity 0.16; core [0.122, 0.747, 0.674, 0.9] rim [0.215, 0.5, 0.449, 0.66]
  - track 166 at frame 119: holes 0, rim-vs-core 0.42, rim-vs-outside 0.94, heterogeneity 0.18; core [0.117, 0.845, 0.745, 0.897] rim [0.217, 0.529, 0.53, 0.743]
  - track 224 at frame 128: holes 0, rim-vs-core 0.67, rim-vs-outside 0.56, heterogeneity 0.18; core [0.139, 0.774, 0.717, 0.916] rim [0.256, 0.37, 0.353, 0.546]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 382 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.1, rim/outside 0.969 (aggregate of 382 individuals; 0/382 membrane-like individually; rim level 0.369)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 8.03 (aggregate of 382 individuals; 0/382 membrane-like individually; rim level 0.698)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 7.97 (aggregate of 382 individuals; 255/382 membrane-like individually; rim level 0.749)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 6.2 (aggregate of 382 individuals; 0/382 membrane-like individually; rim level 0.896)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #90 (t=5450, R_eq 5.7): none; #155 (t=5900, R_eq 5.75): none; #166 (t=5950, R_eq 6.15): none; #224 (t=6400, R_eq 5.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
