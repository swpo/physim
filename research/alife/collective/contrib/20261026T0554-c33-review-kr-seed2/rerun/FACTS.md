# Evidence pack: ringswim-dl2 (seed 4)

- world: `../../20261026T0227-c29-kernel-ring-screen/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 337s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/wip-c33-kr2/rerun --seeds 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5904], min area 6 px

## Measurements
- components: final 294, mean 166.8, max 294; occupancy final 0.37
- tracks: 1612; persistent (alive >= 50% of run): 34; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.72 (1 = constant size)
- enclosures: components with a hole mean 0.39, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [296, 296, 294], H1 [0, 0, 0]
- motion: 122 long-lived tracks moved >= 1 body length; max speed 0.0378/time; max body lengths 5.8
- replication (lineage window K = 20 frames = time 1000, default): splits 640, persistent splits 229 (1 more failed only because the siblings re-merged within K), max generation 7, merges 152, merge/split ratio 0.237, nucleations 3
- channel total drift (end/start - 1): [-0.5524, -0.7101, 0.4098, 0.3263]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 676 at frame 128: holes 0, rim-vs-core 0.58, rim-vs-outside 0.50, heterogeneity 0.15; core [0.129, 0.693, 0.69, 0.912] rim [0.256, 0.382, 0.419, 0.526]
  - track 859 at frame 134: holes 0, rim-vs-core 0.62, rim-vs-outside 0.56, heterogeneity 0.17; core [0.133, 0.76, 0.693, 0.873] rim [0.289, 0.342, 0.403, 0.563]
  - track 860 at frame 134: holes 0, rim-vs-core 0.55, rim-vs-outside 0.49, heterogeneity 0.15; core [0.132, 0.685, 0.687, 0.912] rim [0.26, 0.396, 0.436, 0.544]
  - track 1514 at frame 175: holes 0, rim-vs-core 0.39, rim-vs-outside 0.63, heterogeneity 0.15; core [0.136, 0.675, 0.685, 0.904] rim [0.214, 0.473, 0.498, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1112 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.22, rim/outside 0.929 (aggregate of 1112 individuals; 0/1112 membrane-like individually; rim level 0.416)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 9.79 (aggregate of 1112 individuals; 3/1112 membrane-like individually; rim level 0.695)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 8.95 (aggregate of 1112 individuals; 760/1112 membrane-like individually; rim level 0.782)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 7.93 (aggregate of 1112 individuals; 4/1112 membrane-like individually; rim level 0.908)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #676 (t=6400, R_eq 5.75): none; #859 (t=6700, R_eq 5.7): ['L link']; #860 (t=6700, R_eq 5.73): none; #1514 (t=8750, R_eq 5.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 1112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
