# Evidence pack: pcell-mwall-b42-audit (seed 7)

- world: `../../world_audit.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [192, 192]; wall 869s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1931-c23-audit-b42-metabolic/world_audit.py --out collective/contrib/20261025T1931-c23-audit-b42-metabolic/rerun_res15/seed7 --seeds 7 --frames 200 --spf 500 --size 192 192 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.614], min area 6 px

## Measurements
- components: final 28, mean 26.6, max 31; occupancy final 0.34
- tracks: 72; persistent (alive >= 50% of run): 25; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 56.75 (1 = constant size)
- enclosures: components with a hole mean 7.31, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 11, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 28, 28], H1 [25, 17, 1]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.00112/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 10000, default): splits 18, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.4975, -0.6592, 0.1221, 0.121, -0.6027, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 1.19, heterogeneity 0.21; core [0.25, 0.616, 0.934, 0.86, 0.77, 0.8] rim [0.317, 0.415, 0.64, 0.672, 0.737, 0.529]
  - track 6 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 1.05, heterogeneity 0.20; core [0.224, 0.678, 0.876, 0.818, 0.81, 0.664] rim [0.397, 0.197, 0.596, 0.707, 0.736, 0.585]
  - track 12 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 1.08, heterogeneity 0.19; core [0.245, 0.7, 0.899, 0.821, 0.747, 0.726] rim [0.417, 0.213, 0.595, 0.706, 0.731, 0.597]
  - track 60 at frame 158: holes 1, rim-vs-core 0.30, rim-vs-outside 1.10, heterogeneity 0.22; core [0.092, 0.648, 0.592, 0.49, 0.988, 0.257] rim [0.178, 0.44, 0.593, 0.58, 0.95, 0.427]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 165 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.05, rim/outside 0.867 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.545)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.705, rim/outside 24.7 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.563)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 20.7 (aggregate of 165 individuals; 128/165 membrane-like individually; rim level 0.815)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.18, rim/outside 16.6 (aggregate of 165 individuals; 158/165 membrane-like individually; rim level 0.835)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 20.6 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.881)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.23, rim/outside 19.4 (aggregate of 165 individuals; 161/165 membrane-like individually; rim level 0.722)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #5 (t=50500, R_eq 7.36): ['membrane (wall)', 'M wall material']; #6 (t=50500, R_eq 7): ['membrane (wall)', 'M wall material']; #12 (t=50500, R_eq 6.72): ['membrane (wall)', 'M wall material']; #60 (t=79000, R_eq 14.44, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 45 of 165 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
