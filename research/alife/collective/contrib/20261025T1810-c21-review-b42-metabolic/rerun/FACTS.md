# Evidence pack: pcell-mwall-b42-starve (seed 8)

- world: `../../20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 514s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world_starve.py --out collective/contrib/20261025T1810-c21-review-b42-metabolic/rerun --seeds 8 --threshold 0.35 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0, 1.5923], min area 6 px

## Measurements
- components: final 0, mean 13.8, max 30; occupancy final 0.00
- tracks: 36; persistent (alive >= 50% of run): 22; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000576/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 10000, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.5087, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.68, rim-vs-outside 1.03, heterogeneity 0.26; core [0.126, 0.625, 0.721, 0.649, 0.91, 0.497] rim [0.414, 0.148, 0.446, 0.553, 0.639, 0.497]
  - track 5 at frame 61: holes 0, rim-vs-core 1.02, rim-vs-outside 0.51, heterogeneity 0.26; core [0.26, 0.49, 0.787, 0.763, 0.793, 0.713] rim [0.488, 0.072, 0.27, 0.362, 0.285, 0.354]
  - track 6 at frame 61: holes 0, rim-vs-core 0.60, rim-vs-outside 1.08, heterogeneity 0.27; core [0.13, 0.642, 0.779, 0.699, 0.911, 0.581] rim [0.304, 0.288, 0.501, 0.522, 0.635, 0.46]
  - track 10 at frame 61: holes 0, rim-vs-core 0.68, rim-vs-outside 1.15, heterogeneity 0.29; core [0.127, 0.759, 0.846, 0.605, 0.879, 0.534] rim [0.36, 0.259, 0.562, 0.602, 0.601, 0.533]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 13.4, rim/outside 0.841 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.644)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.526, rim/outside 43.5 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.452)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 76 (aggregate of 68 individuals; 49/68 membrane-like individually; rim level 0.902)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 69.3 (aggregate of 68 individuals; 65/68 membrane-like individually; rim level 0.898)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 76.6 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.887)
  - radial M wall material: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 3.62, rim/outside 67.2 (aggregate of 68 individuals; 66/68 membrane-like individually; rim level 0.836)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #4 (t=30500, R_eq 7.27): ['L link', 'membrane (wall)', 'M wall material']; #5 (t=30500, R_eq 5.86): ['membrane (wall)', 'M wall material']; #6 (t=30500, R_eq 7.82): ['L link', 'membrane (wall)', 'M wall material']; #10 (t=30500, R_eq 6.51): ['membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
