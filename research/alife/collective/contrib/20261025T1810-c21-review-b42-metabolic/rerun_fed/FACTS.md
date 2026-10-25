# Evidence pack: pcell-mwall-b42 (seed 8)

- world: `../../20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 549s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world.py --out collective/contrib/20261025T1810-c21-review-b42-metabolic/rerun_fed --seeds 8 --threshold 0.35 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0, 1.6239], min area 6 px

## Measurements
- components: final 27, mean 24.1, max 30; occupancy final 0.36
- tracks: 52; persistent (alive >= 50% of run): 22; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.86 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 8, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 27, 27], H1 [18, 12, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.000576/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 10000, default): splits 11, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4514, -0.6993, 0.0168, -0.1447, -0.661, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 101: holes 0, rim-vs-core 0.75, rim-vs-outside 0.90, heterogeneity 0.26; core [0.143, 0.623, 0.747, 0.668, 0.828, 0.531] rim [0.415, 0.125, 0.419, 0.526, 0.508, 0.46]
  - track 12 at frame 101: holes 0, rim-vs-core 1.08, rim-vs-outside 0.42, heterogeneity 0.27; core [0.283, 0.453, 0.779, 0.768, 0.76, 0.7] rim [0.512, 0.057, 0.239, 0.314, 0.186, 0.343]
  - track 13 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 1.23, heterogeneity 0.24; core [0.064, 0.632, 0.549, 0.424, 0.893, 0.252] rim [0.324, 0.203, 0.552, 0.69, 0.665, 0.562]
  - track 42 at frame 187: holes 0, rim-vs-core 0.71, rim-vs-outside 0.93, heterogeneity 0.26; core [0.148, 0.526, 0.678, 0.585, 0.929, 0.409] rim [0.399, 0.096, 0.432, 0.577, 0.487, 0.475]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.6, rim/outside 0.883 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.634)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.531, rim/outside 21.2 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.422)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 27.2 (aggregate of 146 individuals; 93/146 membrane-like individually; rim level 0.844)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.83, rim/outside 24.2 (aggregate of 146 individuals; 136/146 membrane-like individually; rim level 0.857)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 25.1 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.825)
  - radial M wall material: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 3.42, rim/outside 25.1 (aggregate of 146 individuals; 139/146 membrane-like individually; rim level 0.763)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #11 (t=50500, R_eq 7.07): ['L link', 'membrane (wall)', 'M wall material']; #12 (t=50500, R_eq 5.64): ['membrane (wall)', 'M wall material']; #13 (t=50500, R_eq 10.25): ['M wall material']; #42 (t=93500, R_eq 7.82): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
