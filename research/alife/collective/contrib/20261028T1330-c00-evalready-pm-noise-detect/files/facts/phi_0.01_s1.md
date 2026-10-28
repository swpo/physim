# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.01_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5447], min area 6 px

## Measurements
- components: final 17, mean 17.0, max 62; occupancy final 0.33
- tracks: 186; persistent (alive >= 50% of run): 2; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.64 (1 = constant size)
- enclosures: components with a hole mean 10.58, final 13; holes at thresholds 0.2/0.35/0.5 final [0, 13, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [18, 15, 11]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.011/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.148, nucleations 22
- channel total drift (end/start - 1): [-0.5009, -0.6723, 0.087, 0.1348]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 91 at frame 59: holes 1, rim-vs-core 0.15, rim-vs-outside 0.80, heterogeneity 0.18; core [0.09, 0.727, 0.513, 0.652] rim [0.152, 0.593, 0.495, 0.619]
  - track 122 at frame 97: holes 1, rim-vs-core 0.19, rim-vs-outside 0.78, heterogeneity 0.19; core [0.098, 0.773, 0.549, 0.627] rim [0.161, 0.604, 0.504, 0.606]
  - track 145 at frame 121: holes 1, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.20; core [0.107, 0.801, 0.608, 0.651] rim [0.185, 0.603, 0.515, 0.592]
  - track 153 at frame 124: holes 0, rim-vs-core 0.33, rim-vs-outside 0.93, heterogeneity 0.21; core [0.099, 0.83, 0.579, 0.546] rim [0.224, 0.546, 0.514, 0.627]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 13.1, rim/outside 0.871 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.463)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 5 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.711)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 4.04 (aggregate of 98 individuals; 87/98 membrane-like individually; rim level 0.565)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.92, rim/outside 3.75 (aggregate of 98 individuals; 84/98 membrane-like individually; rim level 0.646)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #91 (t=2950, R_eq 11.7, ring): ['L link', 'membrane (wall)']; #122 (t=4850, R_eq 12.28, ring): ['L link', 'membrane (wall)']; #145 (t=6050, R_eq 8.67, ring): ['L link', 'membrane (wall)']; #153 (t=6200, R_eq 9.44): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 72 of 98 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
