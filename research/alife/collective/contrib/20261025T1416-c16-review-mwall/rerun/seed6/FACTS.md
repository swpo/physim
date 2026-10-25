# Evidence pack: pcell-mwall (seed 6)

- world: `../../../20261025T1345-c14-pcell-mwall-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 650s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1345-c14-pcell-mwall-claim/world.py --out collective/contrib/20261025T1416-c16-review-mwall/rerun/seed6 --seeds 6 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5749], min area 6 px

## Measurements
- components: final 15, mean 19.5, max 24; occupancy final 0.38
- tracks: 56; persistent (alive >= 50% of run): 17; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 39.86 (1 = constant size)
- enclosures: components with a hole mean 7.12, final 9; holes at thresholds 0.2/0.35/0.5 final [14, 12, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 15, 15], H1 [13, 10, 2]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.000818/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 10000, default): splits 15, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.333, nucleations 2
- channel total drift (end/start - 1): [-0.6577, -0.5126, 0.583, 0.019, -0.3339, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 1.22, heterogeneity 0.22; core [0.177, 0.573, 0.721, 0.531, 0.94, 0.356] rim [0.264, 0.408, 0.629, 0.585, 0.846, 0.423]
  - track 22 at frame 101: holes 1, rim-vs-core 0.55, rim-vs-outside 1.25, heterogeneity 0.22; core [0.114, 0.71, 0.523, 0.284, 0.923, 0.174] rim [0.247, 0.406, 0.606, 0.607, 0.833, 0.435]
  - track 24 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 1.20, heterogeneity 0.22; core [0.19, 0.705, 0.735, 0.604, 0.863, 0.379] rim [0.378, 0.206, 0.629, 0.741, 0.704, 0.552]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.66, rim/outside 0.964 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.486)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.667, rim/outside 5.9 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.493)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 5.41 (aggregate of 115 individuals; 57/115 membrane-like individually; rim level 0.744)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 4.85 (aggregate of 115 individuals; 92/115 membrane-like individually; rim level 0.718)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 4.94 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.851)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.94, rim/outside 4.9 (aggregate of 115 individuals; 99/115 membrane-like individually; rim level 0.561)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #21 (t=50500, R_eq 8.08): ['L link', 'membrane (wall)', 'M wall material']; #22 (t=50500, R_eq 11.23): ['membrane (wall)']; #24 (t=50500, R_eq 6.15): ['L link', 'membrane (wall)', 'M wall material']; #51 (t=76500, R_eq 23.46, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
