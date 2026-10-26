# Evidence pack: ringswim-dl2 (seed 3)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 238s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0433-c32-review-kernelring/world.py --out collective/contrib/20261026T0433-c32-review-kernelring/pack --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5865], min area 6 px

## Measurements
- components: final 288, mean 192.6, max 288; occupancy final 0.37
- tracks: 1405; persistent (alive >= 50% of run): 121; longest 180 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.22 (1 = constant size)
- enclosures: components with a hole mean 0.36, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [290, 290, 289], H1 [0, 0, 0]
- motion: 107 long-lived tracks moved >= 1 body length; max speed 0.0392/time; max body lengths 4.3
- replication (lineage window K = 20 frames = time 1000, default): splits 562, persistent splits 220 (0 more failed only because the siblings re-merged within K), max generation 7, merges 117, merge/split ratio 0.208, nucleations 2
- channel total drift (end/start - 1): [-0.5556, -0.7076, 0.4197, 0.3088]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 333 at frame 111: holes 0, rim-vs-core 0.59, rim-vs-outside 0.59, heterogeneity 0.17; core [0.138, 0.776, 0.748, 0.889] rim [0.273, 0.387, 0.45, 0.591]
  - track 614 at frame 123: holes 0, rim-vs-core 0.60, rim-vs-outside 0.58, heterogeneity 0.17; core [0.128, 0.759, 0.729, 0.9] rim [0.263, 0.376, 0.427, 0.571]
  - track 640 at frame 124: holes 0, rim-vs-core 0.64, rim-vs-outside 0.54, heterogeneity 0.17; core [0.125, 0.748, 0.707, 0.886] rim [0.273, 0.341, 0.392, 0.532]
  - track 1231 at frame 155: holes 0, rim-vs-core 0.60, rim-vs-outside 0.55, heterogeneity 0.17; core [0.131, 0.756, 0.736, 0.891] rim [0.261, 0.38, 0.436, 0.564]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1275 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.89, rim/outside 0.931 (aggregate of 1275 individuals; 0/1275 membrane-like individually; rim level 0.401)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 10.8 (aggregate of 1275 individuals; 3/1275 membrane-like individually; rim level 0.707)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 9.85 (aggregate of 1275 individuals; 920/1275 membrane-like individually; rim level 0.803)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 8.57 (aggregate of 1275 individuals; 5/1275 membrane-like individually; rim level 0.921)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #333 (t=5550, R_eq 5.05): none; #614 (t=6150, R_eq 5.56): none; #640 (t=6200, R_eq 5.64): ['L link']; #1231 (t=7750, R_eq 4.92): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 1275 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
