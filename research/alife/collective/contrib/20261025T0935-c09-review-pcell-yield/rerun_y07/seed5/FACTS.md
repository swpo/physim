# Evidence pack: pcell (seed 5)

- world: `../../world_y07.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 100 steps x dt 1.0 = time 16000; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0935-c09-review-pcell-yield/world_y07.py --out collective/contrib/20261025T0935-c09-review-pcell-yield/rerun_y07/seed5 --seeds 5 --frames 160 --spf 100 --lineage-k 10 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.618], min area 6 px

## Measurements
- components: final 24, mean 20.9, max 27; occupancy final 0.32
- tracks: 69; persistent (alive >= 50% of run): 17; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.34 (1 = constant size)
- enclosures: components with a hole mean 6.84, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 12, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 24, 24], H1 [18, 18, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00134/time; max body lengths 1.5
- replication (lineage window K = 10 frames = time 1000, --lineage-k): splits 17, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.176, nucleations 1
- channel total drift (end/start - 1): [-0.4594, -0.6905, 0.0515, -0.2427]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 82: holes 0, rim-vs-core 0.39, rim-vs-outside 0.87, heterogeneity 0.23; core [0.125, 0.726, 0.712, 0.545] rim [0.264, 0.381, 0.635, 0.628]
  - track 25 at frame 82: holes 0, rim-vs-core 0.67, rim-vs-outside 0.56, heterogeneity 0.22; core [0.223, 0.704, 0.821, 0.71] rim [0.45, 0.181, 0.481, 0.623]
  - track 27 at frame 82: holes 0, rim-vs-core 0.64, rim-vs-outside 0.52, heterogeneity 0.20; core [0.261, 0.61, 0.829, 0.786] rim [0.451, 0.161, 0.476, 0.576]
  - track 61 at frame 121: holes 0, rim-vs-core 0.39, rim-vs-outside 0.84, heterogeneity 0.22; core [0.112, 0.575, 0.617, 0.453] rim [0.266, 0.299, 0.617, 0.674]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.19, rim/outside 0.851 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.586)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 26.3 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.545)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 21.5 (aggregate of 129 individuals; 98/129 membrane-like individually; rim level 0.775)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.81, rim/outside 18 (aggregate of 129 individuals; 124/129 membrane-like individually; rim level 0.803)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #24 (t=8200, R_eq 7.53): ['L link', 'membrane (wall)']; #25 (t=8200, R_eq 5.73): ['L link', 'membrane (wall)']; #27 (t=8200, R_eq 5.23): ['membrane (wall)']; #61 (t=12100, R_eq 8.1): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 41 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
