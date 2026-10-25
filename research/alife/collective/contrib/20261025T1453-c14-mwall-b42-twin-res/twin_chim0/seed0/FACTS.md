# Evidence pack: pcell-mwall-b42-chim0 (seed 0)

- world: `../../world_m42_chim0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 606s; status ok
- command: `python -m labkit.run scratch/c14/world_m42_chim0.py --out scratch/c14/m42chim0/seed0 --seeds 0 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6205], min area 6 px

## Measurements
- components: final 29, mean 24.4, max 29; occupancy final 0.35
- tracks: 69; persistent (alive >= 50% of run): 21; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 26.86 (1 = constant size)
- enclosures: components with a hole mean 6.50, final 12; holes at thresholds 0.2/0.35/0.5 final [0, 12, 20]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 29, 29], H1 [23, 20, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000431/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 10000, default): splits 20, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.4977, -0.6544, 0.1679, -0.0944, -0.5968, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 1.26, heterogeneity 0.19; core [0.123, 0.662, 0.666, 0.5, 0.894, 0.782] rim [0.349, 0.207, 0.659, 0.793, 0.766, 0.667]
  - track 18 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 1.27, heterogeneity 0.20; core [0.147, 0.717, 0.742, 0.604, 0.791, 0.931] rim [0.368, 0.236, 0.643, 0.749, 0.69, 0.775]
  - track 20 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 0.93, heterogeneity 0.18; core [0.204, 0.664, 0.858, 0.76, 0.839, 0.896] rim [0.391, 0.157, 0.491, 0.595, 0.779, 0.736]
  - track 56 at frame 163: holes 1, rim-vs-core 0.38, rim-vs-outside 1.03, heterogeneity 0.20; core [0.106, 0.593, 0.667, 0.548, 0.998, 0.644] rim [0.239, 0.303, 0.578, 0.615, 0.824, 0.592]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.47, rim/outside 0.873 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.566)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.715, rim/outside 23.2 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.535)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 18.4 (aggregate of 150 individuals; 113/150 membrane-like individually; rim level 0.806)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.75, rim/outside 15.2 (aggregate of 150 individuals; 141/150 membrane-like individually; rim level 0.826)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 19.3 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.89)
  - radial M wall material: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 13.6 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.754)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #12 (t=50500, R_eq 7.07): ['L link', 'membrane (wall)']; #18 (t=50500, R_eq 6.02): ['L link', 'membrane (wall)']; #20 (t=50500, R_eq 5.35): ['L link', 'membrane (wall)']; #56 (t=81500, R_eq 8.69, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 38 of 150 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
