# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi5mu125 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6], min area 6 px

## Measurements
- components: final 14, mean 19.2, max 34; occupancy final 0.20
- tracks: 621; persistent (alive >= 50% of run): 0; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 17, 15], H1 [8, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.0326/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 1000, default): splits 213, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 139, merge/split ratio 0.653, nucleations 1
- channel total drift (end/start - 1): [-0.3469, -0.8329, -0.1084, -0.3529]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 404 at frame 133: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.15; core [0.179, 0.585, 0.691, 0.9] rim [0.262, 0.381, 0.437, 0.445]
  - track 362 at frame 118: holes 0, rim-vs-core 0.64, rim-vs-outside 0.59, heterogeneity 0.19; core [0.196, 0.793, 0.719, 0.854] rim [0.378, 0.309, 0.42, 0.618]
  - track 463 at frame 153: holes 0, rim-vs-core 0.73, rim-vs-outside 0.56, heterogeneity 0.20; core [0.229, 0.798, 0.776, 0.872] rim [0.398, 0.294, 0.393, 0.561]
  - track 547 at frame 178: holes 0, rim-vs-core 0.36, rim-vs-outside 0.76, heterogeneity 0.16; core [0.233, 0.714, 0.799, 0.932] rim [0.29, 0.542, 0.575, 0.71]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 111 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 3.65, rim/outside 0.882 (aggregate of 111 individuals; 0/111 membrane-like individually; rim level 0.51)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 7.55 (aggregate of 111 individuals; 3/111 membrane-like individually; rim level 0.616)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 6.3 (aggregate of 111 individuals; 42/111 membrane-like individually; rim level 0.698)
  - radial membrane (wall): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.16 (aggregate of 111 individuals; 3/111 membrane-like individually; rim level 0.836)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #404 (t=6650, R_eq 4.58): none; #362 (t=5900, R_eq 5.32): ['L link']; #463 (t=7650, R_eq 4.82): ['L link']; #547 (t=8900, R_eq 4.55): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
