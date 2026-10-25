# Evidence pack: pcell-yeff (seed 5)

- world: `../../../20261025T1037-c06-pcell-yeff-response/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 250 steps x dt 1.0 = time 50000; grid [128, 128]; wall 244s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1037-c06-pcell-yeff-response/world.py --out collective/contrib/_c07rev22/rerun/seed5 --seeds 5 --frames 200 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5734], min area 6 px

## Measurements
- components: final 9, mean 20.9, max 26; occupancy final 0.27
- tracks: 68; persistent (alive >= 50% of run): 21; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.89 (1 = constant size)
- enclosures: components with a hole mean 6.76, final 2; holes at thresholds 0.2/0.35/0.5 final [50, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 9, 9], H1 [5, 3, 3]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.000713/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 5000, default): splits 22, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.364, nucleations 3
- channel total drift (end/start - 1): [-0.762, -0.361, 0.9315, -0.3584]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 101: holes 1, rim-vs-core 0.31, rim-vs-outside 0.67, heterogeneity 0.21; core [0.168, 0.577, 0.691, 0.545] rim [0.285, 0.318, 0.572, 0.578]
  - track 22 at frame 103: holes 1, rim-vs-core 0.23, rim-vs-outside 0.67, heterogeneity 0.20; core [0.156, 0.574, 0.634, 0.454] rim [0.222, 0.384, 0.585, 0.557]
  - track 33 at frame 103: holes 0, rim-vs-core 0.62, rim-vs-outside 0.88, heterogeneity 0.22; core [0.164, 0.677, 0.653, 0.466] rim [0.374, 0.191, 0.639, 0.784]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 121 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 4.47, rim/outside 0.936 (aggregate of 121 individuals; 0/121 membrane-like individually; rim level 0.506)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 8.31 (aggregate of 121 individuals; 1/121 membrane-like individually; rim level 0.523)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 6.52 (aggregate of 121 individuals; 79/121 membrane-like individually; rim level 0.766)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.71, rim/outside 5.62 (aggregate of 121 individuals; 106/121 membrane-like individually; rim level 0.752)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #17 (t=25250, R_eq 9.25, ring): ['L link', 'membrane (wall)']; #22 (t=25750, R_eq 13.81, ring): ['membrane (wall)']; #33 (t=25750, R_eq 7.44): ['L link', 'membrane (wall)']; #54 (t=32000, R_eq 17.98, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 38 of 121 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
