# Evidence pack: pcell-mwall (seed 2)

- world: `../../world_m15.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [192, 192]; wall 1560s; status ok
- command: `python -m labkit.run scratch/c14/world_m15.py --out scratch/c14/mpack15/seed2 --seeds 2 --size 192 192 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5704], min area 6 px

## Measurements
- components: final 18, mean 21.1, max 24; occupancy final 0.34
- tracks: 64; persistent (alive >= 50% of run): 21; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 58.05 (1 = constant size)
- enclosures: components with a hole mean 7.69, final 7; holes at thresholds 0.2/0.35/0.5 final [33, 7, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [13, 12, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000666/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 10000, default): splits 20, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.15, nucleations 2
- channel total drift (end/start - 1): [-0.6844, -0.4678, 0.6254, -0.1093, -0.2893, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 1.06, heterogeneity 0.19; core [0.268, 0.632, 0.876, 0.827, 0.833, 0.546] rim [0.405, 0.192, 0.56, 0.674, 0.761, 0.45]
  - track 12 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 1.05, heterogeneity 0.20; core [0.236, 0.727, 0.858, 0.768, 0.828, 0.518] rim [0.397, 0.207, 0.58, 0.705, 0.754, 0.476]
  - track 15 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 1.05, heterogeneity 0.22; core [0.215, 0.656, 0.743, 0.624, 0.91, 0.378] rim [0.385, 0.163, 0.552, 0.724, 0.709, 0.474]
  - track 51 at frame 143: holes 0, rim-vs-core 0.45, rim-vs-outside 1.26, heterogeneity 0.19; core [0.253, 0.738, 0.95, 0.833, 0.85, 0.597] rim [0.349, 0.392, 0.726, 0.746, 0.825, 0.481]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 125 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.52, rim/outside 0.941 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.486)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.693, rim/outside 7.24 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.554)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 6.28 (aggregate of 125 individuals; 73/125 membrane-like individually; rim level 0.767)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.87, rim/outside 5.2 (aggregate of 125 individuals; 102/125 membrane-like individually; rim level 0.749)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 5.72 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.866)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.41, rim/outside 5.75 (aggregate of 125 individuals; 111/125 membrane-like individually; rim level 0.566)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #11 (t=50500, R_eq 7.07): ['membrane (wall)', 'M wall material']; #12 (t=50500, R_eq 7.57): ['L link', 'membrane (wall)', 'M wall material']; #15 (t=50500, R_eq 9.93): ['L link', 'membrane (wall)', 'M wall material']; #51 (t=71500, R_eq 6.41): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 125 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
