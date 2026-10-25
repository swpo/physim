# Evidence pack: pcell-multilevel-lowmu (seed 7)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0923-c06-pcell-somatic-decline/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 354s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0923-c06-pcell-somatic-decline/world.py --out /tmp/claude-0/c11rev14/rerun --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6261], min area 6 px

## Measurements
- components: final 25, mean 26.5, max 32; occupancy final 0.29
- tracks: 74; persistent (alive >= 50% of run): 25; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.50 (1 = constant size)
- enclosures: components with a hole mean 7.00, final 3; holes at thresholds 0.2/0.35/0.5 final [12, 3, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 25, 25], H1 [10, 6, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0013/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 10000, default): splits 20, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.05, nucleations 3
- channel total drift (end/start - 1): [-0.6666, -0.508, 0.6083, -0.0466, -0.2602]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 101: holes 1, rim-vs-core 0.42, rim-vs-outside 0.89, heterogeneity 0.22; core [0.13, 0.569, 0.627, 0.504, 0.76] rim [0.28, 0.26, 0.573, 0.638, 0.57]
  - track 19 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 1.10, heterogeneity 0.21; core [0.125, 0.702, 0.651, 0.416, 0.711] rim [0.327, 0.278, 0.669, 0.78, 0.623]
  - track 21 at frame 101: holes 0, rim-vs-core 0.63, rim-vs-outside 0.70, heterogeneity 0.20; core [0.198, 0.653, 0.797, 0.71, 0.623] rim [0.395, 0.159, 0.489, 0.621, 0.502]
  - track 53 at frame 146: holes 0, rim-vs-core 0.61, rim-vs-outside 0.76, heterogeneity 0.20; core [0.21, 0.597, 0.813, 0.742, 0.709] rim [0.384, 0.137, 0.5, 0.611, 0.587]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 164 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.89, rim/outside 0.917 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.517)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.684, rim/outside 13 (aggregate of 164 individuals; 1/164 membrane-like individually; rim level 0.507)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 10.6 (aggregate of 164 individuals; 109/164 membrane-like individually; rim level 0.794)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.4, rim/outside 9.15 (aggregate of 164 individuals; 152/164 membrane-like individually; rim level 0.817)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 9.74 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.721)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #16 (t=50500, R_eq 8.78, ring): ['L link', 'membrane (wall)']; #19 (t=50500, R_eq 7.65): ['L link', 'membrane (wall)']; #21 (t=50500, R_eq 5.89): ['L link', 'membrane (wall)']; #53 (t=73000, R_eq 5.61): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 164 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
