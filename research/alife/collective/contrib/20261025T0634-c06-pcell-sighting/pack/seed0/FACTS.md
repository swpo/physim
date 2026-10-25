# Evidence pack: pcell (seed 0)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 34s; status ok
- command: `python -m labkit.run collective/work/pcell/world.py --out collective/work/pcell/pack --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5393], min area 6 px

## Measurements
- components: final 23, mean 18.1, max 32; occupancy final 0.36
- tracks: 88; persistent (alive >= 50% of run): 19; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.10 (1 = constant size)
- enclosures: components with a hole mean 7.31, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 23]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 23, 23], H1 [23, 22, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 1000, default): splits 22, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.227, nucleations 4
- channel total drift (end/start - 1): [-0.4812, -0.6735, 0.0986, -0.1195]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 86: holes 0, rim-vs-core 0.58, rim-vs-outside 0.85, heterogeneity 0.23; core [0.128, 0.647, 0.664, 0.468] rim [0.351, 0.195, 0.578, 0.735]
  - track 52 at frame 86: holes 0, rim-vs-core 0.61, rim-vs-outside 0.84, heterogeneity 0.23; core [0.128, 0.667, 0.651, 0.455] rim [0.358, 0.189, 0.586, 0.744]
  - track 53 at frame 86: holes 1, rim-vs-core 0.39, rim-vs-outside 0.86, heterogeneity 0.23; core [0.087, 0.725, 0.587, 0.375] rim [0.223, 0.423, 0.594, 0.579]
  - track 80 at frame 136: holes 1, rim-vs-core 0.35, rim-vs-outside 0.71, heterogeneity 0.21; core [0.141, 0.619, 0.653, 0.55] rim [0.271, 0.311, 0.567, 0.616]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.32, rim/outside 0.918 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.568)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 11.3 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.52)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 7.87 (aggregate of 118 individuals; 74/118 membrane-like individually; rim level 0.666)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.45, rim/outside 6.65 (aggregate of 118 individuals; 109/118 membrane-like individually; rim level 0.685)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #51 (t=4300, R_eq 8.06): ['L link', 'membrane (wall)']; #52 (t=4300, R_eq 8.12): ['L link', 'membrane (wall)']; #53 (t=4300, R_eq 10.37, ring): ['L link', 'membrane (wall)']; #80 (t=6800, R_eq 8.57, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 28 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
