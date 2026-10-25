# Evidence pack: pcell (seed 5)

- world: `../../world_cy003.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 625 steps x dt 1.0 = time 100000; grid [128, 128]; wall 371s; status ok
- command: `python -m labkit.run collective/work_c05/rev_cb/world_cy003.py --out collective/work_c05/rev_cb/rerun/seed5 --seeds 5 --frames 160 --spf 625 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6126], min area 6 px

## Measurements
- components: final 23, mean 23.9, max 29; occupancy final 0.34
- tracks: 103; persistent (alive >= 50% of run): 14; longest 159 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.27 (1 = constant size)
- enclosures: components with a hole mean 8.52, final 8; holes at thresholds 0.2/0.35/0.5 final [8, 8, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 23, 23], H1 [17, 13, 1]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.001/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 12500, default): splits 39, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.077, nucleations 1
- channel total drift (end/start - 1): [-0.5647, -0.61, 0.3326, -0.167]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 82: holes 0, rim-vs-core 0.62, rim-vs-outside 0.92, heterogeneity 0.22; core [0.144, 0.69, 0.721, 0.487] rim [0.348, 0.193, 0.673, 0.796]
  - track 27 at frame 82: holes 0, rim-vs-core 0.65, rim-vs-outside 0.51, heterogeneity 0.20; core [0.208, 0.604, 0.836, 0.793] rim [0.37, 0.144, 0.477, 0.569]
  - track 62 at frame 117: holes 0, rim-vs-core 0.59, rim-vs-outside 0.55, heterogeneity 0.20; core [0.234, 0.56, 0.855, 0.775] rim [0.385, 0.121, 0.526, 0.637]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.36, rim/outside 0.902 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.511)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 12 (aggregate of 151 individuals; 1/151 membrane-like individually; rim level 0.52)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 9.57 (aggregate of 151 individuals; 85/151 membrane-like individually; rim level 0.778)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.33, rim/outside 7.98 (aggregate of 151 individuals; 139/151 membrane-like individually; rim level 0.772)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #21 (t=51250, R_eq 6.65): ['L link', 'membrane (wall)']; #27 (t=51250, R_eq 5.2): ['membrane (wall)']; #39 (t=56250, R_eq 14.83, ring): ['membrane (wall)']; #62 (t=73125, R_eq 5.08): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 151 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
