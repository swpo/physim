# Evidence pack: particle-lenia-turnover (seed 7)

- world: `../../world.py`, family `particle-lenia`
- parent: collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py; mutation: particle turnover: random feed of new particles plus decay of every particle (c13)
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 606s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev/rerun/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.9587], min area 6 px

## Measurements
- components: final 62, mean 54.0, max 84; occupancy final 0.22
- tracks: 563; persistent (alive >= 50% of run): 17; longest 170 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.50 (1 = constant size)
- enclosures: components with a hole mean 15.64, final 22; holes at thresholds 0.2/0.35/0.5 final [6, 22, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 60, 31], H1 [48, 0, 0]
- motion: 148 long-lived tracks moved >= 1 body length; max speed 0.25/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 100, default): splits 83, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 95, merge/split ratio 1.15, nucleations 225
- channel total drift (end/start - 1): [-0.0066, -0.0066, 1.3396]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 163 at frame 116: holes 0, rim-vs-core 0.48, rim-vs-outside 0.49, heterogeneity 0.18; core [0.796, 0.177, 0.82] rim [0.555, 0.335, 0.439]
  - track 186 at frame 126: holes 0, rim-vs-core 0.50, rim-vs-outside 0.44, heterogeneity 0.20; core [0.839, 0.178, 0.808] rim [0.517, 0.342, 0.462]
  - track 190 at frame 128: holes 1, rim-vs-core 0.22, rim-vs-outside 0.40, heterogeneity 0.20; core [0.691, 0.2, 0.641] rim [0.533, 0.245, 0.494]
  - track 191 at frame 128: holes 1, rim-vs-core 0.27, rim-vs-outside 0.39, heterogeneity 0.22; core [0.753, 0.096, 0.406] rim [0.516, 0.187, 0.504]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 335 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 5.72 (aggregate of 335 individuals; 172/335 membrane-like individually; rim level 0.687)
  - radial U field: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 5.27, rim/outside 0.756 (aggregate of 335 individuals; 1/335 membrane-like individually; rim level 0.497)
  - radial G(U): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 21.8 (aggregate of 335 individuals; 204/335 membrane-like individually; rim level 0.67)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): G(U)
- membrane-like channels per top track at mid-life: #163 (t=580, R_eq 4.41): none; #186 (t=630, R_eq 4.18): ['G(U)']; #190 (t=640, R_eq 4.26, ring): ['particle density', 'G(U)']; #191 (t=640, R_eq 4.26, ring): ['particle density', 'G(U)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 101 of 335 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
