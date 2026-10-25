# Evidence pack: pcell-multilevel-cy0 (seed 5)

- world: `../../world_cy0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 528s; status ok
- command: `python -m labkit.run collective/contrib/_c07rev20/world_cy0.py --out collective/contrib/_c07rev20/rerun_cy0/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5572], min area 6 px

## Measurements
- components: final 5, mean 14.3, max 25; occupancy final 0.28
- tracks: 68; persistent (alive >= 50% of run): 8; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.32 (1 = constant size)
- enclosures: components with a hole mean 4.52, final 3; holes at thresholds 0.2/0.35/0.5 final [44, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 5, 5], H1 [9, 4, 4]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.00311/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 10000, default): splits 18, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.278, nucleations 2
- channel total drift (end/start - 1): [-0.779, -0.4057, 1.0059, -0.3466, 0.1409]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 101: holes 1, rim-vs-core 0.35, rim-vs-outside 0.77, heterogeneity 0.22; core [0.211, 0.599, 0.682, 0.539, 0.734] rim [0.296, 0.322, 0.565, 0.563, 0.576]
  - track 29 at frame 103: holes 0, rim-vs-core 0.41, rim-vs-outside 0.94, heterogeneity 0.18; core [0.298, 0.602, 0.949, 0.882, 0.688] rim [0.348, 0.36, 0.704, 0.671, 0.616]
  - track 37 at frame 96: holes 0, rim-vs-core 0.62, rim-vs-outside 1.03, heterogeneity 0.22; core [0.205, 0.648, 0.729, 0.506, 0.77] rim [0.369, 0.172, 0.642, 0.771, 0.542]
  - track 65 at frame 187: holes 0, rim-vs-core 0.66, rim-vs-outside 0.73, heterogeneity 0.22; core [0.23, 0.511, 0.846, 0.745, 0.924] rim [0.346, 0.118, 0.523, 0.625, 0.533]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.72, rim/outside 0.967 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.5)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.675, rim/outside 4.99 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.489)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 4.42 (aggregate of 77 individuals; 32/77 membrane-like individually; rim level 0.744)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.06, rim/outside 4.29 (aggregate of 77 individuals; 64/77 membrane-like individually; rim level 0.712)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 3.66 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.649)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #20 (t=50500, R_eq 9.57): ['L link', 'membrane (wall)']; #29 (t=51500, R_eq 4.58): ['membrane (wall)']; #37 (t=48000, R_eq 6.93): ['L link', 'membrane (wall)']; #65 (t=93500, R_eq 5.53): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
