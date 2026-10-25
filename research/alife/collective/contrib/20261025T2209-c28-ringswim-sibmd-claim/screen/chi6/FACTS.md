# Evidence pack: ringswim-waste-256 (seed 0)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 60 steps x dt 1.0 = time 12000; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/c28sd/chi6 --seeds 0 --size 128 128 --spf 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5511], min area 6 px

## Measurements
- components: final 3, mean 3.8, max 25; occupancy final 0.16
- tracks: 265; persistent (alive >= 50% of run): 0; longest 21 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.54, final 3; holes at thresholds 0.2/0.35/0.5 final [2, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [3, 3, 3]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0159/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 1200, default): splits 76, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 72, merge/split ratio 0.947, nucleations 0
- channel total drift (end/start - 1): [-0.3697, -0.7836, -0.3145, -0.5487]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 12: holes 0, rim-vs-core 0.76, rim-vs-outside 0.55, heterogeneity 0.21; core [0.259, 0.846, 0.775, 0.841] rim [0.412, 0.291, 0.352, 0.585]
  - track 72 at frame 39: holes 0, rim-vs-core 0.64, rim-vs-outside 0.92, heterogeneity 0.25; core [0.143, 0.919, 0.516, 0.516] rim [0.416, 0.388, 0.534, 0.746]
  - track 56 at frame 22: holes 1, rim-vs-core 0.26, rim-vs-outside 0.75, heterogeneity 0.24; core [0.092, 0.76, 0.345, 0.495] rim [0.196, 0.564, 0.426, 0.602]
  - track 57 at frame 22: holes 1, rim-vs-core 0.19, rim-vs-outside 0.72, heterogeneity 0.24; core [0.088, 0.681, 0.374, 0.629] rim [0.209, 0.582, 0.464, 0.574]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 8.01, rim/outside 0.737 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.483)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 5.99 (aggregate of 29 individuals; 2/29 membrane-like individually; rim level 0.573)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 4.31 (aggregate of 29 individuals; 18/29 membrane-like individually; rim level 0.388)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 4.73 (aggregate of 29 individuals; 19/29 membrane-like individually; rim level 0.443)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #29 (t=720, R_eq 4.48): ['L link', 'membrane (wall)']; #72 (t=2340, R_eq 7.18): ['L link', 'membrane (wall)']; #56 (t=1320, R_eq 13.39, ring): ['L link']; #57 (t=1320, R_eq 13.76, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
