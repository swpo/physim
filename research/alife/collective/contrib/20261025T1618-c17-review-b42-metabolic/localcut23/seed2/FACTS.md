# Evidence pack: pcell-mwall-b42-localcut (seed 2)

- world: `../../world_local.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 141 frames x 500 steps x dt 1.0 = time 70000; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/c17-b42-wip/world_local.py --out collective/contrib/c17-b42-wip/localcut23/seed2 --seeds 2 --frames 140 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6368], min area 6 px

## Measurements
- components: final 30, mean 26.3, max 30; occupancy final 0.32
- tracks: 55; persistent (alive >= 50% of run): 26; longest 141 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 36.04 (1 = constant size)
- enclosures: components with a hole mean 4.77, final 6; holes at thresholds 0.2/0.35/0.5 final [1, 6, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 30, 30], H1 [21, 14, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.00116/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 10000, default): splits 14, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.4633, -0.698, 0.058, -0.2339, -0.6546, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 71: holes 0, rim-vs-core 0.70, rim-vs-outside 1.33, heterogeneity 0.22; core [0.111, 0.767, 0.694, 0.534, 0.833, 0.401] rim [0.341, 0.24, 0.669, 0.791, 0.77, 0.704]
  - track 4 at frame 71: holes 0, rim-vs-core 0.75, rim-vs-outside 0.82, heterogeneity 0.21; core [0.263, 0.625, 0.943, 0.854, 0.775, 0.823] rim [0.442, 0.18, 0.524, 0.574, 0.677, 0.563]
  - track 5 at frame 71: holes 0, rim-vs-core 0.67, rim-vs-outside 0.91, heterogeneity 0.20; core [0.201, 0.651, 0.823, 0.778, 0.759, 0.691] rim [0.41, 0.16, 0.495, 0.579, 0.729, 0.55]
  - track 41 at frame 119: holes 0, rim-vs-core 0.32, rim-vs-outside 1.25, heterogeneity 0.24; core [0.099, 0.586, 0.647, 0.463, 0.983, 0.339] rim [0.219, 0.393, 0.601, 0.582, 0.86, 0.478]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [24, 47, 71, 93, 116, 140]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.84, rim/outside 0.851 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.574)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.656, rim/outside 29.1 (aggregate of 163 individuals; 1/163 membrane-like individually; rim level 0.508)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 28.3 (aggregate of 163 individuals; 125/163 membrane-like individually; rim level 0.823)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.23, rim/outside 24.4 (aggregate of 163 individuals; 153/163 membrane-like individually; rim level 0.867)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 28.7 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.863)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.72, rim/outside 25.6 (aggregate of 163 individuals; 155/163 membrane-like individually; rim level 0.777)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #3 (t=35500, R_eq 6.56): ['L link', 'membrane (wall)', 'M wall material']; #4 (t=35500, R_eq 4.37): ['membrane (wall)', 'M wall material']; #5 (t=35500, R_eq 5.44): ['L link', 'membrane (wall)', 'M wall material']; #41 (t=59500, R_eq 9.22): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 25 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
