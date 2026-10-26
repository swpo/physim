# Evidence pack: ringswim-dl2 (seed 3)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 239s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0145-c32-review-localdrive/world.py --out collective/contrib/20261026T0145-c32-review-localdrive/pack --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5724], min area 6 px

## Measurements
- components: final 82, mean 75.1, max 114; occupancy final 0.19
- tracks: 1265; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 85, 82], H1 [52, 6, 0]
- motion: 158 long-lived tracks moved >= 1 body length; max speed 0.0385/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 559, persistent splits 113 (0 more failed only because the siblings re-merged within K), max generation 9, merges 20, merge/split ratio 0.036, nucleations 1
- channel total drift (end/start - 1): [-0.3269, -0.833, -0.1524, -0.384]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 664 at frame 146: holes 0, rim-vs-core 0.41, rim-vs-outside 0.76, heterogeneity 0.17; core [0.118, 0.77, 0.674, 0.85] rim [0.303, 0.475, 0.632, 0.639]
  - track 583 at frame 129: holes 0, rim-vs-core 0.42, rim-vs-outside 1.01, heterogeneity 0.19; core [0.123, 0.903, 0.731, 0.695] rim [0.311, 0.534, 0.714, 0.769]
  - track 404 at frame 99: holes 0, rim-vs-core 0.78, rim-vs-outside 0.56, heterogeneity 0.21; core [0.224, 0.851, 0.886, 0.834] rim [0.416, 0.269, 0.495, 0.542]
  - track 1118 at frame 188: holes 0, rim-vs-core 0.42, rim-vs-outside 0.93, heterogeneity 0.17; core [0.114, 0.82, 0.719, 0.809] rim [0.304, 0.471, 0.655, 0.701]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 465 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.04, rim/outside 0.871 (aggregate of 465 individuals; 0/465 membrane-like individually; rim level 0.521)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 6.83 (aggregate of 465 individuals; 11/465 membrane-like individually; rim level 0.693)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 5.45 (aggregate of 465 individuals; 219/465 membrane-like individually; rim level 0.743)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 6.89 (aggregate of 465 individuals; 180/465 membrane-like individually; rim level 0.816)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #664 (t=7300, R_eq 6.38): ['L link']; #583 (t=6450, R_eq 6.48): ['membrane (wall)']; #404 (t=4950, R_eq 5.05): ['membrane (wall)']; #1118 (t=9400, R_eq 6.05): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 465 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
