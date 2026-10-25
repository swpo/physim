# Evidence pack: pcell-mwall-b42-starve (seed 1)

- world: `../../world_m42_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 730s; status ok
- command: `python -m labkit.run scratch/c14/world_m42_starve.py --out scratch/c14/m42starve/seed1 --seeds 1 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5965], min area 6 px

## Measurements
- components: final 0, mean 16.8, max 33; occupancy final 0.00
- tracks: 58; persistent (alive >= 50% of run): 21; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.33 (1 = constant size)
- enclosures: components with a hole mean 2.49, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.00118/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 14, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6512, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 61: holes 0, rim-vs-core 0.64, rim-vs-outside 1.33, heterogeneity 0.22; core [0.106, 0.767, 0.775, 0.576, 0.925, 0.429] rim [0.324, 0.251, 0.691, 0.767, 0.851, 0.653]
  - track 7 at frame 61: holes 0, rim-vs-core 0.63, rim-vs-outside 0.90, heterogeneity 0.21; core [0.2, 0.613, 0.824, 0.761, 0.833, 0.649] rim [0.401, 0.149, 0.517, 0.608, 0.69, 0.599]
  - track 9 at frame 61: holes 0, rim-vs-core 0.43, rim-vs-outside 1.31, heterogeneity 0.23; core [0.115, 0.743, 0.72, 0.566, 0.863, 0.412] rim [0.245, 0.429, 0.686, 0.708, 0.783, 0.609]
  - track 46 at frame 87: holes 1, rim-vs-core 0.36, rim-vs-outside 1.00, heterogeneity 0.23; core [0.116, 0.552, 0.672, 0.551, 0.99, 0.39] rim [0.227, 0.302, 0.574, 0.597, 0.824, 0.516]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.09, rim/outside 0.854 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.559)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.649, rim/outside 28 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.525)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 27.2 (aggregate of 84 individuals; 57/84 membrane-like individually; rim level 0.832)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.05, rim/outside 23.9 (aggregate of 84 individuals; 79/84 membrane-like individually; rim level 0.86)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 27.4 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.861)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.78, rim/outside 24.4 (aggregate of 84 individuals; 81/84 membrane-like individually; rim level 0.787)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #2 (t=30500, R_eq 6.18): ['L link', 'membrane (wall)', 'M wall material']; #7 (t=30500, R_eq 5.56): ['L link', 'membrane (wall)', 'M wall material']; #9 (t=30500, R_eq 6.51): ['L link', 'membrane (wall)', 'M wall material']; #46 (t=43500, R_eq 9.74, ring): ['membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
