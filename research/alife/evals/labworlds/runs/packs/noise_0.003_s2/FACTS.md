# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.003 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.003_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0058, 1.5316], min area 6 px

## Measurements
- components: final 16, mean 12.3, max 23; occupancy final 0.30
- tracks: 132; persistent (alive >= 50% of run): 2; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.11 (1 = constant size)
- enclosures: components with a hole mean 7.87, final 12; holes at thresholds 0.2/0.35/0.5 final [2, 12, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [16, 16, 13]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0116/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 48, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.146, nucleations 1
- channel total drift (end/start - 1): [-0.4751, -0.6715, 0.2362, -0.2776]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 70: holes 0, rim-vs-core 0.51, rim-vs-outside 0.90, heterogeneity 0.21; core [0.127, 0.907, 0.682, 0.602] rim [0.329, 0.463, 0.618, 0.726]
  - track 64 at frame 86: holes 0, rim-vs-core 0.40, rim-vs-outside 0.88, heterogeneity 0.19; core [0.089, 0.782, 0.523, 0.588] rim [0.282, 0.456, 0.574, 0.708]
  - track 67 at frame 85: holes 1, rim-vs-core 0.40, rim-vs-outside 0.77, heterogeneity 0.22; core [0.112, 0.862, 0.632, 0.56] rim [0.256, 0.513, 0.506, 0.594]
  - track 81 at frame 98: holes 1, rim-vs-core 0.20, rim-vs-outside 0.81, heterogeneity 0.20; core [0.098, 0.814, 0.58, 0.595] rim [0.175, 0.63, 0.537, 0.605]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 13.2, rim/outside 0.81 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.489)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 6.58 (aggregate of 75 individuals; 1/75 membrane-like individually; rim level 0.765)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 3.68 (aggregate of 75 individuals; 64/75 membrane-like individually; rim level 0.601)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.14, rim/outside 5.93 (aggregate of 75 individuals; 62/75 membrane-like individually; rim level 0.657)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #60 (t=3500, R_eq 7): ['L link', 'membrane (wall)']; #64 (t=4300, R_eq 8.59): ['L link', 'membrane (wall)']; #67 (t=4250, R_eq 9.18, ring): ['L link', 'membrane (wall)']; #81 (t=4900, R_eq 10.51, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 44 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
