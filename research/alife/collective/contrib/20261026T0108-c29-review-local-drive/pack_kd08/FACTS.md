# Evidence pack: ringswim-dl2 (seed 11)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 312s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0108-c29-review-local-drive/world.py --out collective/contrib/20261026T0108-c29-review-local-drive/pack_kd08 --seeds 11 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5613], min area 6 px

## Measurements
- components: final 83, mean 73.4, max 110; occupancy final 0.19
- tracks: 996; persistent (alive >= 50% of run): 1; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.10 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [86, 84, 81], H1 [57, 5, 0]
- motion: 180 long-lived tracks moved >= 1 body length; max speed 0.0311/time; max body lengths 5.1
- replication (lineage window K = 20 frames = time 1000, default): splits 427, persistent splits 129 (0 more failed only because the siblings re-merged within K), max generation 7, merges 12, merge/split ratio 0.028, nucleations 0
- channel total drift (end/start - 1): [-0.2934, -0.8505, -0.2179, -0.3328]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 575 at frame 148: holes 0, rim-vs-core 0.69, rim-vs-outside 0.44, heterogeneity 0.19; core [0.242, 0.763, 0.937, 0.883] rim [0.359, 0.358, 0.619, 0.447]
  - track 495 at frame 121: holes 0, rim-vs-core 0.56, rim-vs-outside 0.49, heterogeneity 0.16; core [0.128, 0.707, 0.712, 0.869] rim [0.294, 0.364, 0.546, 0.499]
  - track 655 at frame 155: holes 0, rim-vs-core 0.34, rim-vs-outside 0.91, heterogeneity 0.16; core [0.063, 0.716, 0.602, 0.832] rim [0.261, 0.474, 0.621, 0.697]
  - track 848 at frame 183: holes 0, rim-vs-core 0.62, rim-vs-outside 0.45, heterogeneity 0.18; core [0.165, 0.754, 0.794, 0.871] rim [0.323, 0.361, 0.556, 0.479]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 460 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 10.1, rim/outside 0.841 (aggregate of 460 individuals; 0/460 membrane-like individually; rim level 0.549)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 11.2 (aggregate of 460 individuals; 5/460 membrane-like individually; rim level 0.72)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 8.06 (aggregate of 460 individuals; 236/460 membrane-like individually; rim level 0.779)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 11.2 (aggregate of 460 individuals; 186/460 membrane-like individually; rim level 0.859)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #575 (t=7400, R_eq 3.99): none; #495 (t=6050, R_eq 6): ['L link']; #655 (t=7750, R_eq 7.72): ['L link']; #848 (t=9150, R_eq 5.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 460 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
