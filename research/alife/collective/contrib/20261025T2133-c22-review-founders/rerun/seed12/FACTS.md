# Evidence pack: pcell-mwall-b42 (seed 12)

- world: `../../../../20261025T1430-c14-pcell-mwall-b42-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 407s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim/world.py --out collective/contrib/wip-c22/rev_fd/rerun/seed12 --seeds 12 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6427], min area 6 px

## Measurements
- components: final 32, mean 28.6, max 33; occupancy final 0.33
- tracks: 59; persistent (alive >= 50% of run): 23; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 25.38 (1 = constant size)
- enclosures: components with a hole mean 5.17, final 12; holes at thresholds 0.2/0.35/0.5 final [0, 12, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 32], H1 [22, 17, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.00132/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 10000, default): splits 15, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.4824, -0.6699, 0.1241, -0.1602, -0.6234, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 1.02, heterogeneity 0.19; core [0.249, 0.617, 0.902, 0.828, 0.765, 0.779] rim [0.377, 0.326, 0.669, 0.698, 0.741, 0.693]
  - track 7 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.99, heterogeneity 0.18; core [0.256, 0.531, 0.853, 0.81, 0.811, 0.732] rim [0.442, 0.144, 0.54, 0.662, 0.745, 0.637]
  - track 10 at frame 101: holes 0, rim-vs-core 0.66, rim-vs-outside 0.88, heterogeneity 0.21; core [0.265, 0.533, 0.84, 0.782, 0.758, 0.689] rim [0.451, 0.113, 0.471, 0.597, 0.593, 0.528]
  - track 53 at frame 166: holes 1, rim-vs-core 0.33, rim-vs-outside 0.99, heterogeneity 0.23; core [0.145, 0.53, 0.677, 0.561, 0.998, 0.383] rim [0.241, 0.313, 0.577, 0.597, 0.83, 0.491]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 178 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.35, rim/outside 0.863 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.562)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.67, rim/outside 27.7 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.516)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 25.1 (aggregate of 178 individuals; 130/178 membrane-like individually; rim level 0.833)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.3, rim/outside 21.4 (aggregate of 178 individuals; 171/178 membrane-like individually; rim level 0.877)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 25.9 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.882)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.79, rim/outside 21.6 (aggregate of 178 individuals; 172/178 membrane-like individually; rim level 0.774)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=50500, R_eq 4.41): ['membrane (wall)', 'M wall material']; #7 (t=50500, R_eq 4.69): ['membrane (wall)', 'M wall material']; #10 (t=50500, R_eq 5.11): ['membrane (wall)', 'M wall material']; #53 (t=83000, R_eq 8.94, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 35 of 178 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
