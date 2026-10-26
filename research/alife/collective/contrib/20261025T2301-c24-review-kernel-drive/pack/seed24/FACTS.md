# Evidence pack: ringswim-dl2 (seed 24)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 460s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/20261025T2301-c24-review-kernel-drive/pack/seed24 --seeds 24 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5616], min area 6 px

## Measurements
- components: final 89, mean 68.5, max 100; occupancy final 0.20
- tracks: 1045; persistent (alive >= 50% of run): 1; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.79 (1 = constant size)
- enclosures: components with a hole mean 0.31, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 90, 90], H1 [51, 5, 0]
- motion: 187 long-lived tracks moved >= 1 body length; max speed 0.0269/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 459, persistent splits 122 (0 more failed only because the siblings re-merged within K), max generation 8, merges 12, merge/split ratio 0.026, nucleations 0
- channel total drift (end/start - 1): [-0.3183, -0.8387, -0.1441, -0.3149]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 432 at frame 131: holes 0, rim-vs-core 0.62, rim-vs-outside 0.44, heterogeneity 0.16; core [0.229, 0.733, 0.944, 0.895] rim [0.321, 0.407, 0.665, 0.462]
  - track 271 at frame 84: holes 0, rim-vs-core 0.41, rim-vs-outside 0.79, heterogeneity 0.16; core [0.084, 0.702, 0.629, 0.868] rim [0.293, 0.455, 0.624, 0.623]
  - track 446 at frame 113: holes 0, rim-vs-core 0.40, rim-vs-outside 0.81, heterogeneity 0.18; core [0.084, 0.763, 0.662, 0.818] rim [0.296, 0.464, 0.634, 0.654]
  - track 841 at frame 180: holes 0, rim-vs-core 0.28, rim-vs-outside 0.94, heterogeneity 0.16; core [0.105, 0.763, 0.688, 0.826] rim [0.229, 0.543, 0.62, 0.715]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 430 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 9.47, rim/outside 0.835 (aggregate of 430 individuals; 0/430 membrane-like individually; rim level 0.538)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 11 (aggregate of 430 individuals; 3/430 membrane-like individually; rim level 0.699)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 7.93 (aggregate of 430 individuals; 189/430 membrane-like individually; rim level 0.766)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 11.4 (aggregate of 430 individuals; 147/430 membrane-like individually; rim level 0.845)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #432 (t=6550, R_eq 3.7): none; #271 (t=4200, R_eq 7.42): ['L link']; #446 (t=5650, R_eq 7.27): none; #841 (t=9000, R_eq 7.59): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 430 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
