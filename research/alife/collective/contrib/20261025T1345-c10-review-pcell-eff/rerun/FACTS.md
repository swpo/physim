# Evidence pack: pcell-yeff-cap (seed 5)

- world: `../../20261025T1108-c06-pcell-efficiency-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 565s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1108-c06-pcell-efficiency-claim/world.py --out collective/contrib/20261025T1345-c10-review-pcell-eff/rerun --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5456], min area 6 px

## Measurements
- components: final 11, mean 16.4, max 23; occupancy final 0.40
- tracks: 63; persistent (alive >= 50% of run): 15; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.39 (1 = constant size)
- enclosures: components with a hole mean 8.32, final 9; holes at thresholds 0.2/0.35/0.5 final [17, 9, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 11, 11], H1 [10, 10, 5]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.000748/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.4, nucleations 17
- channel total drift (end/start - 1): [-0.6963, -0.4495, 0.7362, -0.1226, -0.2495]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 1, rim-vs-core 0.19, rim-vs-outside 0.89, heterogeneity 0.22; core [0.221, 0.516, 0.665, 0.541, 0.998] rim [0.266, 0.393, 0.605, 0.566, 0.884]
  - track 21 at frame 101: holes 1, rim-vs-core 0.44, rim-vs-outside 0.99, heterogeneity 0.24; core [0.198, 0.626, 0.669, 0.471, 0.984] rim [0.318, 0.299, 0.593, 0.614, 0.777]
  - track 23 at frame 101: holes 1, rim-vs-core 0.34, rim-vs-outside 0.86, heterogeneity 0.22; core [0.173, 0.599, 0.547, 0.295, 0.975] rim [0.249, 0.412, 0.582, 0.544, 0.873]
  - track 36 at frame 108: holes 1, rim-vs-core 0.27, rim-vs-outside 0.92, heterogeneity 0.23; core [0.205, 0.58, 0.69, 0.509, 0.972] rim [0.275, 0.391, 0.616, 0.578, 0.82]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 2.85, rim/outside 1.01 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.473)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 3.83 (aggregate of 94 individuals; 1/94 membrane-like individually; rim level 0.522)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 3.16 (aggregate of 94 individuals; 39/94 membrane-like individually; rim level 0.696)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.44, rim/outside 2.72 (aggregate of 94 individuals; 72/94 membrane-like individually; rim level 0.604)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 3.13 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.898)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #6 (t=50500, R_eq 11.06, ring): ['membrane (wall)']; #21 (t=50500, R_eq 9.24, ring): ['L link', 'membrane (wall)']; #23 (t=50500, R_eq 14.49, ring): ['membrane (wall)']; #36 (t=54000, R_eq 10.42, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 52 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
