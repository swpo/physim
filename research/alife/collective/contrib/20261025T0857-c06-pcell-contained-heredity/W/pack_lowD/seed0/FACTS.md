# Evidence pack: pcell-multilevel-nogate-lowD (seed 0)

- world: `../../world_lowD.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 125 steps x dt 1.0 = time 20000; grid [128, 128]; wall 87s; status ok
- command: `python -m labkit.run collective/work/pcell/W/world_lowD.py --out collective/work/pcell/W/pack_lowD --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5546], min area 6 px

## Measurements
- components: final 4, mean 9.8, max 20; occupancy final 0.21
- tracks: 49; persistent (alive >= 50% of run): 7; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.15 (1 = constant size)
- enclosures: components with a hole mean 7.61, final 1; holes at thresholds 0.2/0.35/0.5 final [30, 1, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 4, 4], H1 [10, 3, 2]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00377/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2500, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.182, nucleations 2
- channel total drift (end/start - 1): [-0.7704, -0.3954, 0.7938, -0.4277, -0.0127]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 81: holes 1, rim-vs-core 0.10, rim-vs-outside 0.81, heterogeneity 0.19; core [0.214, 0.507, 0.669, 0.579, 0.786] rim [0.262, 0.458, 0.605, 0.575, 0.743]
  - track 28 at frame 82: holes 1, rim-vs-core 0.28, rim-vs-outside 0.79, heterogeneity 0.22; core [0.252, 0.559, 0.758, 0.592, 0.808] rim [0.333, 0.392, 0.592, 0.557, 0.691]
  - track 29 at frame 82: holes 1, rim-vs-core 0.17, rim-vs-outside 0.85, heterogeneity 0.19; core [0.227, 0.45, 0.663, 0.737, 0.798] rim [0.26, 0.457, 0.599, 0.589, 0.754]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.63, rim/outside 0.892 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.446)
  - radial K particles: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 3.61 (aggregate of 52 individuals; 3/52 membrane-like individually; rim level 0.525)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 2.5 (aggregate of 52 individuals; 25/52 membrane-like individually; rim level 0.55)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.4, rim/outside 2.3 (aggregate of 52 individuals; 40/52 membrane-like individually; rim level 0.467)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 2.91 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.738)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #19 (t=10125, R_eq 13.29, ring): ['membrane (wall)']; #20 (t=10125, R_eq 20.35, ring): none; #28 (t=10250, R_eq 9.52, ring): ['L link', 'membrane (wall)']; #29 (t=10250, R_eq 14.82, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 52 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
