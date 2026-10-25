# Evidence pack: phase-membrane (seed 14)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0738-c05-review-pm-damage-mature/twin/seed14 --seeds 14 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5371], min area 6 px

## Measurements
- components: final 21, mean 16.0, max 23; occupancy final 0.29
- tracks: 130; persistent (alive >= 50% of run): 5; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.47 (1 = constant size)
- enclosures: components with a hole mean 10.14, final 10; holes at thresholds 0.2/0.35/0.5 final [1, 10, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 21], H1 [18, 13, 6]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00894/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 50, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.08, nucleations 0
- channel total drift (end/start - 1): [-0.4812, -0.7166, 0.0529, -0.2487]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 98: holes 1, rim-vs-core 0.18, rim-vs-outside 0.86, heterogeneity 0.18; core [0.081, 0.743, 0.489, 0.619] rim [0.167, 0.595, 0.525, 0.634]
  - track 45 at frame 52: holes 1, rim-vs-core 0.37, rim-vs-outside 0.85, heterogeneity 0.22; core [0.111, 0.868, 0.633, 0.554] rim [0.247, 0.543, 0.519, 0.601]
  - track 79 at frame 117: holes 1, rim-vs-core 0.16, rim-vs-outside 0.80, heterogeneity 0.19; core [0.089, 0.745, 0.527, 0.653] rim [0.163, 0.616, 0.518, 0.6]
  - track 98 at frame 132: holes 1, rim-vs-core 0.18, rim-vs-outside 0.81, heterogeneity 0.19; core [0.102, 0.775, 0.574, 0.63] rim [0.17, 0.621, 0.524, 0.601]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11, rim/outside 0.856 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.486)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 6.13 (aggregate of 101 individuals; 1/101 membrane-like individually; rim level 0.757)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 4.8 (aggregate of 101 individuals; 85/101 membrane-like individually; rim level 0.627)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.54, rim/outside 4.95 (aggregate of 101 individuals; 82/101 membrane-like individually; rim level 0.681)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #63 (t=4900, R_eq 10.84, ring): ['L link', 'membrane (wall)']; #45 (t=2600, R_eq 8.63, ring): ['L link', 'membrane (wall)']; #79 (t=5850, R_eq 12.02, ring): ['L link', 'membrane (wall)']; #98 (t=6600, R_eq 11.33, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 58 of 101 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
