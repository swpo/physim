# Evidence pack: pcell-multilevel (seed 3)

- world: `../../20261025T0820-c06-pcell-multilevel-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 375s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0820-c06-pcell-multilevel-claim/world.py --out collective/contrib/20261025T0840-c01-review-pcell-multilevel/rerun --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6236], min area 6 px

## Measurements
- components: final 22, mean 23.8, max 29; occupancy final 0.34
- tracks: 97; persistent (alive >= 50% of run): 17; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.39 (1 = constant size)
- enclosures: components with a hole mean 9.16, final 7; holes at thresholds 0.2/0.35/0.5 final [6, 7, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 22, 22], H1 [16, 11, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000583/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 10000, default): splits 34, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 5, merges 4, merge/split ratio 0.118, nucleations 2
- channel total drift (end/start - 1): [-0.5941, -0.5798, 0.3937, -0.0849, -0.4573]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 87: holes 0, rim-vs-core 0.67, rim-vs-outside 0.72, heterogeneity 0.21; core [0.195, 0.679, 0.81, 0.709, 0.693] rim [0.394, 0.149, 0.51, 0.641, 0.511]
  - track 20 at frame 84: holes 0, rim-vs-core 0.67, rim-vs-outside 0.76, heterogeneity 0.17; core [0.243, 0.683, 0.916, 0.838, 0.619] rim [0.399, 0.197, 0.55, 0.604, 0.588]
  - track 39 at frame 94: holes 0, rim-vs-core 0.64, rim-vs-outside 0.80, heterogeneity 0.18; core [0.224, 0.645, 0.893, 0.758, 0.666] rim [0.391, 0.165, 0.533, 0.64, 0.636]
  - track 77 at frame 161: holes 0, rim-vs-core 0.50, rim-vs-outside 1.13, heterogeneity 0.21; core [0.154, 0.731, 0.648, 0.464, 0.766] rim [0.285, 0.354, 0.699, 0.742, 0.661]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.51, rim/outside 0.913 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.504)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.718, rim/outside 10.8 (aggregate of 151 individuals; 1/151 membrane-like individually; rim level 0.516)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 8.47 (aggregate of 151 individuals; 96/151 membrane-like individually; rim level 0.763)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.4, rim/outside 7.07 (aggregate of 151 individuals; 134/151 membrane-like individually; rim level 0.752)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 8.38 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.738)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #22 (t=43500, R_eq 5.78): ['L link', 'membrane (wall)']; #20 (t=42000, R_eq 4.55): ['membrane (wall)']; #39 (t=47000, R_eq 5.05): ['membrane (wall)']; #77 (t=80500, R_eq 6.26): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 151 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
