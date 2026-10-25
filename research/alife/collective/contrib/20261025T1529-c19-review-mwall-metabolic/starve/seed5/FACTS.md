# Evidence pack: pcell-mwall-b42-starve (seed 5)

- world: `../../../20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 461s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world_starve.py --out collective/contrib/20261025T1529-c19-review-mwall-metabolic/starve/seed5 --seeds 5 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5769], min area 6 px

## Measurements
- components: final 0, mean 13.7, max 27; occupancy final 0.00
- tracks: 50; persistent (alive >= 50% of run): 11; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.56 (1 = constant size)
- enclosures: components with a hole mean 2.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.000401/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 10000, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.6285, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 61: holes 0, rim-vs-core 0.60, rim-vs-outside 0.79, heterogeneity 0.21; core [0.223, 0.566, 0.847, 0.777, 0.804, 0.679] rim [0.409, 0.162, 0.533, 0.595, 0.642, 0.587]
  - track 5 at frame 61: holes 0, rim-vs-core 0.75, rim-vs-outside 1.28, heterogeneity 0.24; core [0.107, 0.794, 0.752, 0.565, 0.825, 0.439] rim [0.364, 0.223, 0.662, 0.765, 0.691, 0.767]
  - track 7 at frame 61: holes 0, rim-vs-core 0.65, rim-vs-outside 1.30, heterogeneity 0.22; core [0.113, 0.747, 0.722, 0.583, 0.835, 0.437] rim [0.345, 0.237, 0.662, 0.754, 0.759, 0.711]
  - track 38 at frame 97: holes 0, rim-vs-core 0.73, rim-vs-outside 1.32, heterogeneity 0.23; core [0.086, 0.71, 0.676, 0.484, 0.913, 0.35] rim [0.335, 0.21, 0.645, 0.768, 0.807, 0.706]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.839 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.585)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.705, rim/outside 33.4 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.565)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 32.1 (aggregate of 70 individuals; 57/70 membrane-like individually; rim level 0.851)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.88, rim/outside 27.5 (aggregate of 70 individuals; 67/70 membrane-like individually; rim level 0.858)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 32.5 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.871)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.38, rim/outside 28.4 (aggregate of 70 individuals; 67/70 membrane-like individually; rim level 0.793)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #2 (t=30500, R_eq 5.5): ['membrane (wall)', 'M wall material']; #5 (t=30500, R_eq 6.33): ['L link', 'membrane (wall)', 'M wall material']; #7 (t=30500, R_eq 6.53): ['L link', 'membrane (wall)', 'M wall material']; #38 (t=48500, R_eq 7.59): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
