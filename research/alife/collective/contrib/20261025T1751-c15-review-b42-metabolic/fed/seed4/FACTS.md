# Evidence pack: pcell-mwall-b42 (seed 4)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 793s; status ok
- command: `python -m labkit.run /root/rev7/world.py --out /root/rev7/fed/seed4 --seeds 4 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6106], min area 6 px

## Measurements
- components: final 28, mean 23.4, max 29; occupancy final 0.35
- tracks: 55; persistent (alive >= 50% of run): 19; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 19.15 (1 = constant size)
- enclosures: components with a hole mean 6.56, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 10, 22]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 28, 28], H1 [26, 19, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000423/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 10000, default): splits 18, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4837, -0.6794, 0.1229, -0.1683, -0.6146, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.64, rim-vs-outside 1.31, heterogeneity 0.22; core [0.119, 0.695, 0.712, 0.536, 0.972, 0.375] rim [0.335, 0.221, 0.626, 0.752, 0.871, 0.641]
  - track 4 at frame 101: holes 0, rim-vs-core 0.48, rim-vs-outside 1.00, heterogeneity 0.23; core [0.217, 0.624, 0.876, 0.754, 0.875, 0.658] rim [0.304, 0.358, 0.581, 0.579, 0.753, 0.512]
  - track 6 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 1.31, heterogeneity 0.23; core [0.131, 0.682, 0.738, 0.462, 0.958, 0.364] rim [0.357, 0.215, 0.646, 0.765, 0.828, 0.64]
  - track 41 at frame 151: holes 0, rim-vs-core 0.70, rim-vs-outside 1.26, heterogeneity 0.23; core [0.126, 0.61, 0.684, 0.466, 0.952, 0.342] rim [0.353, 0.183, 0.649, 0.785, 0.76, 0.676]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 145 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.18, rim/outside 0.878 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.563)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.733, rim/outside 20.6 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.536)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 16.3 (aggregate of 145 individuals; 106/145 membrane-like individually; rim level 0.792)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.59, rim/outside 13.6 (aggregate of 145 individuals; 132/145 membrane-like individually; rim level 0.803)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 17.2 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.889)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.75, rim/outside 13.8 (aggregate of 145 individuals; 132/145 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #2 (t=50500, R_eq 6.98): ['L link', 'membrane (wall)', 'M wall material']; #4 (t=50500, R_eq 5.89): ['L link', 'membrane (wall)', 'M wall material']; #6 (t=50500, R_eq 7.33): ['L link', 'membrane (wall)', 'M wall material']; #41 (t=75500, R_eq 7.29): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 39 of 145 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
