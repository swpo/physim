# Evidence pack: pcell-mwall-b42-localcut (seed 6)

- world: `../../world_local.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 424s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1547-c13-review-b42-metabolic/world_local.py --out collective/contrib/20261025T1547-c13-review-b42-metabolic/rerun_world_local/seed6 --seeds 6 --spf 500 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6315], min area 6 px

## Measurements
- components: final 29, mean 26.6, max 30; occupancy final 0.34
- tracks: 59; persistent (alive >= 50% of run): 21; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 14.17 (1 = constant size)
- enclosures: components with a hole mean 4.58, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 9, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 29], H1 [24, 18, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.000437/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 10000, default): splits 17, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.4842, -0.6767, 0.1191, -0.0503, -0.621, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.64, rim-vs-outside 0.89, heterogeneity 0.22; core [0.239, 0.555, 0.838, 0.725, 0.832, 0.642] rim [0.444, 0.113, 0.507, 0.651, 0.594, 0.582]
  - track 6 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 1.27, heterogeneity 0.22; core [0.109, 0.678, 0.647, 0.528, 0.886, 0.334] rim [0.355, 0.2, 0.645, 0.785, 0.772, 0.675]
  - track 8 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 1.28, heterogeneity 0.24; core [0.116, 0.68, 0.703, 0.486, 0.898, 0.376] rim [0.36, 0.178, 0.645, 0.785, 0.74, 0.681]
  - track 49 at frame 166: holes 0, rim-vs-core 0.38, rim-vs-outside 1.18, heterogeneity 0.25; core [0.129, 0.577, 0.683, 0.53, 0.987, 0.369] rim [0.243, 0.327, 0.59, 0.604, 0.788, 0.5]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 164 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.41, rim/outside 0.861 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.569)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.674, rim/outside 25.5 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.517)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 23.2 (aggregate of 164 individuals; 126/164 membrane-like individually; rim level 0.836)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.61, rim/outside 19.8 (aggregate of 164 individuals; 156/164 membrane-like individually; rim level 0.876)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 22.8 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.878)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.13, rim/outside 21 (aggregate of 164 individuals; 157/164 membrane-like individually; rim level 0.775)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=50500, R_eq 5.41): ['membrane (wall)', 'M wall material']; #6 (t=50500, R_eq 7.05): ['L link', 'membrane (wall)', 'M wall material']; #8 (t=50500, R_eq 6.84): ['L link', 'membrane (wall)', 'M wall material']; #49 (t=83000, R_eq 8.14): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 164 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
