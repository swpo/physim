# Evidence pack: ringswim-dl2 (seed 1)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 276s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5875], min area 6 px

## Measurements
- components: final 295, mean 207.9, max 295; occupancy final 0.38
- tracks: 1320; persistent (alive >= 50% of run): 163; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.10 (1 = constant size)
- enclosures: components with a hole mean 0.23, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [295, 295, 295], H1 [0, 0, 0]
- motion: 116 long-lived tracks moved >= 1 body length; max speed 0.0295/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 526, persistent splits 244 (0 more failed only because the siblings re-merged within K), max generation 6, merges 95, merge/split ratio 0.181, nucleations 4
- channel total drift (end/start - 1): [-0.5585, -0.7056, 0.4314, 0.5665]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 196 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 0.50, heterogeneity 0.18; core [0.135, 0.746, 0.748, 0.894] rim [0.278, 0.334, 0.398, 0.508]
  - track 334 at frame 109: holes 0, rim-vs-core 0.64, rim-vs-outside 0.54, heterogeneity 0.17; core [0.101, 0.763, 0.695, 0.874] rim [0.254, 0.335, 0.384, 0.541]
  - track 412 at frame 113: holes 0, rim-vs-core 0.62, rim-vs-outside 0.38, heterogeneity 0.17; core [0.146, 0.669, 0.773, 0.9] rim [0.241, 0.388, 0.452, 0.459]
  - track 1165 at frame 151: holes 0, rim-vs-core 0.59, rim-vs-outside 0.57, heterogeneity 0.17; core [0.108, 0.766, 0.72, 0.883] rim [0.249, 0.378, 0.428, 0.575]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1370 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 7.51, rim/outside 0.936 (aggregate of 1370 individuals; 0/1370 membrane-like individually; rim level 0.383)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 10.3 (aggregate of 1370 individuals; 0/1370 membrane-like individually; rim level 0.708)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 9.48 (aggregate of 1370 individuals; 987/1370 membrane-like individually; rim level 0.804)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 8.12 (aggregate of 1370 individuals; 6/1370 membrane-like individually; rim level 0.922)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #196 (t=5050, R_eq 5.17): ['L link']; #334 (t=5450, R_eq 5.53): ['L link']; #412 (t=5650, R_eq 4.62): none; #1165 (t=7550, R_eq 5.2): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1370 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
