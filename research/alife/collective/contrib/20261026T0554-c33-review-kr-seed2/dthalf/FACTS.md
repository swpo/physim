# Evidence pack: ringswim-dl2 (seed 4)

- world: `../../20261026T0227-c29-kernel-ring-screen/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 675s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/wip-c33-kr2/dthalf --seeds 4 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5894], min area 6 px

## Measurements
- components: final 281, mean 167.3, max 281; occupancy final 0.38
- tracks: 1513; persistent (alive >= 50% of run): 56; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.83 (1 = constant size)
- enclosures: components with a hole mean 0.38, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [281, 281, 281], H1 [4, 0, 0]
- motion: 114 long-lived tracks moved >= 1 body length; max speed 0.015/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 2000, default): splits 567, persistent splits 207 (3 more failed only because the siblings re-merged within K), max generation 7, merges 169, merge/split ratio 0.298, nucleations 1
- channel total drift (end/start - 1): [-0.5556, -0.707, 0.4174, 0.3438]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 613 at frame 126: holes 0, rim-vs-core 0.67, rim-vs-outside 0.60, heterogeneity 0.20; core [0.169, 0.828, 0.733, 0.841] rim [0.355, 0.317, 0.417, 0.596]
  - track 653 at frame 128: holes 0, rim-vs-core 0.57, rim-vs-outside 0.52, heterogeneity 0.15; core [0.12, 0.699, 0.659, 0.888] rim [0.259, 0.368, 0.407, 0.529]
  - track 707 at frame 131: holes 0, rim-vs-core 0.32, rim-vs-outside 0.88, heterogeneity 0.15; core [0.09, 0.717, 0.622, 0.896] rim [0.23, 0.5, 0.565, 0.718]
  - track 1343 at frame 163: holes 0, rim-vs-core 0.42, rim-vs-outside 0.72, heterogeneity 0.16; core [0.13, 0.733, 0.697, 0.897] rim [0.222, 0.475, 0.481, 0.655]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1104 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.23, rim/outside 0.931 (aggregate of 1104 individuals; 0/1104 membrane-like individually; rim level 0.415)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 9.53 (aggregate of 1104 individuals; 3/1104 membrane-like individually; rim level 0.692)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 8.76 (aggregate of 1104 individuals; 770/1104 membrane-like individually; rim level 0.779)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 7.84 (aggregate of 1104 individuals; 11/1104 membrane-like individually; rim level 0.91)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #613 (t=12600, R_eq 5.44): ['L link']; #653 (t=12800, R_eq 5.75): ['L link']; #707 (t=13100, R_eq 6.05): none; #1343 (t=16300, R_eq 5.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1104 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
